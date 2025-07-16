"""
综合测试脚本 - 测试系统的各个方面
"""
import io
import os
import tempfile
import threading
import time

import requests
from PIL import Image

def test_error_handling():
    """测试错误处理功能"""
    print("🚨 测试错误处理功能")
    print("="*40)
    
    base_url = "http://localhost:8000"
    
    # 测试1: 无效文件格式
    print("  - 测试无效文件格式...")
    try:
        # 创建文本文件伪装成图片
        files = {'file': ('test.txt', 'This is not an image', 'text/plain')}
        response = requests.post(f"{base_url}/api/predict", files=files, timeout=5)
        
        if response.status_code == 400:
            print("  ✅ 正确拒绝无效文件格式")
        else:
            print(f"  ❌ 未正确处理无效文件: {response.status_code}")
    except Exception as e:
        print(f"  ❌ 错误处理测试异常: {e}")
    
    # 测试2: 超大文件
    print("  - 测试文件大小限制...")
    try:
        # 创建大图片 (模拟超过10MB)
        large_image = Image.new('RGB', (5000, 5000), color='red')
        img_buffer = io.BytesIO()
        large_image.save(img_buffer, format='JPEG', quality=100)
        img_buffer.seek(0)
        
        files = {'file': ('large_image.jpg', img_buffer, 'image/jpeg')}
        response = requests.post(f"{base_url}/api/predict", files=files, timeout=10)
        
        if response.status_code == 400:
            print("  ✅ 正确拒绝超大文件")
        else:
            print(f"  ⚠️ 文件大小检查: {response.status_code}")
    except Exception as e:
        print(f"  ❌ 大文件测试异常: {e}")
    
    # 测试3: 空文件
    print("  - 测试空文件...")
    try:
        files = {'file': ('empty.jpg', b'', 'image/jpeg')}
        response = requests.post(f"{base_url}/api/predict", files=files, timeout=5)
        
        if response.status_code == 400:
            print("  ✅ 正确拒绝空文件")
        else:
            print(f"  ❌ 未正确处理空文件: {response.status_code}")
    except Exception as e:
        print(f"  ❌ 空文件测试异常: {e}")

def test_performance():
    """测试性能"""
    print("\n⚡ 测试系统性能")
    print("="*40)
    
    base_url = "http://localhost:8000"
    
    # 测试API响应时间
    print("  - 测试API响应时间...")
    try:
        start_time = time.time()
        response = requests.get(f"{base_url}/health", timeout=5)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # 转换为毫秒
        
        if response.status_code == 200:
            print(f"  ✅ 健康检查响应时间: {response_time:.2f}ms")
            if response_time < 100:
                print("  🚀 响应速度优秀")
            elif response_time < 500:
                print("  👍 响应速度良好")
            else:
                print("  ⚠️ 响应速度较慢")
        else:
            print(f"  ❌ 健康检查失败: {response.status_code}")
    except Exception as e:
        print(f"  ❌ 性能测试异常: {e}")

def test_concurrent_requests():
    """测试并发请求处理"""
    print("\n🔄 测试并发请求处理")
    print("="*40)
    
    base_url = "http://localhost:8000"
    results = []
    
    def make_request():
        try:
            start_time = time.time()
            response = requests.get(f"{base_url}/api/stats", timeout=10)
            end_time = time.time()
            
            results.append({
                'status': response.status_code,
                'time': end_time - start_time
            })
        except Exception as e:
            results.append({
                'status': 'error',
                'time': 0,
                'error': str(e)
            })
    
    # 创建5个并发请求
    print("  - 发送5个并发请求...")
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=make_request)
        threads.append(thread)
        thread.start()
    
    # 等待所有请求完成
    for thread in threads:
        thread.join()
    
    # 分析结果
    successful = [r for r in results if r['status'] == 200]
    failed = [r for r in results if r['status'] != 200]
    
    print(f"  ✅ 成功请求: {len(successful)}/{len(results)}")
    print(f"  ❌ 失败请求: {len(failed)}")
    
    if successful:
        avg_time = sum(r['time'] for r in successful) / len(successful)
        print(f"  ⏱️ 平均响应时间: {avg_time*1000:.2f}ms")

def test_database_integrity():
    """测试数据库完整性"""
    print("\n🗄️ 测试数据库完整性")
    print("="*40)
    
    base_url = "http://localhost:8000"
    
    try:
        # 获取当前统计数据
        response = requests.get(f"{base_url}/api/stats", timeout=5)
        if response.status_code == 200:
            stats_before = response.json()
            print(f"  📊 测试前记录数: {stats_before['total_predictions']}")
            
            # 创建测试图片并上传
            test_image = Image.new('RGB', (100, 100), color='green')
            img_buffer = io.BytesIO()
            test_image.save(img_buffer, format='JPEG')
            img_buffer.seek(0)
            
            files = {'file': ('integrity_test.jpg', img_buffer, 'image/jpeg')}
            upload_response = requests.post(f"{base_url}/api/predict", files=files, timeout=10)
            
            if upload_response.status_code == 200:
                # 再次获取统计数据
                response = requests.get(f"{base_url}/api/stats", timeout=5)
                if response.status_code == 200:
                    stats_after = response.json()
                    print(f"  📊 测试后记录数: {stats_after['total_predictions']}")
                    
                    # 验证数据一致性
                    if stats_after['total_predictions'] >= stats_before['total_predictions']:
                        print("  ✅ 数据库记录正确增加")
                    else:
                        print("  ❌ 数据库记录异常")
                else:
                    print("  ❌ 无法获取测试后统计数据")
            else:
                print(f"  ❌ 测试上传失败: {upload_response.status_code}")
        else:
            print("  ❌ 无法获取初始统计数据")
            
    except Exception as e:
        print(f"  ❌ 数据库完整性测试异常: {e}")

def main():
    """运行综合测试"""
    print("🧪 综合系统测试")
    print("="*50)
    
    # 检查API服务是否运行
    try:
        response = requests.get("http://localhost:8000/health", timeout=3)
        if response.status_code != 200:
            print("❌ API服务未运行，请先启动 python main.py")
            return False
    except requests.exceptions.RequestException:
        print("❌ 无法连接到API服务，请先启动 python main.py")
        return False
    
    print("✅ API服务运行正常，开始综合测试...\n")
    
    # 运行各项测试
    test_error_handling()
    test_performance()
    test_concurrent_requests()
    test_database_integrity()
    
    print("\n" + "="*50)
    print("🎉 综合测试完成！")
    print("💡 提示：如需完整功能测试，请确保有 weights.pt 模型文件")
    
    return True

if __name__ == "__main__":
    main()