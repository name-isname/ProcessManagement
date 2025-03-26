from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

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