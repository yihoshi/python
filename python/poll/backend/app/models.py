from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base

class Poll(Base):
    __tablename__ = "polls"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)

class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, index=True)
    poll_id = Column(Integer, ForeignKey("polls.id"), nullable=False)
    text = Column(String(255), nullable=False)
    votes = Column(Integer, default=0)