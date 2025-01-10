from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
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

@router.get("/events/search", response_model=List[schemas.EventResponse], status_code=status.HTTP_200_OK)
def search_event_by_name(event_name: str, db: Session = Depends(get_db)):
    if not event_name or event_name.strip() == "":
        return []
    events = crud.get_event_by_name(db, event_name.strip())
    if not events:
        raise HTTPException(status_code=404, detail=f"Event with name {event_name} not found")
    return events

@router.get("/events/{event_id}", response_model=schemas.EventResponse, status_code=status.HTTP_200_OK)
def read_event_by_id(event_id: int, db: Session = Depends(get_db)):
    event = crud.get_event_by_id(db, event_id)
    if event is None:
        raise HTTPException(status_code=404, detail=f"Event with ID {event_id} not found")
    return event

@router.get("/events/", response_model=List[schemas.EventResponse], status_code=status.HTTP_200_OK)
def read_events(skip: int = 0, limit: int = 10, sort: str = 'event_date', order: str = 'desc', db: Session = Depends(get_db)):
    events = crud.get_events(db, skip, limit, sort, order)
    if not events:
        raise HTTPException(status_code=404, detail=f"Events not returned...")
    return events

