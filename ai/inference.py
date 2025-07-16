"""
海洋垃圾检测推理模块
"""
import os
from typing import List, Tuple
from ultralytics import YOLO
import cv2

# 默认的YOLO类别到海洋垃圾映射
DEFAULT_YOLO_MAPPING = {
    'bottle': 'plastic_bottle',
    'cup': 'plastic_bottle',
    'cell phone': 'other_trash',
    'book': 'paper',
    'scissors': 'other_trash',
    'teddy bear': 'other_trash',
    'toothbrush': 'other_trash',
}

try:
    from ai.class_mapping import map_yolo_to_trash
except ImportError:
    # 如果没有类别映射文件，使用默认映射
    def map_yolo_to_trash(yolo_class_name):
        return DEFAULT_YOLO_MAPPING.get(yolo_class_name, 'other_trash')


def classify_image(image_path: str) -> List[Tuple[str, float]]:
    """
    对图片进行垃圾分类
    
    Args:
        image_path: 图片文件路径
        
    Returns:
        List[Tuple[str, float]]: 检测结果列表，格式为 [("label", confidence), ...]
    """
    try:
        # 检查图片文件是否存在
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片文件未找到: {image_path}")
        
        # 检查模型文件
        model_path = "weights.pt"
        if not os.path.exists(model_path):
            print(f"⚠️ 模型文件未找到: {model_path}，使用模拟模式")
            # 模拟模式：返回随机检测结果用于测试
            import random
            mock_categories = ["plastic_bottle", "plastic_bag", "can", "paper"]
            detections = []
            
            # 随机生成1-3个检测结果
            num_detections = random.randint(1, 3)
            for _ in range(num_detections):
                category = random.choice(mock_categories)
                confidence = random.uniform(0.4, 0.95)  # 随机置信度
                detections.append((category, confidence))
            
            # 按置信度排序
            detections.sort(key=lambda x: x[1], reverse=True)
            return detections
            
        # 真实模式：使用YOLOv8模型
        model = YOLO(model_path)
        
        # 进行推理
        results = model(image_path)
        
        # 处理结果
        detections = []
        for result in results:
            if result.boxes is not None:
                for box in result.boxes:
                    # 获取类别和置信度
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    
                    # 获取YOLO类别名称
                    yolo_class_name = model.names[class_id] if class_id < len(model.names) else "unknown"
                    
                    # 映射到海洋垃圾类别
                    trash_category = map_yolo_to_trash(yolo_class_name)
                    
                    # 只返回置信度大于0.3且映射到垃圾类别的检测结果
                    if confidence > 0.3 and trash_category is not None:
                        detections.append((trash_category, confidence))
        
        # 按置信度排序
        detections.sort(key=lambda x: x[1], reverse=True)
        
        return detections
        
    except Exception as e:
        print(f"推理过程中发生错误: {str(e)}")
        raise RuntimeError(f"图片分类失败: {str(e)}")


def load_model(model_path: str = "weights.pt"):
    """
    预加载模型（用于优化性能）
    
    Args:
        model_path: 模型文件路径
        
    Returns:
        YOLO: 加载的模型实例
    """
    try:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"模型文件未找到: {model_path}")
            
        model = YOLO(model_path)
        print(f"模型加载成功: {model_path}")
        return model
        
    except Exception as e:
        print(f"模型加载失败: {str(e)}")
        raise RuntimeError(f"无法加载模型: {str(e)}")


def validate_image(image_path: str) -> bool:
    """
    验证图片文件是否有效
    
    Args:
        image_path: 图片文件路径
        
    Returns:
        bool: 图片是否有效
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(image_path):
            return False
            
        # 检查文件扩展名
        valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        file_ext = os.path.splitext(image_path)[1].lower()
        if file_ext not in valid_extensions:
            return False
            
        # 尝试读取图片
        image = cv2.imread(image_path)
        if image is None:
            return False
            
        return True
        
    except Exception:
        return False