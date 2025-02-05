from typing import List
from fastapi import APIRouter, status, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from starlette.status import HTTP_404_NOT_FOUND
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get(
            "/api/elo-records/search",
            response_model=List[schemas.FighterEloProgressionResponse],
            status_code=status.HTTP_200_OK,
            summary="Get Elo rating progression for fighters",
            description="Retrieve Elo rating history for fighters matching the search term. Returns grouped data by fighter with their Elo progression."
            )
def read_elo_records_by_fighter(
        fighter_name: str = Query(...,
                                  description="Name or partial name of the fighter(s) to search for",
                                  min_length=1,
                                  example="Connor Mac"
                                  ),
        sort: str = Query('desc',
                          description="Sort order for Elo progression (asc or desc)",
                          regex='^(asc|desc)$'
                          ),
        db: Session = Depends(get_db)
):
    fighter_name = fighter_name.strip()
    if not fighter_name or fighter_name == "":
        return []

    sort = sort.lower().strip()
    if sort not in ['asc', 'desc']:
        sort = 'desc'

    fighter_records = crud.get_elo_records_by_fighter(
        db,
        fighter_name,
        sort
    )
    if not fighter_records:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"No Elo records found for fighter name containing '{fighter_name}'"
        )
    return fighter_records

