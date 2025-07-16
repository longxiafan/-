#!/bin/bash
set -e

echo "🌊 启动海洋垃圾检测API服务..."

# 检查模型文件
if [ ! -f "/app/weights.pt" ]; then
    echo "⚠️ 模型文件不存在，正在下载..."
    python -c "
from ultralytics import YOLO
import shutil
import os
model = YOLO('yolov8n.pt')
if os.path.exists('yolov8n.pt'):
    shutil.copy('yolov8n.pt', 'weights.pt')
    print('✅ 模型文件下载完成')
"
fi

# 初始化数据库
echo "🗄️ 初始化数据库..."
python -c "
from db.session import init_database
init_database()
print('✅ 数据库初始化完成')
"

echo "🚀 启动FastAPI服务器..."
exec "$@"