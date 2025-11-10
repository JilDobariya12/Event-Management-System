from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from database import Base

class Attendee(Base):
    __tablename__ = "attendee"
    attendee_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    type = Column(String(50))
    payment_status = Column(String(20))

class Venue(Base):
    __tablename__ = "venue"
    venue_id = Column(Integer, primary_key=True, index=True)
    venue_name = Column(String(100), nullable=False)
    layout = Column(Text)
    capacity = Column(Integer)
    security_id = Column(Integer)
    design_id = Column(Integer)

class Event(Base):
    __tablename__ = "event"
    event_id = Column(Integer, primary_key=True, index=True)
    event_name = Column(String(100), nullable=False)
    date_time = Column(DateTime, nullable=False)
    venue_id = Column(Integer, ForeignKey("venue.venue_id"))
    volunteer_id = Column(Integer, nullable=True)
    finance_id = Column(Integer, nullable=True)

#models.py: Defines the structure of tables (Attendee, Venue, Event).