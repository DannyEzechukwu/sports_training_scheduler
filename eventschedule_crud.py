from model import db, connect_to_db, EventSchedule

import datetime

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
    # Query for all events in database
    scheduled_events = all_scheduled_events()

    # List comp to get events between dates using datetime objects
    # List comp is a life saver
    events_to_select = [i for i in scheduled_events if datetime.datetime(i.year, i.month, i.date) <= 
                    datetime.datetime(end_year, end_month, end_date) and
                    datetime.datetime(i.year, i.month, i.date) >= datetime.datetime(start_year, start_month, start_date)]
    
    return events_to_select
    
    
