from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("api/fights/search", response_model=List[schemas.FightResponse], status_code=status.HTTP_200_OK)
def search_fights_with_fighter(fighter_name: str, db: Session = Depends(get_db)):
    if not fighter_name or fighter_name.strip() == "":
        return []
    fights = crud.get_fights_with_fighter(db, fighter_name.strip())
    if not fights:
        raise HTTPException(status_code=404, detail="Fights not found")
    return fights

@router.get("api/fights/{fight_id}", response_model=schemas.FightResponse, status_code=status.HTTP_200_OK)
def read_fight(fight_id: int, db: Session = Depends(get_db)):
    fight = crud.get_fight_by_id(db, fight_id)
    if fight is None:
        raise HTTPException(status_code=404, detail="Fight not found")
    return fight

@router.get("api/fights/", response_model=List[schemas.FightResponse], status_code=status.HTTP_200_OK)
def read_fights(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fights = crud.get_fights(db, skip=skip, limit=limit)
    if not fights:
        raise HTTPException(status_code=404, detail="No fights returned...")
    return fights

