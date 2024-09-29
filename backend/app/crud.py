from sqlalchemy.orm import Session
from . import models

def create_fighter(db: Session, name: str, elo_rating: float):
    fighter = models.Fighter(name=name, elo_rating=elo_rating)
    db.add(fighter)
    db.commit()
    db.refresh(fighter)
    return fighter

def get_fighters(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Fighter).offset(skip).limit(limit).all()
