from pydantic import BaseModel

class FighterBase(BaseModel):
    name: str
    elo_rating: float

class FighterResponse(FighterBase):
    id: int

    class Config:
        orm_mode = True

class FightBase(BaseModel):
    fighter_1_id: int
    fighter_2_id: int
    result: str
    method: str

class FightResponse(FightBase):
    id: int

    class Config:
        orm_mode = True
