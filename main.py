from fastapi import Depends,FastAPI,HTTPException,status,Request
from fastapi.responses import JSONResponse,HTMLResponse
from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles

import crud,models,schemas

from database import SessionLocal,engine
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# html 模板
templates = Jinja2Templates(directory="templates")
# 静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/",response_class=HTMLResponse)
def read_root(request:Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html",{"request":request})

@app.post("/create-processes/",response_model=schemas.Process)
def create_process(process:schemas.ProcessCreate,db:Session = Depends(get_db))->models.Process:
    return crud.create_process(db=db,process=process)

@app.get("/home",response_model=list[schemas.Process])
def read_processes_in_homepage(db:Session = Depends(get_db))->list[models.Process]:
    db_process = crud.get_processes_by_status(db,schemas.ProcessStatus.RUNNING)
    if not db_process:  # 空列表也是合法的，不应该抛出404
        return []
    return db_process

@app.get("/delete-process/{process_id}",response_model=schemas.Process)
def delete_process(process_id:int,db:Session = Depends(get_db))->models.Process:
    db_process = crud.delete_process(db,process_id)
    if db_process is None:
        raise HTTPException(status_code=404,detail="Process not found")
    return db_process

@app.post("/update-process/{process_id}",response_model=schemas.Process)
def update_process(process_id:int,process:schemas.ProcessUpdate,db:Session = Depends(get_db))->models.Process:
    db_process = crud.update_process(db,process_id,process)
    if db_process is None:
        raise HTTPException(status_code=404,detail="Process not found")
    return db_process

@app.get("/get-logs-of-process/{process_id}",response_model=list[schemas.Log])
def get_logs_of_process(process_id:int,db:Session = Depends(get_db)) -> list[models.Log]:
    db_logs = crud.get_all_logs_of_process(db,process_id)
    if db_logs is None:
        raise HTTPException(status_code=404,detail="Log not found")
    return db_logs

@app.post("/create-log-of-process/{process_id}",response_model=schemas.Log)
def create_log_of_process(process_id:int,log:schemas.LogCreate,db:Session = Depends(get_db)) -> models.Log:
    db_log = crud.create_log(db,process_id,log)
    if db_log is None:
        raise HTTPException(status_code=404,detail="Log not found")
    return db_log

@app.post("/update-log/{log_id}",response_model=schemas.Log)
def update_log(log_id:int,log:schemas.LogUpdate,db:Session = Depends(get_db)) -> models.Log:
    db_log = crud.update_log(db,log_id,log)
    if db_log is None:
        raise HTTPException(status_code=404,detail="Log not found")
    return db_log

@app.get("/delete-log/{log_id}",response_model=schemas.Log)
def delete_log(log_id:int,db:Session = Depends(get_db)) -> models.Log:
    db_log = crud.delete_log(db,log_id)
    if db_log is None:
        raise HTTPException(status_code=404,detail="Log not found")
    return db_log

@app.get("/all-processes", response_model=list[schemas.Process])
def read_all_processes(db: Session = Depends(get_db)) -> list[models.Process]:
    db_processes = crud.get_all_processes(db)
    return db_processes

@app.get("/processes-by-status/{status}", response_model=list[schemas.Process])
def read_processes_by_status(status: str, db: Session = Depends(get_db)) -> list[models.Process]:
    db_processes = crud.get_processes_by_status(db, status)
    if not db_processes:  # 空列表是合法的
        return []
    return db_processes

@app.get("/get-process/{process_id}", response_model=schemas.Process)
def get_process(process_id: int, db: Session = Depends(get_db)) -> models.Process:
    db_process = crud.get_process_by_id(db, process_id)
    if db_process is None:
        raise HTTPException(status_code=404, detail="Process not found")
    return db_process

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)