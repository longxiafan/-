#!/bin/bash

# 海洋垃圾检测系统部署脚本

set -e

echo "🌊 海洋垃圾检测系统 Docker 部署"
echo "=================================="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    echo "📥 安装指南: https://docs.docker.com/get-docker/"
    exit 1
fi

# 检查docker-compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose 未安装，请先安装 docker-compose"
    echo "📥 安装指南: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker 环境检查通过"

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p data logs

# 停止现有容器
echo "🛑 停止现有容器..."
docker-compose down 2>/dev/null || true

# 构建并启动服务
echo "🔨 构建并启动服务..."
docker-compose up -d --build

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 15

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose ps

# 显示日志
echo "📋 显示启动日志..."
docker-compose logs --tail=20

echo ""
echo "🎉 部署完成！"
echo "=================================="
echo "🌐 API服务: http://localhost:10000"
echo "📖 API文档: http://localhost:10000/docs"
echo "❤️ 健康检查: http://localhost:10000/health"
echo ""
echo "💡 常用命令:"
echo "  查看日志: docker-compose logs -f"
echo "  停止服务: docker-compose down"
echo "  重启服务: docker-compose restart"
echo "  进入容器: docker exec -it ocean-trash-detection-api bash"
echo ""

# 测试API是否可访问
echo "🧪 测试API连接..."
sleep 5
if curl -s http://localhost:10000/health > /dev/null; then
    echo "✅ API服务正常运行"
else
    echo "⚠️ API服务可能还在启动中，请稍后访问"
fi

echo ""