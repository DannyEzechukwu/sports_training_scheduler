from model import db, connect_to_db, Athlete, Coach, Event, Feedback, EventSchedule, SelectedEvent

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

def athlete_rejected_events(athlete_id : int, month : int, date : int, year : int, start_time : str): 
    
     
     # Container to hold all rejected events that conflict with athletes schedule
     rejected = []

     # Get the athlete using the id passed in as paremeter
     # and get all of the events the athlete has selected
     athlete = get_athlete_by_id(athlete_id)
     athlete_selected_events = athlete.selected_events
     
     
     # Loop through the vents the athlete has selected
     for event in athlete_selected_events:
          
          # Get the EventSchedule object for each event the athlete selected
          selected_event_object = SelectedEvent.query.get(event.id)
          
          event_on_schedule = EventSchedule.query.filter(EventSchedule.id == selected_event_object.event_schedule_id).first()

          # Condition for if a elected event for athlete is
          # on the same date and starts at the same time as an 
          # event rendered from the schedule on the client
          if (
          event_on_schedule.month == month and
          event_on_schedule.date == date and
          event_on_schedule.year == year and
          event_on_schedule.start_time == start_time
          ):
               rejected.append(event_on_schedule)

     return rejected


def athlete_past_present_future_events_by_id(id): 
     past_events = []
     current_events = []
     future_events = []
     # Get athlete by id
     athlete = Athlete.query.get(id)
     # Get the list of events the athlete has selected using the
     # selected_events relationship variable
     athlete_selected_events = athlete.selected_events
     # Loop through the events in the athlete has selected
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
               date_for_event_on_schedule = datetime.datetime(year, month, date).date()
               # Check if current date is greater than the date of the
               # event we found
               if current_date > date_for_event_on_schedule: 
                    past_events.append({
                         "athlete": get_athlete_by_id(event.athlete_id).fname,
                         "coach" : f"Coach {event.coach.fname}",
                         "event" : Event.query.get(event_on_schedule.event_id).name,
                         "location" : Event.query.get(event_on_schedule.event_id).location,
                         "description": Event.query.get(event_on_schedule.event_id).description, 
                         "date": date_for_event_on_schedule,
                         "display_date" : date_for_event_on_schedule.strftime("%m/%d/%Y"),
                         "start_time_object": datetime.datetime.strptime(event_on_schedule.start_time, '%I:%M %p').time(),
                         "start_time" : f"{event_on_schedule.start_time}",
                         "end_time" : f"{event_on_schedule.end_time}",
                         "duration" : f"{event_on_schedule.start_time} - {event_on_schedule.end_time}",
                         "no_feedback": f"Awaiting feedback from Coach {event.coach.fname}",
                         "feedback" : event.feedback_message.feedback
                    })
               elif current_date < date_for_event_on_schedule: 
                    future_events.append({
                         "athlete": get_athlete_by_id(event.athlete_id).fname,
                         "coach" : f"Coach {event.coach.fname}",
                         "event" : Event.query.get(event_on_schedule.event_id).name,
                         "location" : Event.query.get(event_on_schedule.event_id).location,
                         "description": Event.query.get(event_on_schedule.event_id).description, 
                         "date": date_for_event_on_schedule, 
                         "display_date" : date_for_event_on_schedule.strftime("%m/%d/%Y"),
                         "start_time" : f"{event_on_schedule.start_time}",
                         "start_time_object": datetime.datetime.strptime(event_on_schedule.start_time, '%I:%M %p').time(),
                         "end_time" : f"{event_on_schedule.end_time}",
                         "duration" : f"{event_on_schedule.start_time} - {event_on_schedule.end_time}"
                    })
               else: 
                    current_events.append({
                         "athlete": get_athlete_by_id(event.athlete_id).fname,
                         "coach" : f"Coach {event.coach.fname}",
                         "event" : Event.query.get(event_on_schedule.event_id).name,
                         "location" : Event.query.get(event_on_schedule.event_id).location,
                         "description": Event.query.get(event_on_schedule.event_id).description, 
                         "date": date_for_event_on_schedule, 
                         "display_date" : date_for_event_on_schedule.strftime("%m/%d/%Y"),
                         "start_time" : f"{event_on_schedule.start_time}",
                         "start_time_object": datetime.datetime.strptime(event_on_schedule.start_time, '%I:%M %p').time(),
                         "end_time" : f"{event_on_schedule.end_time}",
                         "duration" : f"{event_on_schedule.start_time} - {event_on_schedule.end_time}"
                    })

     return past_events, current_events, future_events


     
