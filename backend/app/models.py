from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base

# Define the Fighter model
class Fighter(Base):
    __tablename__ = "fighters"
    
    id = Column(Integer, primary_key=True, index=True)
    fighter_name = Column(String(255), unique=True, index=True)
    elo_rating = Column(Float, nullable=False)

    # Relationship to the fights
    fights_as_fighter_1 = relationship("Fight", back_populates="fighter_1_relationship", foreign_keys="Fight.fighter_1_id")
    fights_as_fighter_2 = relationship("Fight", back_populates="fighter_2_relationship", foreign_keys="Fight.fighter_2_id")
    
    elo_record_relationship = relationship("EloRecord", back_populates="fighter_relationship")
    
    def __repr__(self):
        return f"<Fighter(name={self.fighter_name}, elo_rating={self.elo_rating})>"
    
class EloRecord(Base):
    __tablename__ = "elo_records"

    id = Column(Integer, primary_key=True, index=True)
    fighter_id = Column(Integer, ForeignKey("fighters.id"))
    elo_rating = Column(Float, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"))

    fighter_relationship = relationship("Fighter", back_populates="elo_record_relationship")

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String, unique=True)
    event_date = Column(Date)
    
    # Establish relationship with fights
    fights_relationship = relationship("Fight", back_populates="event_relationship")
    
    def __repr__(self):
        return f"<Event(name={self.event_name}, event_date={self.event_date})>"

# Define the Fight model
class Fight(Base):
    __tablename__ = "fights"
    
    id = Column(Integer, primary_key=True, index=True)
    fighter_1_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)
    fighter_2_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)
    result = Column(String(50), nullable=False)  # e.g., "win", "loss", "draw"
    method = Column(String(50))  # e.g., "TKO", "submission", "decision"
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    # Relationships
    fighter_1_relationship = relationship("Fighter", back_populates="fights_as_fighter_1", foreign_keys=[fighter_1_id])
    fighter_2_relationship = relationship("Fighter", back_populates="fights_as_fighter_2", foreign_keys=[fighter_2_id])
    event_relationship = relationship("Event", back_populates="fights_relationship")
    
    def __repr__(self):
        return f"<Fight(fighter_1_id={self.fighter_1_id}, fighter_2_id={self.fighter_2_id}, result={self.result}, method={self.method})>"
