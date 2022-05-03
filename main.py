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



