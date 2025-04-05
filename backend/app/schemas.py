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

class EloProgressionRecord(BaseModel):
    elo_record_id: int
    elo_rating: float
    event_name: str | None
    event_date: str | None
    fight_number: int

    class Config:
        from_attributes = True

class FighterEloProgressionResponse(BaseModel):
    fighter_id: int
    fighter_name: str
    total_fights: int
    elo_progression: list[EloProgressionRecord]

    class Config:
        from_attributes = True

class PaginatedFighterEloProgressionResponse(BaseModel):
    data: List[FighterEloProgressionResponse]
    total_count: int
    pagination: Pagination
