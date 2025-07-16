"""
海洋垃圾检测 Streamlit 前端应用
"""
import os
import io
from datetime import datetime, timedelta

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from PIL import Image

# 页面配置
st.set_page_config(
    page_title="海洋垃圾检测系统",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API基础URL - 支持本地开发和生产环境
API_BASE_URL = os.getenv("API_BASE_URL", st.secrets.get("API_BASE_URL", "http://localhost:8000"))

# 应用标题和描述
st.title("🌊 海洋垃圾检测系统")
st.markdown("""
### 上传海洋垃圾照片，AI智能识别垃圾类别
使用先进的YOLOv8深度学习模型，快速准确地识别海洋中的各类垃圾，助力海洋环保事业。
""")

# 侧边栏导航
with st.sidebar:
    st.header("🧭 导航菜单")
    page = st.selectbox(
        "选择页面",
        ["🔍 垃圾检测", "📊 历史记录", "📈 统计分析"],
        index=0
    )
    
    st.header("ℹ️ 系统信息")
    st.info("""
    **支持的垃圾类别：**
    - 🍶 塑料瓶
    - 🛍️ 塑料袋  
    - 🥫 罐头
    - 📄 纸张
    - 🍾 玻璃瓶
    - 🗑️ 其他垃圾
    """)
    
    if page == "🔍 垃圾检测":
        st.header("📋 使用说明")
        st.markdown("""
        1. 点击下方上传按钮选择图片
        2. 支持 JPG、PNG、JPEG 格式
        3. 文件大小不超过 10MB
        4. 等待AI分析完成
        5. 查看检测结果和置信度
        """)

# 根据选择的页面显示不同内容
if page == "🔍 垃圾检测":
    # 垃圾检测页面
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📤 上传图片")
        
        # 文件上传控件
        uploaded_file = st.file_uploader(
            "选择海洋垃圾图片",
            type=['jpg', 'jpeg', 'png'],
            help="支持JPG、PNG、JPEG格式，最大10MB"
        )
        
        # 显示上传的图片
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption="上传的图片", use_column_width=True)
                
                # 显示图片信息
                st.info(f"""
                **图片信息：**
                - 文件名：{uploaded_file.name}
                - 文件大小：{len(uploaded_file.getvalue()) / 1024:.1f} KB
                - 图片尺寸：{image.size[0]} × {image.size[1]}
                """)
                
            except Exception as e:
                st.error(f"无法显示图片：{str(e)}")

    with col2:
        st.header("🔍 检测结果")
        
        if uploaded_file is not None:
            # 分析按钮
            if st.button("🚀 开始分析", type="primary", use_container_width=True):
                
                # 显示进度条
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # 更新进度
                    progress_bar.progress(25)
                    status_text.text("正在上传图片...")
                    
                    # 准备API请求
                    api_url = f"{API_BASE_URL}/api/predict"
                    files = {"file": uploaded_file.getvalue()}
                    
                    progress_bar.progress(50)
                    status_text.text("正在进行AI分析...")
                    
                    # 发送请求到后端API
                    response = requests.post(api_url, files={"file": uploaded_file}, timeout=30)
                    
                    progress_bar.progress(75)
                    status_text.text("正在处理结果...")
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        progress_bar.progress(100)
                        status_text.text("分析完成！")
                        
                        # 显示结果
                        if result["success"] and result["detections"]:
                            st.success(f"✅ {result['message']}")
                            st.info(f"⏱️ 处理时间：{result['processing_time']:.2f} 秒")
                            
                            # 创建结果数据框
                            detections_data = []
                            for detection in result["detections"]:
                                detections_data.append({
                                    "垃圾类别": detection["class_name"],
                                    "置信度": detection["confidence"],
                                    "置信度百分比": f"{detection['confidence']*100:.1f}%"
                                })
                            
                            df = pd.DataFrame(detections_data)
                            
                            # 显示检测结果表格
                            st.subheader("📊 检测详情")
                            st.dataframe(df, use_container_width=True, hide_index=True)
                            
                            # 显示置信度条形图
                            if len(detections_data) > 0:
                                st.subheader("📈 置信度可视化")
                                fig = px.bar(
                                    df, 
                                    x="垃圾类别", 
                                    y="置信度",
                                    title="各类垃圾检测置信度",
                                    color="置信度",
                                    color_continuous_scale="viridis"
                                )
                                fig.update_layout(
                                    xaxis_title="垃圾类别",
                                    yaxis_title="置信度",
                                    showlegend=False
                                )
                                st.plotly_chart(fig, use_container_width=True)
                        
                        elif result["success"] and not result["detections"]:
                            st.warning("🤔 未检测到海洋垃圾，请尝试上传其他图片")
                        
                        else:
                            st.error(f"❌ 检测失败：{result.get('message', '未知错误')}")
                    
                    else:
                        st.error(f"❌ API请求失败：HTTP {response.status_code}")
                        if response.text:
                            st.error(f"错误详情：{response.text}")
                            
                except requests.exceptions.ConnectionError:
                    st.error("❌ 无法连接到后端服务，请确保API服务正在运行")
                except Exception as e:
                    st.error(f"❌ 发生未知错误：{str(e)}")
                finally:
                    # 清理进度显示
                    progress_bar.empty()
                    status_text.empty()
        
        else:
            st.info("👆 请先上传一张海洋垃圾图片")

elif page == "📊 历史记录":
    # 历史记录页面
    st.header("📊 检测历史记录")
    
    # 筛选选项
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        category_filter = st.selectbox(
            "按类别筛选",
            ["全部", "塑料瓶", "塑料袋", "罐头", "纸张", "玻璃瓶", "其他垃圾"]
        )
    
    with col2:
        records_per_page = st.selectbox(
            "每页显示",
            [10, 20, 50, 100],
            index=1
        )
    
    with col3:
        page_number = st.number_input(
            "页码",
            min_value=1,
            value=1
        )
    
    # 获取历史记录
    try:
        params = {
            "skip": (page_number - 1) * records_per_page,
            "limit": records_per_page
        }
        
        if category_filter != "全部":
            params["label_filter"] = category_filter
        
        response = requests.get(f"{API_BASE_URL}/api/history", params=params)
        
        if response.status_code == 200:
            history_data = response.json()
            
            if history_data:
                # 转换为DataFrame
                df = pd.DataFrame(history_data)
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['日期时间'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
                
                # 显示数据表格
                display_df = df[['filename', 'label', 'confidence', '日期时间']].copy()
                display_df.columns = ['文件名', '垃圾类别', '置信度', '检测时间']
                display_df['置信度'] = display_df['置信度'].round(3)
                
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # 显示统计信息
                st.subheader("📈 本页统计")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("记录数量", len(df))
                
                with col2:
                    st.metric("平均置信度", f"{df['confidence'].mean():.3f}")
                
                with col3:
                    st.metric("最高置信度", f"{df['confidence'].max():.3f}")
                
                with col4:
                    st.metric("最低置信度", f"{df['confidence'].min():.3f}")
                
            else:
                st.info("📝 暂无历史记录")
                
        else:
            st.error(f"❌ 获取历史记录失败：HTTP {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("❌ 无法连接到后端服务")
    except Exception as e:
        st.error(f"❌ 发生错误：{str(e)}")

elif page == "📈 统计分析":
    # 统计分析页面
    st.header("📈 统计分析")
    
    try:
        # 获取统计数据
        stats_response = requests.get(f"{API_BASE_URL}/api/stats")
        recent_response = requests.get(f"{API_BASE_URL}/api/recent", params={"limit": 20})
        
        if stats_response.status_code == 200:
            stats = stats_response.json()
            
            # 总体统计
            st.subheader("📊 总体统计")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("总检测次数", stats["total_predictions"])
            
            with col2:
                st.metric("平均置信度", f"{stats['avg_confidence']:.3f}")
            
            with col3:
                st.metric("检测类别数", len(stats["categories_count"]))
            
            with col4:
                st.metric("最近24小时", stats["recent_predictions"])
            
            # 类别分布图
            if stats["categories_count"]:
                st.subheader("🗂️ 垃圾类别分布")
                
                categories_df = pd.DataFrame(
                    list(stats["categories_count"].items()),
                    columns=["类别", "数量"]
                )
                
                # 饼图
                col1, col2 = st.columns(2)
                
                with col1:
                    fig_pie = px.pie(
                        categories_df,
                        values="数量",
                        names="类别",
                        title="类别分布饼图"
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with col2:
                    fig_bar = px.bar(
                        categories_df,
                        x="类别",
                        y="数量",
                        title="类别分布柱状图",
                        color="数量",
                        color_continuous_scale="viridis"
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
            
            # 最近检测记录
            if recent_response.status_code == 200:
                recent_data = recent_response.json()
                
                if recent_data:
                    st.subheader("🕒 最近检测记录")
                    
                    recent_df = pd.DataFrame(recent_data)
                    recent_df['timestamp'] = pd.to_datetime(recent_df['timestamp'])
                    recent_df['日期时间'] = recent_df['timestamp'].dt.strftime('%m-%d %H:%M')
                    
                    # 时间趋势图
                    fig_timeline = px.scatter(
                        recent_df,
                        x='timestamp',
                        y='confidence',
                        color='label',
                        title="最近检测置信度趋势",
                        hover_data=['filename']
                    )
                    fig_timeline.update_layout(
                        xaxis_title="时间",
                        yaxis_title="置信度"
                    )
                    st.plotly_chart(fig_timeline, use_container_width=True)
                    
                    # 最近记录表格
                    display_recent = recent_df[['filename', 'label', 'confidence', '日期时间']].copy()
                    display_recent.columns = ['文件名', '垃圾类别', '置信度', '检测时间']
                    display_recent['置信度'] = display_recent['置信度'].round(3)
                    
                    st.dataframe(display_recent.head(10), use_container_width=True, hide_index=True)
        
        else:
            st.error(f"❌ 获取统计数据失败：HTTP {stats_response.status_code}")
            
    except requests.exceptions.ConnectionError:
        st.error("❌ 无法连接到后端服务")
    except Exception as e:
        st.error(f"❌ 发生错误：{str(e)}")

# 页脚
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌊 海洋垃圾检测系统 | 基于 YOLOv8 深度学习模型 | 助力海洋环保 🌍</p>
</div>
""", unsafe_allow_html=True)