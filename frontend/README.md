# 海洋垃圾检测 - Streamlit 前端

## 概述

这是海洋垃圾检测系统的 Streamlit 前端应用，提供直观的 Web 界面用于上传图片、查看检测结果、历史记录和统计分析。

## 功能特性

### 🔍 垃圾检测
- 支持 JPG、PNG、JPEG 格式图片上传
- 实时显示检测进度
- 可视化展示检测结果和置信度

### 📊 历史记录
- 分页显示历史检测记录
- 按类别筛选功能
- 统计信息展示

### 📈 统计分析
- 总体统计数据
- 垃圾类别分布图表
- 检测趋势分析

## 本地开发

### 安装依赖

```bash
cd frontend
pip install -r requirements.txt
```

### 配置后端 API

创建 `.streamlit/secrets.toml` 文件：

```toml
API_BASE_URL = "http://localhost:8000"
```

### 启动应用

```bash
streamlit run app.py
```

访问 http://localhost:8501 查看应用。

## 部署到 Streamlit Cloud

### 1. 准备部署

确保以下文件存在：
- `app.py` - 主应用文件
- `requirements.txt` - Python 依赖
- `.streamlit/config.toml` - Streamlit 配置

### 2. 创建应用

1. 访问 https://share.streamlit.io
2. 点击 "New app"
3. 选择 GitHub 仓库和分支
4. 设置主文件路径为 `frontend/app.py`

### 3. 配置密钥

在 App settings > Secrets 中添加：

```toml
API_BASE_URL = "https://your-render-app.onrender.com"
```

## 环境变量

| 变量名 | 描述 | 默认值 |
|--------|------|--------|
| `API_BASE_URL` | 后端 API 地址 | `http://localhost:8000` |

## 技术栈

- **Streamlit** - Web 应用框架
- **Requests** - HTTP 客户端
- **Pandas** - 数据处理
- **Plotly** - 数据可视化
- **Pillow** - 图像处理

## 项目结构

```
frontend/
├── app.py                 # 主应用文件
├── requirements.txt       # Python 依赖
├── .streamlit/
│   ├── config.toml       # Streamlit 配置
│   └── secrets.toml      # 密钥配置
└── README.md             # 项目说明
```

## API 接口

前端应用调用以下后端 API：

- `POST /api/predict` - 图片检测
- `GET /api/history` - 历史记录
- `GET /api/stats` - 统计数据
- `GET /api/recent` - 最近记录

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request

## 许可证

MIT License