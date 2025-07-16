"""
API响应模型定义
"""
from pydantic import BaseModel
from typing import List, Dict, Optional


class Detection(BaseModel):
    """检测结果模型"""
    class_name: str
    confidence: float


class PredictionResponse(BaseModel):
    """预测响应模型"""
    success: bool
    detections: List[Detection]
    message: str = ""
    processing_time: float


class ErrorResponse(BaseModel):
    """错误响应模型"""
    success: bool = False
    error: str
    message: str


# 垃圾类别中英文对照
CATEGORY_NAMES = {
    "plastic_bottle": "塑料瓶",
    "plastic_bag": "塑料袋",
    "can": "罐头",
    "paper": "纸张",
    "glass_bottle": "玻璃瓶",
    "other_trash": "其他垃圾"
}