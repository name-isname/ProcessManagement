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

@app.post("/processes/",response_model=schemas.Process)
def create_process(process:schemas.ProcessCreate,db:Session = Depends(get_db))->models.Process:
    return crud.create_process(db=db,process=process)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="main:app", host="127.0.0.1", port=8000, reload=True)