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
    print('成功')
    return db.execute(select(models.Process).where(models.Process.id == process_id)).scalar_one_or_none()

def get_processes_by_status(db: Session, status: schemas.ProcessStatus) -> list[models.Process]:
    return db.execute(select(models.Process).where(models.Process.status == status)).scalars().all()

def get_all_processes(db: Session) -> list[models.Process]:
    return db.execute(select(models.Process)).scalars().all()

def update_process(db: Session, process_id: int, process: schemas.ProcessUpdate) -> models.Process:
    db_process = get_process_by_id(db, process_id)
    if db_process is None:
        return None
    if process.name:
        db_process.name = process.name
    if process.description:
        db_process.description = process.description
    if process.status:
        db_process.status = process.status
    if process.priority:
        db_process.priority = process.priority
    db.commit()
    db.refresh(db_process)
    return db_process

def delete_process(db: Session, process_id: int) -> models.Process:
    db_process = get_process_by_id(db, process_id)
    if db_process is None:
        print('failed')
        return None
    db.execute(delete(models.Log).where(models.Log.process_id == process_id))
    db.delete(db_process)
    db.commit()
    return db_process

def get_all_logs_of_process(db: Session, process_id: int) -> list[models.Log]:
    db_process = get_process_by_id(db, process_id)
    if db_process is None:
        return None
    return db_process.logs

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

# if __name__ == "__main__":
#     from database import SessionLocal, engine

#     models.Base.metadata.create_all(bind=engine)
#     def get_db():
#         db = SessionLocal()
#         try:
#             yield db
#         finally:
#             db.close()
    
#     import schemas
    
#     def build_process(process_data: schemas.ProcessCreate):
#         return models.Process(
#             name=process_data.name,
#             status=process_data.status.value,
#             priority=process_data.priority.value,
#             details=process_data.details
#         )
    
#     def get_process_info():
#         name = input("name?: ")
        
#         print(f"可用状态: {[status.value for status in schemas.ProcessStatus]}")
#         while True:
#             p_status = input("status?: ").lower()
#             if p_status in [status.value for status in schemas.ProcessStatus]:
#                 break
#             print("无效的状态，请重新输入")
        
#         print(f"可用优先级: {[p.value for p in schemas.ProcessPriority]}")
#         while True:
#             priority = input("priority?: ").lower()
#             if priority in [p.value for p in schemas.ProcessPriority]:
#                 break
#             print("无效的优先级，请重新输入")
        
#         details = input("details?: ")
        
#         # 使用 Pydantic 模型创建和验证数据
#         return schemas.ProcessCreate(
#             name=name,
#             status=p_status,
#             priority=priority,
#             details=details
#         )
    
#     def print_process_details(process: models.Process):
#         print(f"""进程ID: {process.id}
# 名称: {process.name}
# 状态: {process.status}
# 优先级: {process.priority}
# 创建时间: {process.created_at}
# 详细信息: {process.details}
# ------------------------""")

#     # for process in get_all_process(next(get_db())):
#     #     print_process_details(process)
#     #os.system("cls")
#     #created_process = create_process(next(get_db()), build_process(*get_process_info()))
#     #print(type(create_process))
#     #print_process_details(created_process)
#     # for process in get_process_by_status(next(get_db())):
#     #     print_process_details(process)
#     created_process = create_process(next(get_db()), build_process(get_process_info()))
#     print_process_details(created_process)

