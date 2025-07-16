"""
文件上传功能测试
"""
import io

import requests
from PIL import Image

def test_file_upload():
    """
    测试文件上传到API的功能
    
    Returns:
        bool: 测试是否成功
    """
    print("📤 测试文件上传功能")
    print("="*40)
    
    # 创建测试图片
    print("  - 创建测试图片...")
    test_image = Image.new('RGB', (224, 224), color='blue')
    
    # 将图片保存到内存
    img_buffer = io.BytesIO()
    test_image.save(img_buffer, format='JPEG')
    img_buffer.seek(0)
    
    try:
        # 测试文件上传到API
        print("  - 测试上传到 /api/predict...")
        files = {'file': ('test_image.jpg', img_buffer, 'image/jpeg')}
        
        response = requests.post(
            'http://localhost:8000/api/predict',
            files=files,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"  ✅ 文件上传成功: {response.status_code}")
            print(f"  📊 检测结果: {len(result.get('detections', []))} 个对象")
            print(f"  ⏱️ 处理时间: {result.get('processing_time', 0):.2f}秒")
            return True
        else:
            print(f"  ❌ 文件上传失败: {response.status_code}")
            print(f"  错误信息: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("  ❌ 无法连接到API服务器，请确保服务正在运行")
        return False
    except requests.exceptions.Timeout:
        print("  ❌ 请求超时，服务器响应过慢")
        return False
    except Exception as e:
        print(f"  ❌ 上传测试异常: {e}")
        return False

if __name__ == "__main__":
    success = test_file_upload()
    if success:
        print("\n🎉 文件上传测试通过！")
    else:
        print("\n❌ 文件上传测试失败！")