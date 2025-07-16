"""
设置YOLOv8模型脚本
"""
import os
from ultralytics import YOLO

def download_yolo_model():
    """
    下载并设置YOLOv8模型
    """
    print("🤖 开始设置YOLOv8模型...")
    
    try:
        # 下载YOLOv8n模型（最小版本，适合测试）
        print("📥 下载YOLOv8n模型...")
        model = YOLO('yolov8n.pt')
        
        # 将模型保存为weights.pt
        model_path = "weights.pt"
        print(f"💾 保存模型到: {model_path}")
        
        # 复制模型文件
        import shutil
        if os.path.exists('yolov8n.pt'):
            shutil.copy('yolov8n.pt', model_path)
            print(f"✅ 模型文件已保存: {model_path}")
        
        # 测试模型加载
        print("🧪 测试模型加载...")
        test_model = YOLO(model_path)
        print(f"✅ 模型加载成功！支持的类别数: {len(test_model.names)}")
        
        # 显示支持的类别
        print("\n📋 YOLO模型支持的类别:")
        for i, name in test_model.names.items():
            print(f"  {i}: {name}")
        
        return True
        
    except Exception as e:
        print(f"❌ 模型设置失败: {e}")
        return False

def create_custom_model_mapping():
    """
    创建自定义的海洋垃圾类别映射
    """
    print("\n🗂️ 创建海洋垃圾类别映射...")
    
    # YOLO的通用类别到海洋垃圾的映射
    yolo_to_trash_mapping = {
        'bottle': 'plastic_bottle',
        'cup': 'plastic_bottle', 
        'cell phone': 'other_trash',
        'book': 'paper',
        'scissors': 'other_trash',
        'teddy bear': 'other_trash',
        'toothbrush': 'other_trash',
        'person': None,  # 忽略人物
        'bicycle': None,  # 忽略非垃圾物品
        'car': None,
        'motorcycle': None,
        'airplane': None,
        'bus': None,
        'train': None,
        'truck': None,
        'boat': None,
    }
    
    mapping_content = f"""# YOLOv8类别到海洋垃圾映射
YOLO_TO_TRASH_MAPPING = {yolo_to_trash_mapping}

def map_yolo_to_trash(yolo_class_name):
    \"\"\"
    将YOLO类别映射到海洋垃圾类别
    \"\"\"
    return YOLO_TO_TRASH_MAPPING.get(yolo_class_name, 'other_trash')
"""
    
    with open('ai/class_mapping.py', 'w', encoding='utf-8') as f:
        f.write(mapping_content)
    
    print("✅ 类别映射文件已创建: ai/class_mapping.py")

if __name__ == "__main__":
    print("🌊 海洋垃圾检测模型设置")
    print("="*50)
    
    success = download_yolo_model()
    
    if success:
        create_custom_model_mapping()
        print("\n🎉 模型设置完成！")
        print("💡 现在可以使用真实的YOLOv8模型进行检测了")
        print("⚠️ 注意：这是通用模型，检测效果可能不如专门训练的海洋垃圾模型")
    else:
        print("\n❌ 模型设置失败")
        print("💡 系统将继续使用模拟模式")