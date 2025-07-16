# Streamlit Cloud 部署指南

## 概述

本指南将帮助你在 Streamlit Cloud 平台上部署海洋垃圾检测前端应用，并确保它能正确连接到 Render 后端 API 服务。

## 前置要求

- GitHub 账户（用于代码托管）
- Streamlit Cloud 账户（免费注册：https://share.streamlit.io）
- Render 后端 API 已部署并运行

## 项目结构

```
frontend/
├── app.py                    # 主应用文件
├── requirements.txt          # Python 依赖
├── .streamlit/
│   ├── config.toml          # Streamlit 配置
│   └── secrets.toml         # 密钥配置（本地开发用）
└── README.md                # 应用说明
```

## 部署步骤

### 1. 准备代码

确保你的前端代码已经推送到 GitHub 仓库：

```bash
# 进入前端目录
cd frontend

# 添加并提交更改
git add .
git commit -m "准备 Streamlit Cloud 部署"
git push origin main
```

### 2. 创建 Streamlit Cloud 应用

1. **访问 Streamlit Cloud**
   - 登录 https://share.streamlit.io
   - 点击 "New app"

2. **连接 GitHub 仓库**
   ```
   Repository: your-username/ocean-trash-detection
   Branch: main
   Main file path: frontend/app.py
   ```

3. **配置应用设置**
   ```
   App name: ocean-trash-detection-frontend
   App URL: https://ocean-trash-detection.streamlit.app
   ```

### 3. 配置环境变量

在 Streamlit Cloud 的 App settings > Secrets 中添加以下配置：

```toml
# API 后端 URL - 替换为你的 Render 后端 URL
API_BASE_URL = "https://your-render-app.onrender.com"

# 可选配置
MAX_UPLOAD_SIZE = 10
TIMEOUT_SECONDS = 30
```

**重要**: 将 `your-render-app` 替换为你实际的 Render 应用名称。

### 4. 部署验证

部署完成后，验证以下功能：

1. **应用访问**: 访问你的 Streamlit 应用 URL
2. **页面加载**: 确保所有页面正常显示
3. **API 连接**: 测试图片上传和检测功能
4. **数据展示**: 验证历史记录和统计分析页面

## 配置文件说明

### requirements.txt

```txt
# Streamlit前端专用依赖
streamlit==1.28.1
requests==2.31.0
plotly==5.17.0
pandas==2.1.1
pillow==10.0.1
```

### .streamlit/config.toml

```toml
[global]
developmentMode = false

[server]
headless = true
enableCORS = false
enableXsrfProtection = false
maxUploadSize = 10

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### API 连接配置

前端应用使用以下逻辑连接后端：

```python
# API基础URL - 支持本地开发和生产环境
import os
API_BASE_URL = os.getenv("API_BASE_URL", st.secrets.get("API_BASE_URL", "http://localhost:8000"))
```

这种配置方式支持：
- **本地开发**: 使用 `http://localhost:8000`
- **生产环境**: 使用 Streamlit secrets 中的 `API_BASE_URL`
- **环境变量**: 支持通过环境变量覆盖

## 后端 API 端点

前端应用会调用以下后端 API：

| 端点 | 方法 | 用途 |
|------|------|------|
| `/api/predict` | POST | 图片检测预测 |
| `/api/history` | GET | 获取检测历史 |
| `/api/stats` | GET | 获取统计数据 |
| `/api/recent` | GET | 获取最近记录 |
| `/health` | GET | 健康检查 |

## CORS 配置

确保你的 Render 后端 API 允许来自 Streamlit Cloud 的跨域请求：

```python
# 在 main.py 中配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://*.streamlit.app",  # 允许所有 Streamlit 应用
        "https://your-app.streamlit.app",  # 或指定具体域名
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

## 功能特性

### 🔍 垃圾检测页面

- **文件上传**: 支持 JPG、PNG、JPEG 格式
- **实时预览**: 显示上传的图片和基本信息
- **进度指示**: 显示处理进度和状态
- **结果展示**: 表格和图表形式展示检测结果

### 📊 历史记录页面

- **数据筛选**: 按类别、页码筛选记录
- **分页显示**: 支持自定义每页显示数量
- **统计信息**: 显示当前页面的统计数据
- **时间格式**: 友好的时间显示格式

### 📈 统计分析页面

- **总体统计**: 显示系统整体使用情况
- **类别分布**: 饼图和柱状图展示垃圾类别分布
- **趋势分析**: 时间序列图显示检测趋势
- **最近记录**: 展示最新的检测记录

## 性能优化

### 缓存配置

```python
# 使用 Streamlit 缓存优化性能
@st.cache_data(ttl=300)  # 缓存 5 分钟
def get_stats_data():
    response = requests.get(f"{API_BASE_URL}/api/stats")
    return response.json()

@st.cache_data(ttl=60)   # 缓存 1 分钟
def get_recent_data(limit=20):
    response = requests.get(f"{API_BASE_URL}/api/recent", params={"limit": limit})
    return response.json()
```

### 图片处理优化

```python
# 优化图片显示
def optimize_image_display(image, max_width=800):
    if image.width > max_width:
        ratio = max_width / image.width
        new_height = int(image.height * ratio)
        image = image.resize((max_width, new_height))
    return image
```

## 错误处理

### 网络连接错误

```python
try:
    response = requests.post(api_url, files={"file": uploaded_file}, timeout=30)
except requests.exceptions.ConnectionError:
    st.error("❌ 无法连接到后端服务，请稍后重试")
except requests.exceptions.Timeout:
    st.error("❌ 请求超时，请检查网络连接")
except Exception as e:
    st.error(f"❌ 发生未知错误：{str(e)}")
```

### API 响应错误

```python
if response.status_code == 200:
    result = response.json()
    # 处理成功响应
elif response.status_code == 400:
    st.error("❌ 请求参数错误，请检查上传的文件")
elif response.status_code == 500:
    st.error("❌ 服务器内部错误，请稍后重试")
else:
    st.error(f"❌ API请求失败：HTTP {response.status_code}")
```

## 监控和调试

### 应用日志

Streamlit Cloud 提供应用日志查看功能：
1. 在应用管理页面点击 "Manage app"
2. 查看 "Logs" 标签页
3. 实时监控应用运行状态

### 性能监控

```python
# 添加性能监控
import time

def monitor_api_call(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        st.sidebar.metric("API 响应时间", f"{end_time - start_time:.2f}s")
        return result
    return wrapper
```

## 故障排除

### 常见问题

1. **API 连接失败**
   ```
   检查项:
   - Render 后端服务是否正常运行
   - API_BASE_URL 是否配置正确
   - CORS 设置是否允许 Streamlit 域名
   ```

2. **文件上传失败**
   ```
   检查项:
   - 文件大小是否超过 10MB 限制
   - 文件格式是否为支持的图片格式
   - 网络连接是否稳定
   ```

3. **页面加载缓慢**
   ```
   优化方案:
   - 启用 Streamlit 缓存
   - 优化图片显示尺寸
   - 减少不必要的 API 调用
   ```

### 调试技巧

```python
# 添加调试信息
if st.sidebar.checkbox("显示调试信息"):
    st.sidebar.write(f"API URL: {API_BASE_URL}")
    st.sidebar.write(f"当前页面: {page}")
    
    # 显示 API 响应
    if 'response' in locals():
        st.sidebar.json(response.json())
```

## 安全考虑

### 敏感信息保护

- 使用 Streamlit secrets 存储 API URL
- 不在代码中硬编码敏感信息
- 定期更新依赖包版本

### 输入验证

```python
# 文件类型验证
def validate_uploaded_file(file):
    if file is None:
        return False, "请选择文件"
    
    if file.size > 10 * 1024 * 1024:  # 10MB
        return False, "文件大小超过 10MB 限制"
    
    if file.type not in ['image/jpeg', 'image/png', 'image/jpg']:
        return False, "不支持的文件格式"
    
    return True, "文件验证通过"
```

## 部署清单

部署前请确认以下项目：

- [ ] 代码已推送到 GitHub
- [ ] requirements.txt 包含所有依赖
- [ ] .streamlit/config.toml 配置正确
- [ ] Render 后端 API 正常运行
- [ ] Streamlit secrets 配置了正确的 API_BASE_URL
- [ ] CORS 设置允许 Streamlit 域名访问
- [ ] 所有页面功能测试通过

## 总结

通过以上配置，你的海洋垃圾检测前端应用将在 Streamlit Cloud 上稳定运行，并能够：

✅ **无缝连接** Render 后端 API  
✅ **实时检测** 海洋垃圾图片  
✅ **数据可视化** 检测结果和统计信息  
✅ **响应式设计** 适配不同设备  
✅ **错误处理** 提供友好的用户体验  

部署完成后，用户可以通过 `https://your-app.streamlit.app` 访问完整的海洋垃圾检测系统。