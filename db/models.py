"""
数据库模型定义
"""
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Prediction(SQLModel, table=True):
    """检测记录数据模型"""
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str = Field(max_length=255, description="上传的图片文件名")
    label: str = Field(max_length=100, description="检测到的垃圾类别")
    confidence: float = Field(description="置信度分数 (0-1)")
    timestamp: datetime = Field(default_factory=datetime.now, description="检测时间")
    
    class Config:
        """模型配置"""
        json_schema_extra = {
            "example": {
                "filename": "ocean_trash_001.jpg",
                "label": "塑料瓶",
                "confidence": 0.85,
                "timestamp": "2024-01-15T10:30:00"
            }
        }


class PredictionCreate(SQLModel):
    """创建检测记录的数据模型"""
    filename: str
    label: str
    confidence: float


class PredictionRead(SQLModel):
    """读取检测记录的数据模型"""
    id: int
    filename: str
    label: str
    confidence: float
    timestamp: datetime


class PredictionStats(SQLModel):
    """统计数据模型"""
    total_predictions: int
    categories_count: dict
    avg_confidence: float
    recent_predictions: int  # 最近24小时的检测数量