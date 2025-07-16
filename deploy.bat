@echo off
chcp 65001 >nul
echo 🌊 海洋垃圾检测系统 Docker 部署
echo ==================================

REM 检查Docker是否安装
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker 未安装，请先安装 Docker Desktop
    echo 📥 下载地址: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✅ Docker 环境检查通过

REM 创建必要的目录
echo 📁 创建必要的目录...
if not exist "data" mkdir data
if not exist "logs" mkdir logs

REM 停止现有容器
echo 🛑 停止现有容器...
docker-compose down 2>nul

REM 构建并启动服务
echo 🔨 构建并启动服务...
docker-compose up -d --build

if %errorlevel% neq 0 (
    echo ❌ 构建失败
    pause
    exit /b 1
)

REM 等待服务启动
echo ⏳ 等待服务启动...
timeout /t 15 /nobreak >nul

REM 检查服务状态
echo 🔍 检查服务状态...
docker-compose ps

REM 显示日志
echo 📋 显示启动日志...
docker-compose logs --tail=20

echo.
echo 🎉 部署完成！
echo ==================================
echo 🌐 API服务: http://localhost:10000
echo 📖 API文档: http://localhost:10000/docs
echo ❤️ 健康检查: http://localhost:10000/health
echo.
echo 💡 常用命令:
echo   查看日志: docker-compose logs -f
echo   停止服务: docker-compose down
echo   重启服务: docker-compose restart
echo   进入容器: docker exec -it ocean-trash-detection-api bash
echo.

REM 测试API是否可访问
echo 🧪 测试API连接...
timeout /t 5 /nobreak >nul
curl -s http://localhost:10000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ API服务正常运行
) else (
    echo ⚠️ API服务可能还在启动中，请稍后访问
)

echo.
pause