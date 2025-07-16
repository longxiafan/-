"""
数据库连接和会话管理
"""
import os
from typing import Generator
from sqlmodel import SQLModel, create_engine, Session

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ocean_trash_detection.db")

# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    echo=False,  # 设置为True可以看到SQL语句
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)


def create_db_and_tables():
    """创建数据库和表"""
    SQLModel.metadata.create_all(engine)
    print("数据库和表创建成功")


def get_session() -> Generator[Session, None, None]:
    """获取数据库会话"""
    with Session(engine) as session:
        yield session


def init_database():
    """初始化数据库"""
    try:
        create_db_and_tables()
        print("数据库初始化完成")
    except Exception as e:
        print(f"数据库初始化失败: {str(e)}")
        raise


# 测试数据库连接
def test_connection():
    """测试数据库连接"""
    try:
        from sqlmodel import text
        with Session(engine) as session:
            # 执行一个简单的查询来测试连接
            session.exec(text("SELECT 1")).first()
            print("数据库连接测试成功")
            return True
    except Exception as e:
        print(f"数据库连接测试失败: {str(e)}")
        return False