from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path  # 添加这行
from sqlalchemy import create_engine

# 创建数据库引擎和表
DB_PATH = 'sqlite:///' + str(Path(__file__).parent / 'process.db')
engine = create_engine(
    DB_PATH, 
    connect_args={"check_same_thread": False}
    )

#Base.metadata.create_all(engine)#需要放到crud中

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine)

Base = declarative_base()