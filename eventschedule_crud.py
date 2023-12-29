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

def get_scheduled_event_by_event_id(event_id): 
    return EventSchedule.query.filter(EventSchedule.event_id == event_id).first()

def filter_events(start_month, start_date, start_year, end_month, end_date, end_year): 
    return EventSchedule.query.filter(
        (EventSchedule.month >= start_month) & 
        (EventSchedule.month <= end_month) &
        (EventSchedule.date >= start_date) &
        (EventSchedule.date <= end_date) &
        (EventSchedule.year >= start_year) &
        (EventSchedule.year <= end_year) 
    )
    
    
