from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/fights/{fight_id}", response_model=schemas.FightResponse)
def read_fight(fight_id: int, db: Session = Depends(get_db)):
    fight = crud.get_fight(db, fight_id)
    if fight is None:
        raise HTTPException(status_code=404, detail="Fight not found")
    return fight

@router.get("/fights/", response_model=List[schemas.FightResponse])
def read_fights(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fights = crud.get_fights(db, skip=skip, limit=limit)
    return fights
