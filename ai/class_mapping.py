# YOLOv8类别到海洋垃圾映射
YOLO_TO_TRASH_MAPPING = {'bottle': 'plastic_bottle', 'cup': 'plastic_bottle', 'cell phone': 'other_trash', 'book': 'paper', 'scissors': 'other_trash', 'teddy bear': 'other_trash', 'toothbrush': 'other_trash', 'person': None, 'bicycle': None, 'car': None, 'motorcycle': None, 'airplane': None, 'bus': None, 'train': None, 'truck': None, 'boat': None}

def map_yolo_to_trash(yolo_class_name):
    """
    将YOLO类别映射到海洋垃圾类别
    """
    return YOLO_TO_TRASH_MAPPING.get(yolo_class_name, 'other_trash')
