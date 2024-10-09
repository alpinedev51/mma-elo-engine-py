from app.models import Fighter, Fight, EloRecord  # Import models from app.models
from .elo_calculator import calculate_elo

def update_fighter_elo(fight, session, event_id):
    """
    Update the ELO rating for two fighters based on the result of a fight.
    """
    # Fetch both fighters from the database
    fighter_1 = session.query(Fighter).filter(Fighter.id == fight.fighter_1_id).one()
    fighter_2 = session.query(Fighter).filter(Fighter.id == fight.fighter_2_id).one()

    # Calculate new ELO ratings based on the fight result
    new_elo_fighter_1, new_elo_fighter_2 = calculate_elo(
        fighter_1.elo_rating, fighter_2.elo_rating, fight.result, fight.method, k_factor=200
    )

    # Update fighter ELOs in the database
    fighter_1.elo_rating = new_elo_fighter_1
    fighter_2.elo_rating = new_elo_fighter_2
    
    history_entry_1 = EloRecord(fighter_id=fighter_1.id, elo_rating=new_elo_fighter_1, event_id=event_id)
    history_entry_2 = EloRecord(fighter_id=fighter_2.id, elo_rating=new_elo_fighter_2, event_id=event_id)
    
    session.add(history_entry_1)
    session.add(history_entry_2)

    return [
        {"id": fighter_1.id, "elo_score": new_elo_fighter_1},
        {"id": fighter_2.id, "elo_score": new_elo_fighter_2}
        ]

def update_elo_ratings(event_id, session):
    """
    Update the ELO ratings for all fights in a given event.
    
    :param event_id: The ID of the event to process.
    :param session: The database session.
    """
    # Fetch the event and related fights
    fights = session.query(Fight).filter(Fight.event_id == event_id).all()
    
    elo_updates = []

    # Process each fight in the event
    for fight in fights:
        elo_updates.extend(update_fighter_elo(fight, session, event_id))
    
    session.bulk_update_mappings(Fighter, elo_updates)
