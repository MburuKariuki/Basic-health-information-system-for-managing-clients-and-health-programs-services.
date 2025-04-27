from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.database import engine, SessionLocal
from fastapi.staticfiles import StaticFiles

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Health Info API - Daniel Mburu")

templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/clients/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    return crud.create_client(db, client)

@app.get("/clients/{client_id}", response_model=schemas.Client)
def read_client(client_id: int, db: Session = Depends(get_db)):
    db_client = crud.get_client(db, client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@app.post("/programs/", response_model=schemas.Program)
def create_program(program: schemas.ProgramCreate, db: Session = Depends(get_db)):
    return crud.create_program(db, program)

@app.post("/enrollments/")
def enroll_client(enrollment: schemas.Enrollment, db: Session = Depends(get_db)):
    return crud.enroll_client(db, enrollment.client_id, enrollment.program_id)

@app.get("/search/", response_class=HTMLResponse)
def search_clients(request: Request, query: str = "", db: Session = Depends(get_db)):
    clients = crud.search_clients(db, query)
    return templates.TemplateResponse("index.html", {"request": request, "clients": clients})

@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    clients = crud.get_all_clients(db)
    return templates.TemplateResponse("index.html", {"request": request, "clients": clients})
