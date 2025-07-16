"""
数据库模块

提供数据库连接、模型定义和CRUD操作功能
"""

from .session import get_session, init_database
from .models import Prediction, PredictionCreate, PredictionRead, PredictionStats
from .crud import (
    create_prediction,
    get_predictions,
    get_predictions_count,
    get_prediction_stats,
    get_recent_predictions
)

__all__ = [
    "get_session",
    "init_database",
    "Prediction",
    "PredictionCreate", 
    "PredictionRead",
    "PredictionStats",
    "create_prediction",
    "get_predictions",
    "get_predictions_count",
    "get_prediction_stats",
    "get_recent_predictions",
]