# Render 平台部署指南

## 概述

本指南将帮助你在 Render 平台上部署海洋垃圾检测 FastAPI 服务。Render 是一个现代化的云平台，支持自动部署和扩展。

## 前置要求

- GitHub 账户（用于代码托管）
- Render 账户（免费注册：https://render.com）
- 项目代码已推送到 GitHub 仓库

## 部署方式

### 方式一：使用 render.yaml 自动部署（推荐）

1. **准备配置文件**
   - 项目根目录已包含 `render.yaml` 配置文件
   - 该文件定义了服务的所有配置参数

2. **连接 GitHub 仓库**
   - 登录 Render Dashboard
   - 点击 "New" → "Blueprint"
   - 选择你的 GitHub 仓库
   - Render 会自动检测 `render.yaml` 文件

3. **部署配置**
   ```yaml
   # render.yaml 配置说明
   services:
     - type: web                    # Web 服务类型
       name: ocean-trash-detection-api
       env: docker                  # 使用 Docker 环境
       dockerfilePath: ./Dockerfile # Dockerfile 路径
       plan: starter               # 服务计划（免费层）
       region: oregon              # 部署区域
       healthCheckPath: /health    # 健康检查路径
   ```

### 方式二：手动创建 Web Service

1. **创建新服务**
   - 在 Render Dashboard 点击 "New" → "Web Service"
   - 连接你的 GitHub 仓库

2. **配置服务设置**
   ```
   Name: ocean-trash-detection-api
   Environment: Docker
   Region: Oregon (US West)
   Branch: main
   Dockerfile Path: ./Dockerfile
   ```

3. **环境变量设置**
   ```
   PORT=10000
   PYTHONUNBUFFERED=1
   PYTHONDONTWRITEBYTECODE=1
   ```

## 推荐配置

### 服务计划选择

| 计划类型 | 内存 | CPU | 价格 | 适用场景 |
|---------|------|-----|------|----------|
| Free | 512MB | 0.1 CPU | $0/月 | 开发测试 |
| Starter | 512MB | 0.5 CPU | $7/月 | 小型应用 |
| Standard | 2GB | 1 CPU | $25/月 | 生产环境 |

**推荐**: 
- 开发/测试: Free 计划
- 生产环境: Starter 或 Standard 计划（AI 模型需要更多内存）

### 部署区域

```
推荐区域:
- Oregon (US West) - 延迟较低
- Frankfurt (Europe) - 欧洲用户
- Singapore (Asia) - 亚洲用户
```

### 健康检查配置

```
Health Check Path: /health
Health Check Timeout: 30 seconds
Health Check Interval: 30 seconds
```

## 启动命令

Render 会自动使用 Dockerfile 中的 CMD 指令：

```dockerfile
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1"]
```

如需自定义启动命令，可在 Render Dashboard 中设置：

```bash
# 基本启动命令
uvicorn main:app --host 0.0.0.0 --port $PORT

# 生产环境启动命令（多进程）
uvicorn main:app --host 0.0.0.0 --port $PORT --workers 2

# 带日志级别的启动命令
uvicorn main:app --host 0.0.0.0 --port $PORT --log-level info
```

## 环境变量配置

### 必需环境变量

```bash
PORT=10000                    # 服务端口（Render 自动设置）
PYTHONUNBUFFERED=1           # Python 输出缓冲
PYTHONDONTWRITEBYTECODE=1    # 禁用 .pyc 文件
```

### 可选环境变量

```bash
# 数据库配置（如使用外部数据库）
DATABASE_URL=sqlite:///./ocean_trash_detection.db

# AI 模型配置
MODEL_CONFIDENCE_THRESHOLD=0.5
MODEL_PATH=weights.pt

# 日志配置
LOG_LEVEL=info
```

## 持久化存储

### 磁盘挂载配置

```yaml
disk:
  name: ocean-trash-data
  mountPath: /app/data
  sizeGB: 1
```

用途：
- 存储 SQLite 数据库文件
- 缓存 AI 模型文件
- 保存上传的图片（如需要）

## 部署流程

### 1. 准备代码

```bash
# 确保代码已推送到 GitHub
git add .
git commit -m "准备 Render 部署"
git push origin main
```

### 2. 创建服务

- 访问 [Render Dashboard](https://dashboard.render.com)
- 选择部署方式（Blueprint 或 Web Service）
- 连接 GitHub 仓库

### 3. 配置服务

- 设置服务名称和环境变量
- 选择合适的服务计划
- 配置健康检查

### 4. 部署验证

部署完成后，访问以下端点验证：

```bash
# 健康检查
curl https://your-app.onrender.com/health

# API 根路径
curl https://your-app.onrender.com/

# 测试预测接口（需要图片文件）
curl -X POST https://your-app.onrender.com/api/predict \
  -F "file=@test_image.jpg"
```

## 监控和日志

### 查看日志

1. 在 Render Dashboard 中选择你的服务
2. 点击 "Logs" 标签页
3. 实时查看应用日志

### 监控指标

Render 提供以下监控指标：
- CPU 使用率
- 内存使用率
- 响应时间
- 错误率
- 请求量

## 自动部署

### GitHub 集成

Render 支持自动部署：
- 推送到 `main` 分支时自动部署
- 支持预览部署（Pull Request）
- 部署状态通知

### 部署钩子

```bash
# 部署前钩子（在 Dockerfile 中）
RUN python setup_model.py

# 部署后验证
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:10000/health || exit 1
```

## 故障排除

### 常见问题

1. **内存不足**
   ```
   解决方案: 升级到更高的服务计划
   或优化模型加载方式
   ```

2. **启动超时**
   ```
   解决方案: 增加健康检查超时时间
   或优化应用启动速度
   ```

3. **模型下载失败**
   ```
   解决方案: 检查网络连接
   或预先上传模型文件
   ```

### 调试命令

```bash
# 查看容器状态
docker ps

# 查看应用日志
docker logs <container_id>

# 进入容器调试
docker exec -it <container_id> /bin/bash
```

## 成本优化

### 免费层限制

- 750 小时/月的运行时间
- 服务在无活动时会休眠
- 冷启动时间较长

### 优化建议

1. **使用 Starter 计划**避免休眠
2. **优化 Docker 镜像**减少构建时间
3. **实现缓存机制**提高响应速度
4. **监控资源使用**避免超额费用

## 安全配置

### HTTPS

Render 自动提供 HTTPS 证书，无需额外配置。

### 环境变量安全

```bash
# 敏感信息使用环境变量
API_KEY=your_secret_key
DATABASE_PASSWORD=your_db_password
```

### CORS 配置

```python
# 生产环境中限制 CORS 域名
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 扩展和维护

### 水平扩展

Render 支持自动扩展：
- 基于 CPU/内存使用率
- 基于请求量
- 手动调整实例数量

### 版本管理

```bash
# 使用 Git 标签管理版本
git tag v1.0.0
git push origin v1.0.0

# 在 Render 中部署特定版本
# Dashboard → Settings → Branch: v1.0.0
```

### 备份策略

1. **代码备份**: GitHub 仓库
2. **数据备份**: 定期下载数据库文件
3. **配置备份**: 导出 render.yaml 配置

## 总结

通过以上配置，你的海洋垃圾检测 API 服务将在 Render 平台上稳定运行。记住：

✅ 使用 `render.yaml` 进行自动化部署  
✅ 选择合适的服务计划  
✅ 配置健康检查和监控  
✅ 设置持久化存储  
✅ 实施安全最佳实践  

部署完成后，你将获得一个可公开访问的 API 端点，支持海洋垃圾图片的智能识别和分类。