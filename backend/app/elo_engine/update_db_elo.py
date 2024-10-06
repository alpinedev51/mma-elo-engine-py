from app.models import Fighter, Event
from app.elo_engine.update_fighter_elo import update_elo_ratings

def reset_fighter_elo(session, base_elo=1000):
    """
    Reset the ELO rating for all fighters in the database to the default value (1000).
    
    :param session: The database session.
    """
    # Fetch all fighters from the database
    fighters = session.query(Fighter).all()
    
    # Reset each fighter's ELO rating to 1000
    for fighter in fighters:
        fighter.elo_rating = base_elo
    
    # Commit the changes to the session
    session.commit()
    print(f"Reset ELO ratings for {len(fighters)} fighters.")

def update_all_fighters_elo(session):
    """
    Recalculate and update the ELO ratings for all fighters by processing all events and fights.
    
    :param session: The database session.
    """
    # Reset all fighter ELO ratings (default is to 1000)
    reset_fighter_elo(session)
    
    # Fetch all events in chronological order (assuming events have a date field)
    events = session.query(Event).order_by(Event.event_date).all()
    
    # Process each event and update ELO ratings
    for event in events:
        print(f"Processing event {event.id} ({event.event_name})...")
        update_elo_ratings(event.id, session)
        session.commit()
        print(f"Updated ELO ratings for event {event.id}.")

if __name__ == "__main__":
    # Assuming you have an existing session setup elsewhere, import it
    from app.database import get_db  # Replace with your actual engine import
    
    # Create a session
    db = next(get_db())
    
    # Update all fighters' ELO ratings
    update_all_fighters_elo(db)
    
    # Close the session
    db.close()
