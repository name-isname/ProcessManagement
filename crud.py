from sqlalchemy.orm import Session

import models

#获取所有进程
def get_all_process(db: Session):
    return db.query(models.Process).all()

def create_process(db: Session, process: models.Process):
    db.add(process)
    db.commit()
    db.refresh(process)
    return process

if __name__ == "__main__":
    from database import SessionLocal, engine

    models.Base.metadata.create_all(bind=engine)
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    def build_process(name: str, p_status: str, priority: str, details: str):
        process = models.Process(
            name=name,
            status= p_status,
            priority=priority,
            details=details,
        )
        return process

    def get_process_info():
        name = input("name?:")
        p_status = input("status?:")
        priority = input("priority?:")
        details = input("details?:")
        return name, p_status, priority, details

    def print_process_details(process: models.Process):
        print(f"""进程ID: {process.id}
名称: {process.name}
状态: {process.status}
优先级: {process.priority}
创建时间: {process.created_at}
详细信息: {process.details}
------------------------""")

    for process in get_all_process(next(get_db())):
        print_process_details(process)

    created_process = create_process(next(get_db()), build_process(*get_process_info()))
    print(type(create_process))
    print_process_details(created_process)


