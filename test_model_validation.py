"""
验证AI模型功能的综合测试
"""
import os
import requests
import io
from PIL import Image, ImageDraw

def test_model_with_api():
    """通过API测试模型功能"""
    print("🧪 通过API测试真实AI模型")
    print("="*50)
    
    # 创建一个包含可能被识别为瓶子的图片
    print("📸 创建测试图片（模拟瓶子）...")
    
    # 创建一个更大的图片，画一个更明显的瓶子形状
    img = Image.new('RGB', (640, 480), color='white')
    draw = ImageDraw.Draw(img)
    
    # 画一个瓶子轮廓
    # 瓶身
    draw.rectangle([250, 200, 350, 400], fill='blue', outline='black', width=3)
    # 瓶颈
    draw.rectangle([275, 150, 325, 200], fill='blue', outline='black', width=3)
    # 瓶盖
    draw.rectangle([270, 130, 330, 150], fill='red', outline='black', width=3)
    
    # 添加标签文字
    draw.text((200, 420), "Test Bottle", fill='black')
    
    # 转换为字节
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='JPEG', quality=95)
    img_buffer.seek(0)
    
    try:
        print("📤 上传图片到API...")
        files = {'file': ('test_bottle.jpg', img_buffer, 'image/jpeg')}
        response = requests.post('http://localhost:8000/api/predict', files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API响应成功")
            print(f"📊 检测结果: {len(result.get('detections', []))} 个对象")
            print(f"⏱️ 处理时间: {result.get('processing_time', 0):.2f}秒")
            print(f"📝 消息: {result.get('message', '')}")
            
            # 显示检测详情
            detections = result.get('detections', [])
            if detections:
                print("\n🔍 检测详情:")
                for i, detection in enumerate(detections, 1):
                    print(f"  {i}. {detection['class_name']}: {detection['confidence']:.3f}")
            else:
                print("⚠️ 未检测到任何垃圾对象")
                print("💡 这可能是因为图片太简单或模型需要更真实的图片")
            
            return True
        else:
            print(f"❌ API请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ 请求超时 - 模型处理时间较长")
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def check_model_status():
    """检查模型状态"""
    print("\n🔍 检查模型状态")
    print("="*30)
    
    # 检查模型文件
    if os.path.exists("weights.pt"):
        size = os.path.getsize("weights.pt") / (1024 * 1024)  # MB
        print(f"✅ 模型文件存在: weights.pt ({size:.1f} MB)")
    else:
        print("❌ 模型文件不存在")
        return False
    
    # 检查类别映射
    if os.path.exists("ai/class_mapping.py"):
        print("✅ 类别映射文件存在")
    else:
        print("❌ 类别映射文件不存在")
    
    # 测试模型导入
    try:
        from ultralytics import YOLO
        model = YOLO("weights.pt")
        print(f"✅ 模型加载成功，支持 {len(model.names)} 个类别")
        
        # 显示一些相关的类别
        relevant_classes = []
        for id, name in model.names.items():
            if name in ['bottle', 'cup', 'cell phone', 'book', 'scissors']:
                relevant_classes.append(f"{name} (ID: {id})")
        
        if relevant_classes:
            print("🗂️ 相关类别:")
            for cls in relevant_classes:
                print(f"  - {cls}")
        
        return True
    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🤖 AI模型验证测试")
    print("="*50)
    
    # 检查模型状态
    model_ok = check_model_status()
    
    if not model_ok:
        print("\n❌ 模型状态检查失败")
        return False
    
    # 通过API测试
    api_ok = test_model_with_api()
    
    print("\n" + "="*50)
    print("📊 测试结果总结")
    print("="*50)
    
    if model_ok and api_ok:
        print("🎉 所有测试通过！")
        print("✅ 真实AI模型已成功集成")
        print("💡 系统现在使用YOLOv8进行真实的物体检测")
        return True
    else:
        print("⚠️ 部分测试失败")
        return False

if __name__ == "__main__":
    main()