from typing import List, Optional
from pydantic import BaseModel

class ProgramBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProgramCreate(ProgramBase):
    pass

class Program(ProgramBase):
    id: int
    class Config:
        orm_mode = True

class ClientBase(BaseModel):
    name: str
    age: int

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    programs: List[Program] = []
    class Config:
        orm_mode = True

class Enrollment(BaseModel):
    client_id: int
    program_id: int
