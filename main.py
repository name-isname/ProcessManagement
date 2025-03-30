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
    db_process = crud.get_processes_by_status(db,"运行中")
    if db_process is None:
        raise HTTPException(status_code=404,detail="Process not found")
    return db_process

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)