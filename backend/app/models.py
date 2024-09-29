from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Define the Fighter model
class Fighter(Base):
    __tablename__ = 'fighters'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    elo_rating = Column(Float, nullable=False)

    # Relationship to the fights
    fights_as_fighter_1 = relationship("Fight", back_populates="fighter_1", foreign_keys='Fight.fighter_1_id')
    fights_as_fighter_2 = relationship("Fight", back_populates="fighter_2", foreign_keys='Fight.fighter_2_id')

# Define the Fight model
class Fight(Base):
    __tablename__ = 'fights'
    
    id = Column(Integer, primary_key=True, index=True)
    fighter_1_id = Column(Integer, ForeignKey('fighters.id'), nullable=False)
    fighter_2_id = Column(Integer, ForeignKey('fighters.id'), nullable=False)
    result = Column(String, nullable=False)  # e.g., "win", "loss", "draw"
    method = Column(String, nullable=False)  # e.g., "TKO", "submission, decision

    # Relationships
    fighter_1 = relationship("Fighter", back_populates="fights_as_fighter_1", foreign_keys=[fighter_1_id])
    fighter_2 = relationship("Fighter", back_populates="fights_as_fighter_2", foreign_keys=[fighter_2_id])