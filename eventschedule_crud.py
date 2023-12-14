from model import db, connect_to_db, EventSchedule

def schedule_event(event_id, month, date, year, start_time, end_time): 
    
    scheduled_event = EventSchedule(event_id = event_id, 
                month = month, 
                date = date, 
                year = year, 
                start_time = start_time, 
                end_time = end_time)
    
    return scheduled_event

def get_scheduled_event_by_id(id): 
    return EventSchedule.query.get(id)

def all_scheduled_events():
    return EventSchedule.query.all()

def events_by_month_date_year(month, date, year):
    return EventSchedule.query.filter((EventSchedule.month == month) &
                               (EventSchedule.date == date) &
                               (EventSchedule.year == year)).all()