from model import User, SelectedEvent, Event, EventSchedule

#User crud functions

def create_user(fname, lname, username, email, password):
    
    user = User(fname = fname, 
            lname = lname, 
            username = username, 
            email = email,
            password = password)
    
    return user

#SelectedEvent crud functions
def select_event(user_id, event_schedule_id, event_id): 
    
    selected_event = SelectedEvent(user_id = user_id,
                event_schedule_id = event_schedule_id, 
                event_id = event_id)
    
    return selected_event

#Event crud functions
def create_event(name, location, description): 
    
    event = Event(name = name,
                location = location, 
                description = description)
    
    return event

#Event Schedule crud functions
def schedule_event(event_id, weekday, month, date, year, start_time, end_time): 
    
    scheduled_event = EventSchedule(event_id = event_id,
                weekday = weekday, 
                month = month, 
                date = date, 
                year = year, 
                start_time = start_time, 
                end_time = end_time)
    
    return scheduled_event
    
