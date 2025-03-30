from sqlalchemy.orm import Session
from sqlalchemy import select,delete

import models, schemas
import os

def create_process(db: Session, process: schemas.ProcessCreate) -> models.Process:
    db_process = models.Process(
        name=process.name,
        description=process.description,
        status=process.status,
        priority=process.priority
    )
    db.add(db_process)
    db.commit()
    db.refresh(db_process)
    return db_process

def get_process_by_id(db: Session, process_id: int) -> models.Process:
    return db.execute(select(models.Process).where(models.Process.id == process_id)).scalar_one_or_none()

def get_processes_by_status(db: Session, status: schemas.ProcessStatus) -> list[models.Process]:
    return db.execute(select(models.Process).where(models.Process.status == status)).scalars().all()

def get_all_processes(db: Session) -> list[models.Process]:
    return db.execute(select(models.Process)).scalars().all()

def update_process(db: Session, process_id: int, process: schemas.ProcessUpdate) -> models.Process:
    db_process = get_process_by_id(db, process_id)
    if db_process is None:
        return None
    # 使用 dict(exclude_unset=True) 只更新设置了的字段
    for key, value in process.dict(exclude_unset=True).items():
        setattr(db_process, key, value)
    db.commit()
    db.refresh(db_process)
    return db_process

def delete_process(db: Session, process_id: int) -> models.Process:
    db_process = get_process_by_id(db, process_id)
    if db_process is None:
        return None
    db.execute(delete(models.Log).where(models.Log.process_id == process_id))
    db.delete(db_process)
    db.commit()
    return db_process

def get_all_logs_of_process(db: Session, process_id: int) -> list[models.Log]:
    db_process = get_process_by_id(db, process_id)
    if db_process is None:
        return []
    return db_process.logs

#----------------log-------------

def create_log(db: Session, process_id: int, log: schemas.LogCreate) -> models.Log:
    db_process = get_process_by_id(db, process_id)
    if db_process is None:
        return None
    db_log = models.Log(
        process_id=process_id,
        log_entry=log.log_entry
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

def get_log_by_id(db: Session, log_id: int) -> models.Log:
    return db.execute(select(models.Log).where(models.Log.id == log_id)).scalar_one_or_none()

def update_log(db: Session, log_id: int, log: schemas.LogUpdate) -> models.Log:
    db_log = get_log_by_id(db, log_id)
    if db_log is None:
        return None
    for key, value in log.dict(exclude_unset=True).items():
        setattr(db_log, key, value)
    db.commit()
    db.refresh(db_log)
    return db_log

def delete_log(db: Session, log_id: int) -> models.Log:
    db_log = get_log_by_id(db, log_id)
    if db_log is None:
        return None
    db.delete(db_log)
    db.commit()
    return db_log
