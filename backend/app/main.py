from fastapi import FastAPI, status, HTTPException, Depends
from . import crud
from . import schemas
from sqlalchemy.orm import Session
from typing import List
from .database import init_db, get_db

# Create the database
#init_db()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the MMA ELO Engine API"}

@app.get("/fighters/search", response_model=List[schemas.FighterResponse], status_code=status.HTTP_200_OK)
def search_fighter_by_name(fighter_name: str, db: Session = Depends(get_db)):
    fighters = crud.get_fighter_by_name(db, fighter_name)
    if not fighters:
        raise HTTPException(status_code=404, detail=f"Fighter with name {fighter_name} not found")
    return fighters

@app.get("/fighters/{fighter_id}", response_model=schemas.FighterResponse, status_code=status.HTTP_200_OK)
def read_fighter_by_id(fighter_id: int, db: Session = Depends(get_db)):
    fighter = crud.get_fighter_by_id(db, fighter_id)
    if fighter is None:
        raise HTTPException(status_code=404, detail=f"Fighter with ID {fighter_id} not found")
    return fighter

@app.get("/fighters/", response_model=List[schemas.FighterResponse], status_code=status.HTTP_200_OK)
def read_fighters(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fighters = crud.get_fighters(db, skip=skip, limit=limit)
    if not fighters:
        raise HTTPException(status_code=404, detail="No fighters returned...")
    return fighters

@app.get("/events/search", response_model=List[schemas.EventResponse], status_code=status.HTTP_200_OK)
def search_event_by_name(event_name: str, db: Session = Depends(get_db)):
    events = crud.get_event_by_name(db, event_name)
    if not events:
        raise HTTPException(status_code=404, detail=f"Event with name {event_name} not found")
    return events

@app.get("/events/{event_id}", response_model=schemas.EventResponse, status_code=status.HTTP_200_OK)
def read_event_by_id(event_id: int, db: Session = Depends(get_db)):
    event = crud.get_event_by_id(db, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail=f"Event with ID {event_id} not found")
    return event

@app.get("/events/", response_model=List[schemas.EventResponse], status_code=status.HTTP_200_OK)
def read_events(skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    events = crud.get_events(db, skip, limit)
    if not events:
        raise HTTPException(status_code=404, detail=f"Events not returned...")
    return events

@app.get("/fights/search", response_model=List[schemas.FightResponse], status_code=status.HTTP_200_OK)
def search_fights_with_fighter(fighter_name: str, db: Session = Depends(get_db)):
    fights = crud.get_fights_with_fighter(db, fighter_name)
    if not fights:
        raise HTTPException(status_code=404, detail="Fights not found")
    return fights

@app.get("/fights/{fight_id}", response_model=schemas.FightResponse, status_code=status.HTTP_200_OK)
def read_fight(fight_id: int, db: Session = Depends(get_db)):
    fight = crud.get_fight_by_id(db, fight_id)
    if fight is None:
        raise HTTPException(status_code=404, detail="Fight not found")
    return fight

@app.get("/fights/", response_model=List[schemas.FightResponse], status_code=status.HTTP_200_OK)
def read_fights(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    fights = crud.get_fights(db, skip=skip, limit=limit)
    if not fights:
        raise HTTPException(status_code=404, detail="No fights returned...")
    return fights