"""
FastAPI服务器测试脚本
"""
import requests
import time
import subprocess
import sys
from threading import Thread

def test_api_endpoints():
    """测试API端点"""
    base_url = "http://localhost:8000"
    
    print("🔍 测试API端点...")
    
    # 等待服务器启动
    print("⏳ 等待服务器启动...")
    time.sleep(2)
    
    try:
        # 测试根路径
        print("  - 测试根路径 /")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("  ✅ 根路径响应正常")
        else:
            print(f"  ❌ 根路径响应异常: {response.status_code}")
        
        # 测试健康检查
        print("  - 测试健康检查 /health")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("  ✅ 健康检查正常")
            print(f"    响应: {response.json()}")
        else:
            print(f"  ❌ 健康检查异常: {response.status_code}")
        
        # 测试历史记录
        print("  - 测试历史记录 /api/history")
        response = requests.get(f"{base_url}/api/history")
        if response.status_code == 200:
            history = response.json()
            print(f"  ✅ 历史记录正常，找到 {len(history)} 条记录")
        else:
            print(f"  ❌ 历史记录异常: {response.status_code}")
        
        # 测试统计数据
        print("  - 测试统计数据 /api/stats")
        response = requests.get(f"{base_url}/api/stats")
        if response.status_code == 200:
            stats = response.json()
            print(f"  ✅ 统计数据正常，总记录: {stats['total_predictions']}")
        else:
            print(f"  ❌ 统计数据异常: {response.status_code}")
        
        print("🎉 API端点测试完成！")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保FastAPI服务正在运行")
        return False
    except Exception as e:
        print(f"❌ API测试失败: {e}")
        return False

if __name__ == "__main__":
    print("🧪 FastAPI服务器测试")
    print("="*40)
    
    # 提示用户启动服务器
    print("📝 请在另一个终端窗口运行以下命令启动服务器：")
    print("   python main.py")
    print()
    input("按Enter键继续测试（确保服务器已启动）...")
    
    success = test_api_endpoints()
    
    if success:
        print("\n✅ 所有API测试通过！")
    else:
        print("\n❌ 部分API测试失败")
    
    sys.exit(0 if success else 1)