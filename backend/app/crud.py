from sqlalchemy.orm import Session
from sqlalchemy import text
from .models import Fighter, Fight, Event

# /fighters/search
def get_fighter_by_name(db: Session, fighter_name: str):
    return db.query(Fighter).filter(Fighter.fighter_name.ilike(f"%{fighter_name}%")).all()

# /fighters/{fighter_id}
def get_fighter_by_id(db: Session, fighter_id: int):
    return db.query(Fighter).filter(Fighter.id == fighter_id).first()

# /fighters/
def get_fighters(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Fighter).offset(skip).limit(limit).all()

# /events/search
def get_event_by_name(db: Session, event_name: str):
    return db.query(Event).filter(Event.event_name.ilike(f"%{event_name}%")).all()

# /events/{event_id}
def get_event_by_id(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()

# /events/
def get_events(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Event).offset(skip).limit(limit).all()

# /fights/search
def get_fights_with_fighter(db: Session, fighter_name: str):
    return db.query(Fight)\
        .join(Fighter, Fight.fighter_1_id == Fighter.id)\
        .filter(Fighter.fighter_name.ilike(f"%{fighter_name}%"))\
        .union(
            db.query(Fight)\
                .join(Fighter, Fight.fighter_2_id == Fighter.id)\
                .filter(Fighter.fighter_name.ilike(f"%{fighter_name}%"))
        )\
        .all()

# /fights/{fight_id}
def get_fight_by_id(db: Session, fight_id: int):
    return db.query(Fight).filter(Fight.id == fight_id).first()

# /fights/
def get_fights(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Fight).offset(skip).limit(limit).all()

# /elo-records/search
def get_elo_records_by_fighter(db: Session, fighter_name: str):
    result = db.execute(
        text("SELECT * FROM get_elo_records_by_fighter(:fighter_name_arg)"),
        {"fighter_name_arg": fighter_name}
    )
    records = result.fetchall()
    elo_records = [row._mapping for row in records]
    return elo_records if elo_records else None
