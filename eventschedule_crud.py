from model import db, connect_to_db, EventSchedule

def schedule_event(event_id, month, date, year, start_time, end_time): 
    
    scheduled_event = EventSchedule(event_id = event_id, 
                month = month, 
                date = date, 
                year = year, 
                start_time = start_time, 
                end_time = end_time)
    
    return scheduled_event