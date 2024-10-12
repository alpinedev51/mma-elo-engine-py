from app.models import Fighter, Event, EloRecord
from app.elo_engine.update_fighter_elo import update_elo_ratings

def reset_fighter_elo(session, base_elo=1000):
    """
    Reset the ELO rating for all fighters in the database to the default value (1000).
    
    :param session: The database session.
    """
    fighters = session.query(Fighter).all()
    
    session.query(EloRecord).delete()
    elo_record_count = session.query(EloRecord).count()
    if elo_record_count == 0:
        print("EloRecord table is empty after deletion.")
    else:
        raise ValueError("EloRecord table should be empty after deletion.")
    
    for fighter in fighters:
        fighter.elo_rating = base_elo
        #new_record = EloRecord(fighter_id=fighter.id, elo_rating=base_elo, event_id=None)
        #session.add(new_record)
        
    #elo_record_count = session.query(EloRecord).count()
    #fighters_count = session.query(Fighter).count()
    #if elo_record_count != fighters_count:
    #    raise ValueError("Elo Record count should have same number of entries as Fighters.")
    
    session.commit()
    print(f"Reset ELO ratings for {len(fighters)} fighters.")

def update_all_fighters_elo(session):
    """
    Recalculate and update the ELO ratings for all fighters by processing all events and fights.
    
    :param session: The database session.
    """
    reset_fighter_elo(session)
    
    events = session.query(Event).order_by(Event.event_date).all()
    
    for event in events:
        print(f"Processing event {event.id} ({event.event_name})...")
        update_elo_ratings(event.id, session)
        session.commit()
        print(f"Updated ELO ratings for event {event.id}.")

if __name__ == "__main__":
    from app.database import get_db
    
    db = next(get_db())
    
    update_all_fighters_elo(db)
    
    db.close()
