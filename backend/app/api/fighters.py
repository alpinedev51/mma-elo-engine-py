from fastapi import APIRouter, Depends
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

@router.get("/fighters/{fighter_id}", response_model=schemas.FighterResponse)
def read_fighter(fighter_id: int, db: Session = Depends(get_db)):
    fighter = crud.get_fighter(db, fighter_id)
    if fighter is None:
        raise HTTPException(status_code=404, detail="Fighter not found")
    return fighter

@router.get("/fighters/", response_model=List[schemas.FighterResponse])
def read_fighters(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fighters = crud.get_fighters(db, skip=skip, limit=limit)
    return fighters
