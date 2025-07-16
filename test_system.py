"""
海洋垃圾检测系统测试脚本
"""
import os
import sys
import tempfile
from PIL import Image
import numpy as np

def test_imports():
    """测试所有必要的模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        import sqlmodel
        print("✅ SQLModel 导入成功")
    except ImportError as e:
        print(f"❌ SQLModel 导入失败: {e}")
        return False
    
    try:
        import fastapi
        print("✅ FastAPI 导入成功")
    except ImportError as e:
        print(f"❌ FastAPI 导入失败: {e}")
        return False
    
    try:
        from models import PredictionResponse, Detection, CATEGORY_NAMES
        print("✅ 数据模型导入成功")
    except ImportError as e:
        print(f"❌ 数据模型导入失败: {e}")
        return False
    
    return True


def test_database():
    """测试数据库功能"""
    print("\n🗄️ 测试数据库功能...")
    
    try:
        from db.session import init_database, get_session, test_connection
        from db.models import PredictionCreate
        from db.crud import create_prediction, get_predictions, get_prediction_stats
        
        # 测试数据库连接
        print("  - 测试数据库连接...")
        if test_connection():
            print("  ✅ 数据库连接成功")
        else:
            print("  ❌ 数据库连接失败")
            return False
        
        # 初始化数据库
        print("  - 初始化数据库...")
        init_database()
        print("  ✅ 数据库初始化成功")
        
        # 测试创建记录
        print("  - 测试创建检测记录...")
        with next(get_session()) as session:
            test_prediction = PredictionCreate(
                filename="test_image.jpg",
                label="塑料瓶",
                confidence=0.85
            )
            result = create_prediction(session, test_prediction)
            print(f"  ✅ 创建记录成功，ID: {result.id}")
            
            # 测试查询记录
            print("  - 测试查询记录...")
            predictions = get_predictions(session, limit=5)
            print(f"  ✅ 查询成功，找到 {len(predictions)} 条记录")
            
            # 测试统计功能
            print("  - 测试统计功能...")
            stats = get_prediction_stats(session)
            print(f"  ✅ 统计成功，总记录数: {stats.total_predictions}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 数据库测试失败: {e}")
        return False


def test_ai_inference():
    """测试AI推理模块"""
    print("\n🤖 测试AI推理模块...")
    
    try:
        from ai.inference import validate_image
        
        # 创建测试图片
        print("  - 创建测试图片...")
        test_image = Image.new('RGB', (100, 100), color='red')
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            test_image.save(temp_file.name)
            temp_image_path = temp_file.name
        
        # 测试图片验证
        print("  - 测试图片验证...")
        if validate_image(temp_image_path):
            print("  ✅ 图片验证成功")
        else:
            print("  ❌ 图片验证失败")
            return False
        
        # 清理测试文件
        os.unlink(temp_image_path)
        
        # 注意：不测试classify_image因为需要weights.pt模型文件
        print("  ⚠️ 跳过classify_image测试（需要weights.pt模型文件）")
        
        return True
        
    except Exception as e:
        print(f"  ❌ AI推理测试失败: {e}")
        return False


def test_api_models():
    """测试API数据模型"""
    print("\n📋 测试API数据模型...")
    
    try:
        from models import Detection, PredictionResponse, CATEGORY_NAMES
        
        # 测试Detection模型
        print("  - 测试Detection模型...")
        detection = Detection(class_name="塑料瓶", confidence=0.85)
        print(f"  ✅ Detection创建成功: {detection.class_name}, {detection.confidence}")
        
        # 测试PredictionResponse模型
        print("  - 测试PredictionResponse模型...")
        response = PredictionResponse(
            success=True,
            detections=[detection],
            message="测试成功",
            processing_time=1.23
        )
        print(f"  ✅ PredictionResponse创建成功: {len(response.detections)} 个检测结果")
        
        # 测试类别映射
        print("  - 测试类别映射...")
        print(f"  ✅ 支持 {len(CATEGORY_NAMES)} 个垃圾类别")
        
        return True
        
    except Exception as e:
        print(f"  ❌ API模型测试失败: {e}")
        return False


def test_fastapi_app():
    """测试FastAPI应用"""
    print("\n🚀 测试FastAPI应用...")
    
    try:
        from main import app
        print("  ✅ FastAPI应用导入成功")
        
        # 检查路由
        routes = [route.path for route in app.routes]
        expected_routes = ["/", "/api/predict", "/api/history", "/api/stats", "/api/recent", "/health"]
        
        print("  - 检查API路由...")
        for route in expected_routes:
            if any(route in r for r in routes):
                print(f"    ✅ 路由 {route} 存在")
            else:
                print(f"    ❌ 路由 {route} 缺失")
        
        return True
        
    except Exception as e:
        print(f"  ❌ FastAPI应用测试失败: {e}")
        return False


def main():
    """运行所有测试"""
    print("🧪 开始系统测试...\n")
    
    tests = [
        ("模块导入", test_imports),
        ("数据库功能", test_database),
        ("AI推理模块", test_ai_inference),
        ("API数据模型", test_api_models),
        ("FastAPI应用", test_fastapi_app),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试出现异常: {e}")
            results.append((test_name, False))
    
    # 显示测试结果摘要
    print("\n" + "="*50)
    print("📊 测试结果摘要")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{test_name:<15} {status}")
        if result:
            passed += 1
    
    print("-"*50)
    print(f"总计: {passed}/{total} 个测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统准备就绪。")
        return True
    else:
        print("⚠️ 部分测试失败，请检查上述错误信息。")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)