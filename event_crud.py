from model import db, connect_to_db, Event

def create_event(name, location, description): 
    
    event = Event(name = name,
                location = location, 
                description = description)
    
    return event