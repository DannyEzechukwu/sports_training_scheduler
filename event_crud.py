from model import db, connect_to_db, Event

def create_event(name, location, description, coach_id): 
    
    event = Event(name = name,
                location = location, 
                description = description,
                coach_id = coach_id)
    
    return event