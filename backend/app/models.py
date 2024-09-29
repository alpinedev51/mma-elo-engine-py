from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Define the Fighter model
class Fighter(Base):
    __tablename__ = "fighters"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), unique=True, index=True)
    elo_rating = Column(Float, nullable=False)

    # Relationship to the fights
    fights_as_fighter_1 = relationship("Fight", back_populates="fighter_1", foreign_keys="Fight.fighter_1_id")
    fights_as_fighter_2 = relationship("Fight", back_populates="fighter_2", foreign_keys="Fight.fighter_2_id")
    
    def __repr__(self):
        return f"<Fighter(name={self.name}, elo={self.elo_rating})>"

# Define the Fight model
class Fight(Base):
    __tablename__ = "fights"
    
    id = Column(Integer, primary_key=True, index=True)
    fighter_1_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)
    fighter_2_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)
    result = Column(String(50), nullable=False)  # e.g., "win", "loss", "draw"
    method = Column(String(50))  # e.g., "TKO", "submission, decision
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    # Relationships
    fighter_1_relationship = relationship("Fighter", back_populates="fights_as_fighter_1", foreign_keys=[fighter_1_id])
    fighter_2_relationship = relationship("Fighter", back_populates="fights_as_fighter_2", foreign_keys=[fighter_2_id])
    event_relationship = relationship("Event", back_populates="fights")
    
    def __repr__(self):
        return f"<Fight(fighter_1_id={self.fighter_1_id}, fighter_2_id={self.fighter_2_id}, result={self.result}, method={self.method})>"

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    event = Column(String, unique=True)
    
    # Establish relationship with fights
    fights = relationship("Fight", back_populates="event")
    
    def __repr__(self):
        return f"<Event(name={self.event})>"