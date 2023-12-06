from model import db, connect_to_db, Athlete, Event, Feedback

import datetime

# Will use to seperate athletes schedule into events that have passed,
# events that are scheduled today, and events that are scheduled in the future
# Output is in YYYY-MM-DD
current_date = datetime.datetime.now().date()
# print(current_date)


def create_athlete(fname, lname, username, email, password):
    
    user = Athlete(fname = fname, 
            lname = lname, 
            username = username, 
            email = email,
            password = password)
    
    return user

def all_athletes(): 
     return Athlete.query.all()

def get_athlete_by_username_and_password(username, password): 
     return Athlete.query.filter((Athlete.username == username) & (Athlete.password == password)).first()

def get_athlete_by_id(id): 
     return Athlete.query.get(id)
 
def get_athlete_by_email(email): 
     return Athlete.query.filter((Athlete.email == email)).first() 

def get_athlete_by_username(username): 
     return Athlete.query.filter((Athlete.username == username)).first()

def athlete_past_present_future_events(id): 
     past_events = []
     current_events = []
     future_events = []
     # Get athlete by id
     athlete = Athlete.query.get(id)
     # Get the list of events the athlete has selected using the
     # selected_events relationship variable
     athlete_selected_events = athlete.selected_events
     # Loop[ through the events in the athlete has selected]
     for event in athlete_selected_events: 
          # Get the EventSchedule object using the selection relationship variable
          event_on_schedule = event.selection
          # Set a condition for if match is found
          if event_on_schedule: 
               # Use necessary attributes from class to create a date
               # object that will be compared to today
               year = event_on_schedule.year
               month = event_on_schedule.month
               date = event_on_schedule.date
               date_for_event_on_schedule = datetime.date(year, month, date)
               # Check if current date is greater than the date of the
               # event we found
               if current_date > date_for_event_on_schedule: 
                    past_events.append({
                         "athlete": get_athlete_by_id(event.athlete_id).fname,
                         "coach" : f"Coach {event.coach.fname}",
                         "event" : Event.query.get(event_on_schedule.event_id).name,
                         "description": Event.query.get(event_on_schedule.event_id).description, 
                         "date": f"{event_on_schedule.month}/{event_on_schedule.date}/{event_on_schedule.year}", 
                         "start_time" : f"{event_on_schedule.start_time}",
                         "end_time" : f"{event_on_schedule.start_time}",
                         "duration" : f"{event_on_schedule.start_time} - {event_on_schedule.end_time}",
                         "feedback" : f"{Feedback.query.filter(Feedback.selected_event_id == event.id).first().feedback}"
                    })
               elif current_date < date_for_event_on_schedule: 
                    future_events.append({
                         "athlete": get_athlete_by_id(event.athlete_id).fname,
                         "coach" : f"Coach {event.coach.fname}",
                         "event" : Event.query.get(event_on_schedule.event_id).name,
                         "description": Event.query.get(event_on_schedule.event_id).description, 
                         "date": f"{event_on_schedule.month}/{event_on_schedule.date}/{event_on_schedule.year}", 
                         "start_time" : f"{event_on_schedule.start_time}",
                         "end_time" : f"{event_on_schedule.start_time}",
                         "duration" : f"{event_on_schedule.start_time} - {event_on_schedule.end_time}"
                    })
               else: 
                    current_events.append({
                         "athlete": get_athlete_by_id(event.athlete_id).fname,
                         "coach" : f"Coach {event.coach.fname}",
                         "event" : Event.query.get(event_on_schedule.event_id).name,
                         "description": Event.query.get(event_on_schedule.event_id).description, 
                         "date": f"{event_on_schedule.month}/{event_on_schedule.date}/{event_on_schedule.year}", 
                         "start_time" : f"{event_on_schedule.start_time}",
                         "end_time" : f"{event_on_schedule.start_time}",
                         "duration" : f"{event_on_schedule.start_time} - {event_on_schedule.end_time}"
                    })

     return past_events, current_events, future_events


     
