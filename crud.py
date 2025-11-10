from sqlalchemy.orm import Session
from models import Attendee, Venue, Event

# ----- Attendee -----
def get_attendees(db: Session):
    return db.query(Attendee).all()

def create_attendee(db: Session, name: str, type: str, payment_status: str):
    attendee = Attendee(name=name, type=type, payment_status=payment_status)
    db.add(attendee)
    db.commit()
    db.refresh(attendee)
    return attendee

def delete_attendee(db: Session, attendee_id: int):
    attendee = db.query(Attendee).filter(Attendee.attendee_id == attendee_id).first()
    if attendee:
        db.delete(attendee)
        db.commit()
    return attendee

# ----- Venue -----
def get_venues(db: Session):
    return db.query(Venue).all()

def create_venue(db: Session, name: str, layout: str, capacity: int, security_id=None, design_id=None):
    venue = Venue(venue_name=name, layout=layout, capacity=capacity,
                  security_id=security_id, design_id=design_id)
    db.add(venue)
    db.commit()
    db.refresh(venue)
    return venue

# ----- Event -----
def get_events(db: Session):
    return db.query(Event).all()

def create_event(db: Session, event_name: str, date_time, venue_id: int, volunteer_id=None, finance_id=None):
    event = Event(
        event_name=event_name,
        date_time=date_time,
        venue_id=venue_id,
        volunteer_id=volunteer_id,
        finance_id=finance_id
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

#crud.py: Contains database functions — create, read, update, delete (CRUD operations).