from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from pytz import timezone
from sqlalchemy import and_

"""
Session manages persistence operations for ORM-mapped objects.
Let's just refer to it as a database session for simplicity
"""

from api.app.models import Aula, Event
from api.app import schemas

"""
    Aula CRUD
"""

def get_aula(db:Session, aula_id:int):
    return db.query(Aula).filter(Aula.id==aula_id).first()

def get_aula_by_codigo(db:Session, codigo:str):
    return db.query(Aula).filter(Aula.codigo==codigo).first()

def get_aulas(db:Session, skip: int = 0, limit: int = 20):
    return db.query(Aula).offset(skip).limit(limit).all()

def create_aula(db:Session, aula: schemas.AulaCreate):
    new_aula = Aula(codigo=aula.codigo, capacidad=aula.capacidad)
    db.add(new_aula)
    db.commit()
    db.refresh(new_aula)
    return new_aula


def delete_aula(db:Session, codigo:str):
    db_aula = get_aula_by_codigo(db=db, codigo=codigo)
    db.delete(db_aula)
    db.commit()

def delete_all_aulas(db:Session):
    db.query(Aula).delete()
    db.commit()

"""
    Event CRUD
"""

def get_event(db:Session, id:int):
    return db.query(Event).filter(Event.id==id).first()

def get_next_events_by_aula(db:Session, aula_codigo:str, skip: int = 0, limit: int = 5):
    tz = timezone('America/Lima')
    now = datetime.now(tz=tz)
    end_date = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(1)

    return db.query(Event).filter(and_(
        Event.hora_inicio > now), 
        Event.hora_fin < end_date
    ).join(Aula).filter(and_(Aula.codigo == aula_codigo, )).offset(skip).limit(limit).all()

def get_current_event_by_aula(db:Session, aula_codigo:str):
    tz = timezone('America/Lima')
    now = datetime.now(tz=tz)
    return db.query(Event).filter(and_(
        Event.hora_inicio <= now), 
        Event.hora_fin > now
    ).join(Aula).filter(and_(Aula.codigo == aula_codigo, )).first()



def get_events(db:Session, skip: int = 0, limit: int = 5):
    return db.query(Event).offset(skip).limit(limit).all()

def create_aula_event(db:Session, event:schemas.EventCreate, aula_codigo: str):
    # check if aula exists
    aula = db.query(Aula).filter(Aula.codigo==aula_codigo).one_or_none()
    if aula is None:
        return
    
    new_event= Event(**event.dict(), aula_id=aula.id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

def delete_event(db:Session, id:int):
    db_event = get_event(db=db, id=id)
    db.delete(db_event)
    db.commit()