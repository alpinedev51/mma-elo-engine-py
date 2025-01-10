from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/elo-records/search", response_model=List[schemas.EloRecordByFighterResponse], status_code=status.HTTP_200_OK)
def read_elo_records_by_fighter(fighter_name: str, db: Session = Depends(get_db)):
    if not fighter_name or fighter_name.strip() == "":
        return []
    elo_records = crud.get_elo_records_by_fighter(db, fighter_name.strip())
    if not elo_records:
        raise HTTPException(status_code=404, detail="No Elo records returned...")
    return elo_records

def create_or_replace_elo_records_function(db: Session = Depends(get_db)):
    function_sql = """
    CREATE OR REPLACE FUNCTION get_elo_records_by_fighter(
        fighter_name arg TEXT,
        sort_column_arg TEXT,
        sort_order_arg TEXT
    )
    RETURNS TABLE (id INT, fighter_id INT, elo_rating FLOAT, event_name TEXT, event_date DATE) AS $$
    BEGIN
        RETURN QUERY
        SELECT
            er.id,
            er.fighter_id,
            er.elo_rating,
            e.event_name,
            e.event_date
        FROM elo_records er
        JOIN event e ON er.event_id = e.id
        JOIN fighter f ON er.fighter_id = f.id
        WHERE f.fighter_name ILIKE '%' || fighter_name_arg || '%'
        ORDER BY
            CASE
                WHEN sort_column_arg = 'elo_rating' AND sort_order_arg = 'desc' THEN er.elo_rating DESC
                WHEN sort_column_arg = 'elo_rating' AND sort_order_arg = 'asc' THEN er.elo_rating ASC
                ELSE e.event_date DESC
            END;
    END;
    $$ LANGUAGE plpgsql;
    """
    db.execute(text(function_sql))
    db.commit()

