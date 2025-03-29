from sqlalchemy.orm import Session

import models, schemas
import os

#获取所有进程
def get_all_process(db: Session):
    return db.query(models.Process).all()

def create_process(db: Session, process: models.Process):
    db.add(process)
    db.commit()
    db.refresh(process)
    return process

def get_process_by_id(db: Session, process_id: int):
    return db.query(models.Process).filter(models.Process.id == process_id).first()

def get_process_by_status(db: Session, process_status: str = "running"):
    return db.query(models.Process).filter(models.Process.status == process_status).all()



if __name__ == "__main__":
    from database import SessionLocal, engine

    models.Base.metadata.create_all(bind=engine)
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    import schemas
    
    def build_process(process_data: schemas.ProcessCreate):
        return models.Process(
            name=process_data.name,
            status=process_data.status.value,
            priority=process_data.priority.value,
            details=process_data.details
        )
    
    def get_process_info():
        name = input("name?: ")
        
        print(f"可用状态: {[status.value for status in schemas.ProcessStatus]}")
        while True:
            p_status = input("status?: ").lower()
            if p_status in [status.value for status in schemas.ProcessStatus]:
                break
            print("无效的状态，请重新输入")
        
        print(f"可用优先级: {[p.value for p in schemas.ProcessPriority]}")
        while True:
            priority = input("priority?: ").lower()
            if priority in [p.value for p in schemas.ProcessPriority]:
                break
            print("无效的优先级，请重新输入")
        
        details = input("details?: ")
        
        # 使用 Pydantic 模型创建和验证数据
        return schemas.ProcessCreate(
            name=name,
            status=p_status,
            priority=priority,
            details=details
        )
    
    def print_process_details(process: models.Process):
        print(f"""进程ID: {process.id}
名称: {process.name}
状态: {process.status}
优先级: {process.priority}
创建时间: {process.created_at}
详细信息: {process.details}
------------------------""")

    # for process in get_all_process(next(get_db())):
    #     print_process_details(process)
    #os.system("cls")
    #created_process = create_process(next(get_db()), build_process(*get_process_info()))
    #print(type(create_process))
    #print_process_details(created_process)
    # for process in get_process_by_status(next(get_db())):
    #     print_process_details(process)
    created_process = create_process(next(get_db()), build_process(get_process_info()))
    print_process_details(created_process)

