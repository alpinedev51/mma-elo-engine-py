from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("api/elo-records/search", response_model=List[schemas.EloRecordByFighterResponse], status_code=status.HTTP_200_OK)
def read_elo_records_by_fighter(fighter_name: str, db: Session = Depends(get_db)):
    if not fighter_name or fighter_name.strip() == "":
        return []
    elo_records = crud.get_elo_records_by_fighter(db, fighter_name.strip())
    if not elo_records:
        raise HTTPException(status_code=404, detail="No Elo records returned...")
    return elo_records

