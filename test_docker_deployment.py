"""
Docker部署测试脚本
"""
import requests
import time
import sys
import io
from PIL import Image

def wait_for_service(url, timeout=60):
    """等待服务启动"""
    print(f"⏳ 等待服务启动: {url}")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        try:
            response = requests.get(f"{url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ 服务已启动")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(2)
        print(".", end="", flush=True)
    
    print(f"\n❌ 服务启动超时 ({timeout}秒)")
    return False

def test_api_endpoints(base_url):
    """测试API端点"""
    print(f"\n🧪 测试API端点: {base_url}")
    
    endpoints = [
        ("/", "根路径"),
        ("/health", "健康检查"),
        ("/api/stats", "统计数据"),
        ("/api/history", "历史记录"),
    ]
    
    results = []
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"  ✅ {name}: {response.status_code}")
                results.append(True)
            else:
                print(f"  ❌ {name}: {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            results.append(False)
    
    return all(results)

def test_file_upload(base_url):
    """测试文件上传功能"""
    print(f"\n📤 测试文件上传功能")
    
    try:
        # 创建测试图片
        img = Image.new('RGB', (224, 224), color='blue')
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG')
        img_buffer.seek(0)
        
        # 上传测试
        files = {'file': ('test.jpg', img_buffer, 'image/jpeg')}
        response = requests.post(f"{base_url}/api/predict", files=files, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ 文件上传成功")
            print(f"  📊 检测结果: {len(result.get('detections', []))} 个对象")
            print(f"  ⏱️ 处理时间: {result.get('processing_time', 0):.2f}秒")
            return True
        else:
            print(f"  ❌ 文件上传失败: {response.status_code}")
            print(f"  错误信息: {response.text}")
            return False
            
    except Exception as e:
        print(f"  ❌ 文件上传测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🐳 Docker部署测试")
    print("="*50)
    
    base_url = "http://localhost:10000"
    
    # 等待服务启动
    if not wait_for_service(base_url):
        print("💡 提示：请确保Docker容器正在运行")
        print("   运行命令: docker-compose up -d")
        sys.exit(1)
    
    # 测试API端点
    api_ok = test_api_endpoints(base_url)
    
    # 测试文件上传
    upload_ok = test_file_upload(base_url)
    
    # 总结
    print("\n" + "="*50)
    print("📊 测试结果总结")
    print("="*50)
    
    if api_ok and upload_ok:
        print("🎉 所有测试通过！")
        print("✅ Docker部署成功")
        print(f"🌐 API服务地址: {base_url}")
        print(f"📖 API文档: {base_url}/docs")
        return True
    else:
        print("❌ 部分测试失败")
        print("💡 请检查Docker容器日志: docker-compose logs")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)