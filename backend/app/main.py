from fastapi import FastAPI, status, HTTPException, Depends
import crud
import schemas
from sqlalchemy.orm import Session
from typing import List
from database import init_db, get_db

# Create the database
init_db()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the MMA ELO Engine API"}

# Add additional endpoints here
@app.get("/fighters/{fighter_id}", response_model=schemas.FighterResponse, status_code=status.HTTP_200_OK)
def read_fighter_by_name(fighter_name: str, db: Session = Depends(get_db)):
    fighter = crud.get_fighter_by_name(db, fighter_name)
    if fighter is None:
        raise HTTPException(status_code=404, detail="Fighter not found")
    return fighter

@app.get("/fighters/{fighter_id}", response_model=schemas.FighterResponse, status_code=status.HTTP_200_OK)
def read_fighter_by_id(fighter_id: int, db: Session = Depends(get_db)):
    fighter = crud.get_fighter_by_id(db, fighter_id)
    if fighter is None:
        raise HTTPException(status_code=404, detail="Fighter not found")
    return fighter

@app.get("/fighters/", response_model=List[schemas.FighterResponse], status_code=status.HTTP_200_OK)
def read_fighters(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fighters = crud.get_fighters(db, skip=skip, limit=limit)
    return fighters

@app.get("/fights/{fight_id}", response_model=schemas.FightResponse, status_code=status.HTTP_200_OK)
def read_fight(fight_id: int, db: Session = Depends(get_db)):
    fight = crud.get_fight(db, fight_id)
    if fight is None:
        raise HTTPException(status_code=404, detail="Fight not found")
    return fight

@app.get("/fights/", response_model=List[schemas.FightResponse], status_code=status.HTTP_200_OK)
def read_fights(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fights = crud.get_fights(db, skip=skip, limit=limit)
    return fights