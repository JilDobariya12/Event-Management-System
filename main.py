from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import crud, models
from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from sqlalchemy import text
from models import Event
from fastapi import HTTPException

# create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Event Management API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- Helpers ----------
def resync_sequences():
    # Resync serial sequences to avoid duplicate key errors after imports
    seqs = [
        ("attendee", "attendee_id"),
        ("venue", "venue_id"),
        ("event", "event_id"),
    ]
    with engine.connect() as conn:
        trans = conn.begin()
        for table, col in seqs:
            # set sequence to max(col)+1 or 1 if empty
            sql = text(
                f"SELECT setval(pg_get_serial_sequence('{table}','{col}'), COALESCE((SELECT MAX({col}) FROM {table})+1, 1), false)"
            )
            try:
                conn.execute(sql)
            except Exception:
                # ignore if sequence/table doesn't exist yet
                pass
        trans.commit()

# resync sequences at startup (safe; silently continues if tables not present)
resync_sequences()

class AttendeeInput(BaseModel):
    name: str
    type: str
    payment_status: str

class VenueInput(BaseModel):
    name: str
    layout: str
    capacity: int
    security_id: int
    design_id: int

class EventInput(BaseModel):
    event_name: str
    date_time: str   # accept string ISO, we'll parse
    venue_id: int
    volunteer_id: Optional[int] = None
    finance_id: Optional[int] = None

@app.get("/attendees")
def read_attendees(db: Session = Depends(get_db)):
    return crud.get_attendees(db)

@app.post("/attendees")
def create_attendee(data: AttendeeInput, db: Session = Depends(get_db)):
    return crud.create_attendee(db, data.name, data.type, data.payment_status)

@app.delete("/attendees/{attendee_id}")
def delete_attendee(attendee_id: int, db: Session = Depends(get_db)):
    return crud.delete_attendee(db, attendee_id)

@app.get("/venues")
def read_venues(db: Session = Depends(get_db)):
    return crud.get_venues(db)

@app.post("/venues")
def create_venue(data: VenueInput, db: Session = Depends(get_db)):
    return crud.create_venue(db, data.name, data.layout, data.capacity, data.security_id, data.design_id)

@app.get("/events")
def read_events(db: Session = Depends(get_db)):
    return crud.get_events(db)

@app.post("/events")
def create_event(data: EventInput, db: Session = Depends(get_db)):
    # debug print to help you see inputs in terminal
    print("Received event data:", data.dict())
    try:
        # Parse datetime robustly
        try:
            dt = datetime.fromisoformat(data.date_time)
        except Exception:
            dt = datetime.strptime(data.date_time, "%Y-%m-%dT%H:%M:%S")
        new_event = crud.create_event(db, data.event_name, dt, data.venue_id, data.volunteer_id, data.finance_id)
        print("Event created:", new_event.event_name)
        return new_event
    except Exception as e:
        import traceback
        print("ERROR CREATING EVENT:", e)
        traceback.print_exc()
        # Return useful error JSON to frontend
        return {"error": str(e)}

# @app.delete("/events/{event_id}")
# def delete_event(event_id: int, db: Session = Depends(get_db)):
#     # Fetch the event by primary key
#     event = db.query(Event).filter(Event.event_id == event_id).first()
#     if not event:
#         raise HTTPException(status_code=404, detail="Event not found")
#
#     # Delete and commit
#     db.delete(event)
#     db.commit()
#     return {"message": f"Event '{event.event_name}' deleted successfully!"}

#main.py: The FastAPI entry point — defines all API endpoints that call CRUD functions.
#ALTER TABLE event ALTER COLUMN event_id SET DEFAULT nextval('event_event_id_seq');
