from model import User, ScheduledEvent, Event

#User crud functions

def create_user(fname, lname, username, email, password):
    
    user = User(fname = fname, 
            lname = lname, 
            username = username, 
            email = email,
            password = password)
    
    return user

#Event crud functions
def schedule_event(user_id, event_id, weekday, month, date, event_start_time, event_end_time): 
    
    scheduled_event = ScheduledEvent(user_id = user_id, 
            event_id = event_id, 
            weekday = weekday,
            month = month,
            date = date,
            event_start_time = event_start_time, 
            event_end_time = event_end_time)
    
    return scheduled_event

#Day crud functions
def create_event(name, location, description): 
    day = Event(name = name,
            location = location, 
            description = description)
    
    return day
