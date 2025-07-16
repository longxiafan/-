"""
数据库CRUD操作
"""
from sqlmodel import Session, select, func
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from .models import Prediction, PredictionCreate, PredictionStats


def create_prediction(session: Session, prediction: PredictionCreate) -> Prediction:
    """创建新的检测记录"""
    db_prediction = Prediction(
        filename=prediction.filename,
        label=prediction.label,
        confidence=prediction.confidence
    )
    session.add(db_prediction)
    session.commit()
    session.refresh(db_prediction)
    return db_prediction


def get_prediction(session: Session, prediction_id: int) -> Optional[Prediction]:
    """根据ID获取检测记录"""
    return session.get(Prediction, prediction_id)


def get_predictions(
    session: Session,
    skip: int=0,
    limit: int=100,
    label_filter: Optional[str]=None
) -> List[Prediction]:
    """获取检测记录列表"""
    query = select(Prediction)
    
    if label_filter:
        query = query.where(Prediction.label == label_filter)
    
    query = query.offset(skip).limit(limit).order_by(Prediction.timestamp.desc())
    
    return session.exec(query).all()


def get_predictions_count(session: Session, label_filter: Optional[str]=None) -> int:
    """获取检测记录总数"""
    query = select(func.count(Prediction.id))
    
    if label_filter:
        query = query.where(Prediction.label == label_filter)
    
    return session.exec(query).first()


def get_predictions_by_date_range(
    session: Session,
    start_date: datetime,
    end_date: datetime
) -> List[Prediction]:
    """根据日期范围获取检测记录"""
    query = select(Prediction).where(
        Prediction.timestamp >= start_date,
        Prediction.timestamp <= end_date
    ).order_by(Prediction.timestamp.desc())
    
    return session.exec(query).all()


def get_category_statistics(session: Session) -> Dict[str, int]:
    """获取各类别的统计数据"""
    query = select(Prediction.label, func.count(Prediction.id)).group_by(Prediction.label)
    results = session.exec(query).all()
    
    return {label: count for label, count in results}


def get_prediction_stats(session: Session) -> PredictionStats:
    """获取综合统计数据"""
    # 总检测数量
    total_count = session.exec(select(func.count(Prediction.id))).first()
    
    # 各类别统计
    categories_count = get_category_statistics(session)
    
    # 平均置信度
    avg_confidence = session.exec(select(func.avg(Prediction.confidence))).first() or 0.0
    
    # 最近24小时的检测数量
    yesterday = datetime.now() - timedelta(days=1)
    recent_count = session.exec(
        select(func.count(Prediction.id)).where(Prediction.timestamp >= yesterday)
    ).first()
    
    return PredictionStats(
        total_predictions=total_count or 0,
        categories_count=categories_count,
        avg_confidence=round(avg_confidence, 3),
        recent_predictions=recent_count or 0
    )


def delete_prediction(session: Session, prediction_id: int) -> bool:
    """删除检测记录"""
    prediction = session.get(Prediction, prediction_id)
    if prediction:
        session.delete(prediction)
        session.commit()
        return True
    return False


def get_recent_predictions(session: Session, limit: int=10) -> List[Prediction]:
    """获取最近的检测记录"""
    query = select(Prediction).order_by(Prediction.timestamp.desc()).limit(limit)
    return session.exec(query).all()
