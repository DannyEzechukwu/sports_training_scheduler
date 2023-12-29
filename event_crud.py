from model import db, connect_to_db, Event

def create_event(name, location, description, coach_id): 
    
    event = Event(name = name,
                location = location, 
                description = description,
                coach_id = coach_id)
    
    return event

def get_event_by_id(id): 
    return Event.query.get(id)

def all_events(): 
    return Event.query.all()