from pydantic import BaseModel, condecimal
from typing import List
from datetime import datetime

class FighterBase(BaseModel):
    fighter_name: str
    elo_rating: float

class FighterResponse(FighterBase):
    id: int

    class Config:
        from_attributes = True

class Pagination(BaseModel):
    total_count: int
    page: int
    per_page: int
    pages: int

class FightersListResponse(BaseModel):
    data: List[FighterResponse]
    total_count: int
    pagination: Pagination

class EloRecordBase(BaseModel):
    fighter_id: int
    elo_rating: float
    event_id: int

class EloRecordResponse(EloRecordBase):
    id: int

    class Config:
        from_attributes = True

class EventBase(BaseModel):
    event_name: str
    event_date: datetime

class EventResponse(EventBase):
    id: int

    class Config:
        from_attributes = True

class FightBase(BaseModel):
    fighter_1_id: int
    fighter_2_id: int
    result: str
    method: str
    event_id: int

class FightResponse(FightBase):
    id: int

    class Config:
        from_attributes = True


class EloRecordByFighterResponse(BaseModel):
    fighter_id: int
    fighter_name: str
    elo_rating: float

    class Config:
        from_attributes = True

