from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

enrollments_table = Table(
    'enrollments', Base.metadata,
    Column('client_id', Integer, ForeignKey('clients.id')),
    Column('program_id', Integer, ForeignKey('programs.id'))
)

class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    programs = relationship('Program', secondary=enrollments_table, back_populates='clients')

class Program(Base):
    __tablename__ = 'programs'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    description = Column(String)
    clients = relationship('Client', secondary=enrollments_table, back_populates='programs')
