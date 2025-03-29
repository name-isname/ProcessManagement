from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship,mapped_column, Mapped
from datetime import datetime
from database import Base

class Process(Base):
    __tablename__ = 'processes'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    logs: Mapped[list["Log"]] = relationship(back_populates="process")

    def __repr__(self) -> str:
        return f"Process(id={self.id!r}, name={self.name!r}, description={self.description!r})"


class Log(Base):
    __tablename__ = 'logs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    process_id: Mapped[int] = mapped_column(ForeignKey('processes.id'))
    log_entry: Mapped[str] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.now)
    process: Mapped["Process"] = relationship(back_populates="logs")

    def __repr__(self) -> str:
        return f"Log(id={self.id!r}, process_id={self.process_id!r}, log_entry={self.log_entry!r})"
