from model import db, connect_to_db, SelectedEvent

def select_event(user_id, event_schedule_id, event_id): 
    
    selected_event = SelectedEvent(user_id = user_id,
                event_schedule_id = event_schedule_id, 
                event_id = event_id)
    
    return selected_event