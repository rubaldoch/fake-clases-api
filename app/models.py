from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

# model/table

class Aula(Base):
    __tablename__ = "aula"

    # fields
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(6))
    capacidad = Column(Integer)
    eventos = relationship("Event", back_populates="aula")

class Event(Base):
    __tablename__ = "event"

    # fields 
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    codigo = Column(String(20))
    docente = Column(String(255))
    hora_inicio: Column(DateTime)
    hora_fin: Column(DateTime)
    aula_id: Column(Integer, ForeignKey("aula.id", ondelete="CASCADE"))
    aula = relationship("Aula", back_populates="eventos")
