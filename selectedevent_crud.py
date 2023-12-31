from model import db, connect_to_db, SelectedEvent

def select_event(athlete_id, coach_id, event_schedule_id): 
    
    selected_event = SelectedEvent(athlete_id = athlete_id,
               coach_id = coach_id, 
               event_schedule_id = event_schedule_id)
    
    return selected_event

def get_selectedevent_by_id(id): 
    return SelectedEvent.query.get(id)

def all_selectedevents(): 
    SelectedEvent.query.all()

def get_selectedevent_by_event_schedule_id(event_schedule_id): 
    return SelectedEvent.query.filter(SelectedEvent.event_schedule_id == event_schedule_id).first()