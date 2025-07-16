# 🐳 Docker 部署指南

## 🚀 快速开始

### 方法1: 使用自动部署脚本（推荐）

**Windows用户:**
```cmd
deploy.bat
```

**Linux/Mac用户:**
```bash
chmod +x deploy.sh
./deploy.sh
```

### 方法2: 使用 Docker Compose

```bash
# 构建并启动服务
docker-compose up -d --build

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

### 方法3: 使用 Docker 命令

```bash
# 构建镜像
docker build -t ocean-trash-detection .

# 运行容器
docker run -d \
  --name ocean-trash-api \
  -p 10000:10000 \
  -v $(pwd)/data:/app/data \
  ocean-trash-detection
```

## 🌐 访问服务

部署成功后，可以通过以下地址访问：

- **API文档**: http://localhost:10000/docs
- **健康检查**: http://localhost:10000/health
- **API根路径**: http://localhost:10000/
- **预测接口**: http://localhost:10000/api/predict
- **历史记录**: http://localhost:10000/api/history
- **统计数据**: http://localhost:10000/api/stats

## ⚙️ 环境变量配置

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `PORT` | 10000 | 服务端口 |
| `WORKERS` | 1 | Uvicorn工作进程数 |
| `PYTHONPATH` | /app | Python路径 |

## 💾 数据持久化

- **数据库文件**: 存储在 `./data` 目录
- **日志文件**: 存储在 `./logs` 目录
- **模型文件**: 自动下载到容器内

## 📊 监控和日志

```bash
# 查看容器状态
docker-compose ps

# 查看实时日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f ocean-trash-api

# 进入容器调试
docker exec -it ocean-trash-detection-api bash
```

## 🧪 测试部署

运行测试脚本验证部署：

```bash
python test_docker_deployment.py
```

## 🔧 常用命令

```bash
# 重启服务
docker-compose restart

# 重新构建并启动
docker-compose up -d --build

# 查看容器资源使用
docker stats ocean-trash-detection-api

# 清理未使用的镜像
docker system prune
```

## 🚀 生产环境部署建议

### 1. 资源配置
- **内存**: 至少 2GB，推荐 4GB
- **CPU**: 至少 1核，推荐 2核
- **存储**: 至少 10GB 可用空间

### 2. 安全配置
```yaml
# docker-compose.prod.yml
services:
  ocean-trash-api:
    environment:
      - CORS_ORIGINS=https://yourdomain.com
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2.0'
```

### 3. 反向代理配置
使用 Nginx 或 Traefik 进行反向代理和SSL终止。

### 4. 监控集成
- 集成 Prometheus 监控
- 配置 Grafana 仪表板
- 设置告警规则

## 🔍 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 检查端口使用情况
   netstat -tulpn | grep 10000
   
   # 修改端口映射
   docker-compose up -d -p 8080:10000
   ```

2. **模型下载失败**
   ```bash
   # 手动下载模型
   docker exec -it ocean-trash-detection-api python setup_model.py
   ```

3. **内存不足**
   ```bash
   # 增加内存限制
   docker-compose up -d --memory=4g
   ```

4. **权限问题**
   ```bash
   # 修复数据目录权限
   sudo chown -R $USER:$USER ./data ./logs
   ```

### 日志分析

```bash
# 查看错误日志
docker-compose logs | grep ERROR

# 查看最近的日志
docker-compose logs --tail=100

# 实时监控日志
docker-compose logs -f --tail=0
```

## 📋 系统要求

### 最低要求
- Docker 20.10+
- Docker Compose 1.29+
- 2GB RAM
- 10GB 可用磁盘空间

### 推荐配置
- Docker 24.0+
- Docker Compose 2.0+
- 4GB RAM
- 20GB 可用磁盘空间
- SSD 存储

## 🆘 获取帮助

如果遇到问题，请：

1. 检查 [故障排除](#故障排除) 部分
2. 查看容器日志: `docker-compose logs`
3. 运行测试脚本: `python test_docker_deployment.py`
4. 检查系统资源使用情况