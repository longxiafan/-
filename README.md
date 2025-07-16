# 海洋垃圾检测系统 🌊

基于 YOLOv8 的海洋垃圾智能检测系统，支持图片上传和实时分类识别。

## 📋 项目概述

海洋垃圾检测系统是一个基于 Web 的应用程序，使用深度学习技术自动识别和分类海洋垃圾。系统采用前后端分离架构：

- **后端**: FastAPI + YOLOv8 AI 推理引擎
- **前端**: Streamlit Web 界面  
- **AI 模型**: YOLOv8 目标检测模型
- **数据库**: SQLite (本地) / PostgreSQL (生产)

## 🛠 环境要求

### 系统要求
- **Python**: 3.11 或更高版本
- **内存**: 至少 2GB RAM (推荐 4GB+)
- **存储**: 至少 2GB 可用空间
- **操作系统**: Windows 10+, macOS 10.15+, Ubuntu 18.04+

### 核心依赖
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
streamlit==1.28.1
ultralytics==8.0.196
opencv-python-headless==4.8.1.78
numpy==1.24.3
pillow==10.0.1
```

## 🚀 本地启动方式

### 前置准备

1. **安装 Python 3.11+**
   ```bash
   # 检查 Python 版本
   python --version
   # 或
   python3 --version
   ```

2. **克隆项目**
   ```bash
   git clone <your-repo-url>
   cd ocean-trash-detection
   ```

3. **创建虚拟环境（推荐）**
   ```bash
   # 创建虚拟环境
   python -m venv venv
   
   # 激活虚拟环境
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

### 方式一：分别启动前后端

#### 步骤 1: 准备模型文件
```bash
# 确保模型文件存在（如果没有会自动下载）
python setup_model.py
```

#### 步骤 2: 启动后端 API 服务
```bash
# 安装后端依赖
pip install -r requirements.txt

# 启动 FastAPI 服务
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**验证后端启动成功:**
- 访问 `http://localhost:8000/docs` 查看 API 文档
- 访问 `http://localhost:8000/health` 检查健康状态

#### 步骤 3: 启动前端界面（新终端窗口）
```bash
# 进入前端目录
cd frontend

# 安装前端依赖
pip install -r requirements.txt

# 配置后端 API 地址
export API_BASE_URL=http://localhost:8000  # Linux/Mac
# 或
set API_BASE_URL=http://localhost:8000     # Windows

# 启动 Streamlit 应用
streamlit run app.py --server.port 8501
```

**验证前端启动成功:**
- 访问 `http://localhost:8501` 查看 Web 界面

### 方式二：使用启动脚本

#### Windows 用户
```cmd
# 运行部署脚本
deploy.bat
```

#### Linux/Mac 用户
```bash
# 给脚本执行权限
chmod +x deploy.sh

# 运行部署脚本
./deploy.sh
```

### 方式三：一键启动（推荐）
```bash
# 安装所有依赖并启动服务
python quick_start.py
```

## 🐳 Docker 启动方式

### 单容器启动

```bash
# 构建镜像
docker build -t ocean-trash-detection .

# 运行容器
docker run -p 10000:10000 ocean-trash-detection
```

### 使用 Docker Compose

```bash
# 启动服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

服务启动后访问：`http://localhost:10000`

### Docker 环境变量

| 变量名 | 默认值 | 说明 |
|--------|--------|------|
| `PORT` | 10000 | 服务端口 |
| `PYTHONPATH` | /app | Python 路径 |
| `PYTHONUNBUFFERED` | 1 | Python 输出缓冲 |

## ☁️ 云端部署

### Render 部署 (后端 API)

#### 1. 准备部署

确保项目根目录包含以下文件：
- `render.yaml` - Render 配置文件
- `Dockerfile` - Docker 构建文件
- `requirements.txt` - Python 依赖

#### 2. 部署步骤

1. **连接 GitHub 仓库**
   - 登录 [Render](https://render.com)
   - 点击 "New +" → "Web Service"
   - 连接你的 GitHub 仓库

2. **配置服务**
   - **Name**: `ocean-trash-detection-api`
   - **Environment**: `Docker`
   - **Region**: `Oregon (US West)`
   - **Branch**: `main`
   - **Dockerfile Path**: `./Dockerfile`

3. **环境变量设置**
   ```
   PORT=10000
   PYTHONUNBUFFERED=1
   PYTHONDONTWRITEBYTECODE=1
   ```

4. **高级设置**
   - **Health Check Path**: `/health`
   - **Plan**: `Starter` (免费套餐)

#### 3. 部署后验证

部署完成后，访问分配的 URL（如：`https://your-app.onrender.com`）
- 健康检查：`GET /health`
- API 文档：`GET /docs`

### Streamlit Community Cloud 部署 (前端)

#### 1. 准备前端代码

确保 `frontend/` 目录包含：
- `app.py` - Streamlit 应用主文件
- `requirements.txt` - 前端依赖文件
- `.streamlit/config.toml` - Streamlit 配置

#### 2. 部署步骤

1. **访问 Streamlit Cloud**
   - 前往 [share.streamlit.io](https://share.streamlit.io)
   - 使用 GitHub 账号登录

2. **创建新应用**
   - 点击 "New app"
   - 选择你的 GitHub 仓库
   - **Main file path**: `frontend/app.py`
   - **Python version**: `3.11`

3. **配置环境变量**
   在 "Advanced settings" 中添加：
   ```
   API_BASE_URL=https://your-render-api.onrender.com
   ```

4. **部署配置**
   - Streamlit 会自动检测 `frontend/requirements.txt`
   - 自动应用 `.streamlit/config.toml` 配置

#### 3. 前端配置说明

`.streamlit/config.toml` 关键配置：
```toml
[server]
maxUploadSize = 10  # 最大上传文件大小 (MB)

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
```

## 🔧 配置说明

### API 配置

后端 API 主要配置项：

```python
# main.py 中的配置
app = FastAPI(
    title="Ocean Trash Detection API",
    description="海洋垃圾检测 API",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 模型配置

AI 推理模块配置：

```python
# ai/inference.py 中的配置
MODEL_PATH = "weights.pt"
CONFIDENCE_THRESHOLD = 0.5
MAX_DETECTIONS = 100
```

### 前端配置

Streamlit 应用配置：

```python
# frontend/app.py 中的配置
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
SUPPORTED_FORMATS = ["jpg", "jpeg", "png"]
```

## 📊 API 接口文档

### 主要端点

#### POST /api/predict
上传图片进行垃圾检测

**请求格式:**
```bash
curl -X POST "http://localhost:8000/api/predict" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@ocean_trash.jpg"
```

**响应格式:**
```json
{
  "success": true,
  "detections": [
    {
      "class_name": "plastic_bottle",
      "confidence": 0.85,
      "bbox": [100, 150, 200, 300]
    }
  ],
  "processing_time": 1.23,
  "message": "检测完成"
}
```

#### GET /health
健康检查端点

**响应:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## 🧪 测试

### 运行测试

```bash
# 运行所有测试
python -m pytest

# 运行特定测试
python test_api.py
python test_frontend.py
python test_system.py
```

### 测试覆盖

- **单元测试**: API 端点、AI 推理模块
- **集成测试**: 前后端完整流程
- **系统测试**: Docker 部署验证

## 🔍 故障排除

### 常见问题

#### 1. 模型文件缺失
```bash
# 错误: FileNotFoundError: weights.pt not found
# 解决: 确保模型文件存在
ls -la weights.pt
```

#### 2. 端口占用
```bash
# 错误: Port 8000 already in use
# 解决: 更换端口或停止占用进程
lsof -ti:8000 | xargs kill -9
```

#### 3. 内存不足
```bash
# 错误: CUDA out of memory
# 解决: 使用 CPU 推理或减少批处理大小
export CUDA_VISIBLE_DEVICES=""
```

#### 4. 依赖冲突
```bash
# 解决: 使用虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

### 日志查看

#### Docker 日志
```bash
# 查看容器日志
docker logs ocean-trash-detection-api

# 实时查看日志
docker logs -f ocean-trash-detection-api
```

#### 应用日志
```bash
# 后端日志
tail -f logs/api.log

# 前端日志 (Streamlit)
streamlit run app.py --logger.level debug
```

## 📈 性能优化

### 推理优化
- 使用 GPU 加速（如果可用）
- 模型量化和压缩
- 批处理推理

### 部署优化
- 启用 HTTP/2
- 配置 CDN
- 数据库连接池

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 支持

如有问题或建议，请：
- 提交 [Issue](https://github.com/your-repo/issues)
- 发送邮件至：support@example.com

---

**快速开始**: `docker-compose up -d` 然后访问 `http://localhost:10000` 🚀