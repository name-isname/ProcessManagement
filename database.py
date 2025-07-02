
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from pathlib import Path
import os

# 始终使用当前工作目录下的 process.db
DB_PATH = 'sqlite:///' + str(Path(os.getcwd()) / 'process.db')
engine = create_engine(DB_PATH)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine)

Base = declarative_base()