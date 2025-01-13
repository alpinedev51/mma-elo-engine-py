from sqlalchemy.orm import Session
from sqlalchemy import text, asc, desc
from .models import Fighter, Fight, Event
from fastapi import HTTPException

sortable_fields = {
    'elo_rating': Fighter.elo_rating,
    'fighter_name': Fighter.fighter_name,
    'id': Fighter.id,
}

'''
optimizing the search query:
- currently uses ilike which does a full table scan
- for larger datasets, it's better to do a full-rext search
- query = db.query(Fighter).filter(func.to_tsvector(Fighter.fighter_name).match(fighter_name))
'''
# /fighters/search
def get_fighter_by_name(
        db: Session,
        fighter_name: str,
        skip: int = 0,
        limit: int = 10,
        sort: str = 'elo_rating',
        order: str = 'desc'
):
    if sort not in sortable_fields:
        sort = 'elo_rating'
    query = db.query(Fighter).filter(Fighter.fighter_name.ilike(f"%{fighter_name}%"))
    field = sortable_fields[sort]
    if order == 'asc':
        query = query.order_by(asc(field))
    elif order == 'desc':
        query = query.order_by(desc(field))

    total_count = query.count()
    query = query.offset(skip).limit(limit)
    results = query.all()
    return {"data": results, "total_count": total_count}

# /fighters/{fighter_id}
def get_fighter_by_id(db: Session, fighter_id: int):
    return db.query(Fighter).filter(Fighter.id == fighter_id).first()

# /fighters/
def get_fighters(
        db: Session, 
        skip: int = 0, 
        limit: int = 10, 
        sort: str = 'elo_rating', 
        order: str = 'desc'
):
    if sort not in sortable_fields:
        raise HTTPException(status_code=400, detail="Invalid sort field")
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail="Order must be asc or desc")
    query = db.query(Fighter)
    field = sortable_fields[sort]
    if order == 'asc':
        query = query.order_by(asc(field))
    elif order == 'desc':
        query = query.order_by(desc(field))
    total_count = query.count()
    fighters = query.offset(skip).limit(limit).all()
    page = skip // limit + 1
    return {
        "data": fighters,
        "total_count": total_count,
        "page": page,
        "per_page": limit
    }

# /events/search
def get_event_by_name(db: Session, event_name: str, sort: str = 'event_date', order: str = 'desc'):
    query = db.query(Event).filter(Event.event_name.ilike(f"%{event_name}%"))
    if sort == 'event_date':
        if order == 'asc':
            query = query.order_by(asc(Event.event_date))
        elif order == 'desc':
            query = query.order_by(desc(Event.event_date))
    return query.all()

# /events/{event_id}
def get_event_by_id(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()

# /events/
def get_events(db: Session, skip: int = 0, limit: int = 10, sort: str = 'event_date', order: str = 'desc'):
    query = db.query(Event)
    if sort == 'event_date':
        if order == 'asc':
            query = query.order_by(asc(Event.event_date))
        elif order == 'desc':
            query = query.order_by(desc(Event.event_date))
    return query.offset(skip).limit(limit).all()

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
        text("SELECT * FROM get_elo_records_by_fighter(:fighter_name_arg, :sort_column_arg, :sort_order_arg)"),
        {
            "fighter_name_arg": fighter_name,
            "sort_column_arg": "elo_rating",
            "sort_order_arg": "desc"
        }
    )
    records = result.fetchall()
    elo_records = [row._mapping for row in records]
    return elo_records if elo_records else None

