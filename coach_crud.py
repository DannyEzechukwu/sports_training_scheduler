from model import db, connect_to_db,Athlete, Coach, Event, Feedback, EventSchedule

import datetime

# Will use to seperate coach's schedule into events that have passed,
# events that are scheduled today, and events that are scheduled in the future
# Output is in YYYY-MM-DD
current_date = datetime.datetime.now().date()
# print(current_date)

def create_coach(fname, lname, username, email, password):
     coach = Coach(fname = fname, 
                lname = lname, 
                username = username, 
                email = email,
                password = password)
     return coach

def get_coach_by_id(id): 
     return Coach.query.get(id)

def all_coaches(): 
     return Coach.query.all()

def get_coach_by_email(email):
     return Coach.query.filter((Coach.email == email)).first()

def get_coach_by_username(username): 
     return Coach.query.filter((Coach.username == username)).first()

def get_coach_by_fname(fname):
     return Coach.query.filter((Coach.fname == fname)).first()

def get_coach_by_username_and_password(username, password): 
     return Coach.query.filter((Coach.username == username) & (Coach.password == password)).first()

def coach_past_present_future_events_by_id(id): 
     past_events = []
     current_events = []
     future_events = []
     # Get coach by id
     coach = Coach.query.get(id)
     # Get the list of events the coach has selected for using the
     # events relationship variable
     coach_selected_events = coach.events
    
     # Loop through the events the coach has been selected for
     for event in coach_selected_events:
          # Get the EventSchedule object using the event_schedule_id attribute
          event_on_schedule_id = event.event_schedule_id
          # Apply filter for the first eevent returned from EventSchedule class
          # matching the EventSchedule OID
          event_on_schedule = EventSchedule.query.filter(EventSchedule.id == event_on_schedule_id).first()
          
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
                         "athlete": Athlete.query.get(event.athlete_id).fname,
                         "event" : Event.query.get(event_on_schedule.event_id).name,
                         "location" : Event.query.get(event_on_schedule.event_id).location,
                         "description": Event.query.get(event_on_schedule.event_id).description, 
                         "date": date_for_event_on_schedule, 
                         "display_date" : date_for_event_on_schedule.strftime("%m/%d/%Y"),
                         "start_time" : f"{event_on_schedule.start_time}",
                         "start_time_object": datetime.datetime.strptime(event_on_schedule.start_time, '%I:%M %p').time(),
                         "end_time" : f"{event_on_schedule.start_time}",
                         "duration" : f"{event_on_schedule.start_time} - {event_on_schedule.end_time}",
                         "feedback" : event.feedback_message.feedback,
                         "feedback_id" : event.feedback_message.id
                    })
               elif current_date < date_for_event_on_schedule: 
                    future_events.append({
                         "athlete": Athlete.query.get(event.athlete_id).fname,
                         "event" : Event.query.get(event_on_schedule.event_id).name,
                         "location" : Event.query.get(event_on_schedule.event_id).location,
                         "description": Event.query.get(event_on_schedule.event_id).description, 
                         "date": date_for_event_on_schedule, 
                         "display_date" : date_for_event_on_schedule.strftime("%m/%d/%Y"),
                         "start_time" : f"{event_on_schedule.start_time}",
                         "start_time_object": datetime.datetime.strptime(event_on_schedule.start_time, '%I:%M %p').time(),
                         "end_time" : f"{event_on_schedule.start_time}",
                         "duration" : f"{event_on_schedule.start_time} - {event_on_schedule.end_time}"
                    })
               else: 
                    current_events.append({
                         "athlete": Athlete.query.get(event.athlete_id).fname,
                         "coach" : f"Coach {event.coach.fname}",
                         "event" : Event.query.get(event_on_schedule.event_id).name,
                         "location" : Event.query.get(event_on_schedule.event_id).location,
                         "description": Event.query.get(event_on_schedule.event_id).description, 
                         "date": date_for_event_on_schedule, 
                         "display_date" : date_for_event_on_schedule.strftime("%m/%d/%Y"),
                         "start_time" : f"{event_on_schedule.start_time}",
                         "start_time_object": datetime.datetime.strptime(event_on_schedule.start_time, '%I:%M %p').time(),
                         "end_time" : f"{event_on_schedule.start_time}",
                         "duration" : f"{event_on_schedule.start_time} - {event_on_schedule.end_time}"
                    })

     return past_events, current_events, future_events
