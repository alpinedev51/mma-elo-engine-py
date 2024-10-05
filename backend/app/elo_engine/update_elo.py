from sqlalchemy.orm import sessionmaker
from app.models import Fighter, Fight, Event  # Import models from app.models
from .elo_calculator import calculate_elo

def update_fighter_elo(fight, session):
    """
    Update the ELO rating for two fighters based on the result of a fight.
    """
    # Fetch both fighters from the database
    fighter_1 = session.query(Fighter).filter(Fighter.id == fight.fighter_1_id).one()
    fighter_2 = session.query(Fighter).filter(Fighter.id == fight.fighter_2_id).one()

    # Calculate new ELO ratings based on the fight result
    new_elo_fighter_1, new_elo_fighter_2 = calculate_elo(
        fighter_1.elo_rating, fighter_2.elo_rating, fight.result
    )

    # Update fighter ELOs in the database
    fighter_1.elo_rating = new_elo_fighter_1
    fighter_2.elo_rating = new_elo_fighter_2

    # Commit changes to the session
    session.commit()

def update_elo_ratings(event_id, session):
    """
    Update the ELO ratings for all fights in a given event.
    
    :param event_id: The ID of the event to process.
    :param session: The database session.
    """
    # Fetch the event and related fights
    event = session.query(Event).filter(Event.id == event_id).one()
    fights = session.query(Fight).filter(Fight.event_id == event.id).all()

    # Process each fight in the event
    for fight in fights:
        update_fighter_elo(fight, session)
