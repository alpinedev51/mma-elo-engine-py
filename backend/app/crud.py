from sqlalchemy.orm import Session
from models import Fighter, Fight
from schemas import FighterBase, FightBase

def get_fighter(db: Session, fighter_id: int):
    return db.query(Fighter).filter(Fighter.id == fighter_id).first()

def get_fighters(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Fighter).offset(skip).limit(limit).all()

def get_fight(db: Session, fight_id: int):
    return db.query(Fight).filter(Fight.id == fight_id).first()

def get_fights(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Fight).offset(skip).limit(limit).all()
