from sqlalchemy.orm import Session
from app import models, schemas

def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()

def create_program(db: Session, program: schemas.ProgramCreate):
    db_program = models.Program(**program.dict())
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program

def enroll_client(db: Session, client_id: int, program_id: int):
    client = get_client(db, client_id)
    program = db.query(models.Program).filter(models.Program.id == program_id).first()
    client.programs.append(program)
    db.commit()
    return client

def search_clients(db: Session, query: str):
    return db.query(models.Client).filter(models.Client.name.ilike(f"%{query}%")).all()

def get_all_clients(db: Session):
    return db.query(models.Client).all()
