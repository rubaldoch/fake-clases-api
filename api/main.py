from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app import models, schemas, crud
from app.db import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

# Dependency
def get_db():
    db = SessionLocal()
    try:   
        yield db
    finally:
        db.close()


"Urls"

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

@app.post("/aulas/", response_model=schemas.Aula)
def create_aula(aula: schemas.AulaCreate, db:Session = Depends(get_db)):
    db_aula = crud.get_aula_by_codigo(db, codigo = aula.codigo)
    if db_aula:
        raise HTTPException(status_code=400, detail="Aula already registered")
    return crud.create_aula(db=db, aula=aula)

@app.get("/aulas/", response_model=List[schemas.Aula])
def read_aulas(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    aulas = crud.get_aulas(db=db, skip=skip, limit=limit)
    return aulas

@app.delete("/aulas/{codigo}")
def delete_aula(codigo: str, db: Session = Depends(get_db)):
    db_aula = crud.get_aula_by_codigo(db, codigo = aula.codigo)
    if not  db_aula:
        raise HTTPException(status_code=404, detail="Aula not found")
    crud.delete_aula(db, codigo)
    return {"ok": True}


@app.delete("/aulas/")
def delete_all_aulas(db: Session = Depends(get_db)):
    return crud.delete_all_aulas(db)

@app.post("/events/", response_model=schemas.Event)
def create_event(event: schemas.EventCreate, aula_codigo:str, db:Session = Depends(get_db)):
    db_aula = crud.create_aula_event (db, event, aula_codigo)
    return db_aula

@app.get("/events/", response_model=List[schemas.Event])
def read_events(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    events = crud.get_events(db=db, skip=skip, limit=limit)
    return events

@app.delete("/events/{id}")
def delete_event(id: int, db: Session = Depends(get_db)):
    event = crud.get_event(db, id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    crud.delete_event(db, id)
    return {"ok": True}

@app.get("/events/aula/{aula_codigo}")
def read_events(aula_codigo:str, skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    next_events = crud.get_next_events_by_aula(db, aula_codigo, skip, limit)
    current_event = crud.get_current_event_by_aula(db, aula_codigo)
    status =  "Ocupado" if current_event else "Libre"
   
    return {
        "status": status,
        "current_event": current_event,
        "next_events": next_events
    }

