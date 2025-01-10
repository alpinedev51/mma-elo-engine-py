from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("api/fighters/search", response_model=List[schemas.FighterResponse], status_code=status.HTTP_200_OK)
def search_fighter_by_name(
        fighter_name: str, 
        sort: str = 'elo_rating', 
        order: str = "desc", 
        db: Session = Depends(get_db)
):
    if not fighter_name or fighter_name.strip() == "":
        return []
    crud_result = crud.get_fighter_by_name(db, fighter_name.strip(), sort, order)
    fighters = crud_result["data"]
    if not fighters:
        raise HTTPException(status_code=404, detail=f"Fighter with name {fighter_name} not found")
    return crud_result

@router.get("api/fighters/{fighter_id}", response_model=schemas.FighterResponse, status_code=status.HTTP_200_OK)
def read_fighter_by_id(fighter_id: int, db: Session = Depends(get_db)):
    fighter = crud.get_fighter_by_id(db, fighter_id)
    if fighter is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Fighter with ID {fighter_id} not found"
        )
    return fighter

@router.get("api/fighters/", response_model=List[schemas.FighterResponse], status_code=status.HTTP_200_OK)
def read_fighters(
        skip: int = 0, 
        limit: int = 10, 
        sort: str = 'elo_rating', 
        order: str = 'desc', 
        db: Session = Depends(get_db)
):
    crud_result = crud.get_fighters(db, skip=skip, limit=limit, sort=sort, order=order)
    fighters = crud_result["data"]
    if not fighters:
        raise HTTPException(status_code=404, detail="No fighters returned...")
    total_count = crud_result["total_count"]
    pagination = {
        "total_count": total_count,
        "page": (skip // limit) + 1,
        "per_page": limit,
        "pages": (crud_result["total_count"] + limit - 1) // limit
    }

    return {
        "data": fighters,
        "total_count": total_count,
        "pagination": pagination
    }

