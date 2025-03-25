from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

Base = declarative_base()

class Process(Base):
    __tablename__ = 'processes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    logs = relationship("Log", back_populates="process")

class Log(Base):
    __tablename__ = 'logs'

    id = Column(Integer, primary_key=True)
    process_id = Column(Integer, ForeignKey('processes.id'))
    log_entry = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    process = relationship("Process", back_populates="logs")

# 创建数据库引擎和表
engine = create_engine('sqlite:///f:\\ProcessManagement\\process.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)