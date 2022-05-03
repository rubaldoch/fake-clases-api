from sqlalchemy.orm import Session

"""
Session manages persistence operations for ORM-mapped objects.
Let's just refer to it as a database session for simplicity
"""

from app.models import Aula, Event
from app import schemas

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

"""
    Event CRUD
"""

def get_event(db:Session, id:int):
    return db.query(Event).filter(Event.id==id).first()

def get_events_by_aula(db:Session, aula_codigo:str, skip: int = 0, limit: int = 5):
    return db.query(Event).join(Aula).filter(Aula.codigo == aula_codigo).offset(skip).limit(limit).all()

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