from model import db, connect_to_db, SelectedEvent

def select_event(athlete_id, coach_id, event_schedule_id): 
    
    selected_event = SelectedEvent(athlete_id = athlete_id,
               coach_id = coach_id, 
               event_schedule_id = event_schedule_id)
    
    return selected_event