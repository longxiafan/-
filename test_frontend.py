"""
前端测试脚本
"""
import sys
import importlib.util

def test_frontend_imports():
    """测试前端所需的模块导入"""
    print("🔍 测试前端模块导入...")
    
    required_modules = [
        'streamlit',
        'requests', 
        'pandas',
        'plotly.express',
        'PIL'
    ]
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module} 导入成功")
        except ImportError as e:
            print(f"  ❌ {module} 导入失败: {e}")
            return False
    
    return True

def test_frontend_syntax():
    """测试前端代码语法"""
    print("\n📝 测试前端代码语法...")
    
    try:
        # 读取前端代码文件
        with open('frontend/app.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        # 编译代码检查语法
        compile(code, 'frontend/app.py', 'exec')
        print("  ✅ 前端代码语法正确")
        return True
        
    except SyntaxError as e:
        print(f"  ❌ 前端代码语法错误: {e}")
        return False
    except Exception as e:
        print(f"  ❌ 前端代码检查失败: {e}")
        return False

def test_api_connection():
    """测试API连接配置"""
    print("\n🔗 测试API连接配置...")
    
    try:
        import requests
        
        # 检查API是否可访问
        api_url = "http://localhost:8000"
        response = requests.get(f"{api_url}/health", timeout=3)
        
        if response.status_code == 200:
            print(f"  ✅ API服务可访问: {api_url}")
            return True
        else:
            print(f"  ❌ API服务响应异常: {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("  ⚠️ API服务未启动，前端将无法正常工作")
        return False
    except Exception as e:
        print(f"  ❌ API连接测试失败: {e}")
        return False

def simulate_frontend_logic():
    """模拟前端核心逻辑"""
    print("\n🧠 模拟前端核心逻辑...")
    
    try:
        import streamlit as st
        import requests
        import pandas as pd
        import plotly.express as px
        
        # 模拟API调用
        print("  - 模拟API调用...")
        api_url = "http://localhost:8000/api/stats"
        response = requests.get(api_url, timeout=3)
        
        if response.status_code == 200:
            stats = response.json()
            print(f"    ✅ 获取统计数据: {stats['total_predictions']} 条记录")
            
            # 模拟数据处理
            if stats['categories_count']:
                df = pd.DataFrame(
                    list(stats['categories_count'].items()),
                    columns=['类别', '数量']
                )
                print(f"    ✅ 数据处理成功: {len(df)} 个类别")
            
            print("  ✅ 前端逻辑模拟成功")
            return True
        else:
            print(f"    ❌ API调用失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ 前端逻辑模拟失败: {e}")
        return False

def main():
    """运行前端测试"""
    print("🖥️ Streamlit前端测试")
    print("="*50)
    
    tests = [
        ("模块导入", test_frontend_imports),
        ("代码语法", test_frontend_syntax), 
        ("API连接", test_api_connection),
        ("核心逻辑", simulate_frontend_logic)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 显示结果
    print("\n" + "="*50)
    print("📊 前端测试结果")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:<10} {status}")
        if result:
            passed += 1
    
    print("-"*50)
    print(f"总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("\n🎉 前端测试全部通过！")
        print("💡 启动命令: streamlit run frontend/app.py")
        print("🌐 访问地址: http://localhost:8501")
    else:
        print("\n⚠️ 部分前端测试失败")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)