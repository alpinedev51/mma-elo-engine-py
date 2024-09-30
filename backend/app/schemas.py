from pydantic import BaseModel

class FighterBase(BaseModel):
    name: str
    elo: float

class FighterResponse(FighterBase):
    id: int

    class Config:
        from_attributes = True

class FightBase(BaseModel):
    fighter_1_id: int
    fighter_2_id: int
    result: str
    method: str
    event_id: int

class EventBase(BaseModel):
    event: str
    
class EventResponse(EventBase):
    id: int
    
    class Config:
        from_attributes = True
class FightResponse(FightBase):
    id: int

    class Config:
        from_attributes = True
