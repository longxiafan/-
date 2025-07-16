"""
海洋垃圾检测 FastAPI 后端服务
"""
import os
import time
import tempfile
from typing import List, Optional

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlmodel import Session

from ai.inference import classify_image, validate_image
from models import PredictionResponse, ErrorResponse, Detection, CATEGORY_NAMES
from db.session import get_session, init_database
from db.models import PredictionCreate, PredictionRead, PredictionStats
from db.crud import (
    create_prediction, get_predictions,
    get_prediction_stats, get_recent_predictions
)

# 创建FastAPI应用
app = FastAPI(
    title="Ocean Trash Detection API",
    description="海洋垃圾检测API服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 应用启动时初始化数据库
@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化操作"""
    init_database()
    print("海洋垃圾检测API服务启动完成")


@app.get("/")
async def root():
    """根路径健康检查"""
    return {"message": "Ocean Trash Detection API is running"}


@app.post("/api/predict", response_model=PredictionResponse)
async def predict_trash(file: UploadFile = File(...), session: Session = Depends(get_session)):
    """
    预测上传图片中的海洋垃圾类别
    
    Args:
        file: 上传的图片文件
        session: 数据库会话
        
    Returns:
        PredictionResponse: 包含检测结果的响应
    """
    start_time = time.time()
    
    try:
        # 验证文件类型
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="文件类型错误，请上传图片文件"
            )
        
        # 验证文件大小 (10MB限制)
        MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail="文件大小超过限制（最大10MB）"
            )
        
        # 创建临时文件保存上传的图片
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        try:
            # 验证图片文件
            if not validate_image(temp_file_path):
                raise HTTPException(
                    status_code=400,
                    detail="无效的图片文件"
                )
            
            # 调用AI推理
            raw_results = classify_image(temp_file_path)
            
            # 转换结果格式并保存到数据库
            detections = []
            for class_name, confidence in raw_results:
                # 获取中文类别名称
                display_name = CATEGORY_NAMES.get(class_name, class_name)
                detections.append(Detection(
                    class_name=display_name,
                    confidence=round(confidence, 3)
                ))
                
                # 保存检测结果到数据库
                prediction_data = PredictionCreate(
                    filename=file.filename or "unknown.jpg",
                    label=display_name,
                    confidence=round(confidence, 3)
                )
                create_prediction(session, prediction_data)
            
            processing_time = time.time() - start_time
            
            return PredictionResponse(
                success=True,
                detections=detections,
                message=f"检测完成，发现 {len(detections)} 个垃圾对象",
                processing_time=round(processing_time, 3)
            )
            
        finally:
            # 清理临时文件
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except HTTPException:
        # 重新抛出HTTP异常
        raise
    except Exception as e:
        # 处理其他异常
        processing_time = time.time() - start_time
        error_msg = f"处理图片时发生错误: {str(e)}"
        
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error="internal_server_error",
                message=error_msg
            ).dict()
        )


@app.get("/api/history", response_model=List[PredictionRead])
async def get_prediction_history(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    label_filter: Optional[str] = Query(None, description="按类别筛选"),
    session: Session = Depends(get_session)
):
    """
    获取检测历史记录
    
    Args:
        skip: 跳过的记录数
        limit: 返回的记录数
        label_filter: 按类别筛选
        session: 数据库会话
        
    Returns:
        List[PredictionRead]: 检测记录列表
    """
    try:
        predictions = get_predictions(session, skip=skip, limit=limit, label_filter=label_filter)
        return [
            PredictionRead(
                id=p.id,
                filename=p.filename,
                label=p.label,
                confidence=p.confidence,
                timestamp=p.timestamp
            ) for p in predictions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取历史记录失败: {str(e)}")


@app.get("/api/stats", response_model=PredictionStats)
async def get_statistics(session: Session = Depends(get_session)):
    """
    获取检测统计数据
    
    Args:
        session: 数据库会话
        
    Returns:
        PredictionStats: 统计数据
    """
    try:
        stats = get_prediction_stats(session)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计数据失败: {str(e)}")


@app.get("/api/recent", response_model=List[PredictionRead])
async def get_recent_detections(
    limit: int = Query(10, ge=1, le=50, description="返回的记录数"),
    session: Session = Depends(get_session)
):
    """
    获取最近的检测记录
    
    Args:
        limit: 返回的记录数
        session: 数据库会话
        
    Returns:
        List[PredictionRead]: 最近的检测记录
    """
    try:
        predictions = get_recent_predictions(session, limit=limit)
        return [
            PredictionRead(
                id=p.id,
                filename=p.filename,
                label=p.label,
                confidence=p.confidence,
                timestamp=p.timestamp
            ) for p in predictions
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取最近记录失败: {str(e)}")


@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "ocean-trash-detection",
        "timestamp": time.time()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)