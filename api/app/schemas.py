from datetime import datetime
from typing import (Optional, List)
from pydantic import BaseModel

from api.app.models import Aula

class EventBase(BaseModel):
    name: str
    codigo: Optional[str] = None
    docente: Optional[str] = None
    hora_inicio: datetime
    hora_fin: datetime

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    aula_id: int

    class Config:
        orm_mode = True


class AulaBase(BaseModel):
    codigo: str
    capacidad: int

class AulaCreate(AulaBase):
    pass
    
class Aula(AulaBase):
    id:int
    eventos: List[Event] = []
    # status: str
    # current_event: Event
    # next_events: List[Event]

    class Config:
        orm_mode = True


