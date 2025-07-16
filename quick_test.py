import requests
import json

def test_api():
    print('🚀 快速API测试')
    print('='*40)

    base_url = 'http://localhost:8000'

    try:
        # 测试根路径
        r = requests.get(f'{base_url}/', timeout=3)
        print(f'✅ 根路径: {r.status_code} - {r.json()["message"]}')
        
        # 测试健康检查
        r = requests.get(f'{base_url}/health', timeout=3)
        health = r.json()
        print(f'✅ 健康检查: {r.status_code} - {health["status"]}')
        
        # 测试历史记录
        r = requests.get(f'{base_url}/api/history', timeout=3)
        data = r.json()
        print(f'✅ 历史记录: {r.status_code} - 找到 {len(data)} 条记录')
        
        # 测试统计数据
        r = requests.get(f'{base_url}/api/stats', timeout=3)
        stats = r.json()
        print(f'✅ 统计数据: {r.status_code} - 总记录: {stats["total_predictions"]}')
        
        # 测试最近记录
        r = requests.get(f'{base_url}/api/recent', timeout=3)
        recent = r.json()
        print(f'✅ 最近记录: {r.status_code} - {len(recent)} 条记录')
        
        print('\n🎉 所有API端点测试通过！')
        print('✅ FastAPI后端服务运行正常')
        return True
        
    except Exception as e:
        print(f'❌ API测试失败: {e}')
        return False

if __name__ == "__main__":
    test_api()