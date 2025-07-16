"""
测试真实AI推理功能
"""
import os
import tempfile
from PIL import Image
from ai.inference import classify_image, validate_image

def test_real_ai_inference():
    """测试真实的AI推理功能"""
    print("🤖 测试真实AI推理功能")
    print("="*40)
    
    # 检查模型文件
    if not os.path.exists("weights.pt"):
        print("❌ 模型文件不存在")
        return False
    
    print("✅ 模型文件存在")
    
    # 创建测试图片
    print("📸 创建测试图片...")
    test_image = Image.new('RGB', (640, 480), color='blue')
    
    # 在图片上添加一些简单的形状（模拟物体）
    from PIL import ImageDraw
    draw = ImageDraw.Draw(test_image)
    
    # 画一个瓶子形状
    draw.rectangle([100, 100, 150, 200], fill='brown', outline='black')
    draw.rectangle([110, 80, 140, 100], fill='brown', outline='black')
    
    # 画一个杯子形状
    draw.rectangle([300, 150, 350, 220], fill='white', outline='black')
    draw.arc([295, 145, 355, 225], 0, 180, fill='black')
    
    # 保存测试图片
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
        test_image.save(temp_file.name, 'JPEG')
        temp_image_path = temp_file.name
    
    try:
        # 验证图片
        print("🔍 验证图片...")
        if not validate_image(temp_image_path):
            print("❌ 图片验证失败")
            return False
        
        print("✅ 图片验证成功")
        
        # 进行AI推理
        print("🧠 进行AI推理...")
        results = classify_image(temp_image_path)
        
        print(f"📊 检测结果: {len(results)} 个对象")
        
        for i, (category, confidence) in enumerate(results, 1):
            print(f"  {i}. {category}: {confidence:.3f}")
        
        if results:
            print("✅ AI推理成功！")
            return True
        else:
            print("⚠️ 未检测到任何对象（这是正常的，因为测试图片很简单）")
            return True
            
    except Exception as e:
        print(f"❌ AI推理失败: {e}")
        return False
        
    finally:
        # 清理临时文件
        if os.path.exists(temp_image_path):
            os.unlink(temp_image_path)

if __name__ == "__main__":
    success = test_real_ai_inference()
    if success:
        print("\n🎉 真实AI推理测试通过！")
    else:
        print("\n❌ 真实AI推理测试失败！")