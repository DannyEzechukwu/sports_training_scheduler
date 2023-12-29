""""Seed Training database with Users and events"""

import os
import model
import athlete_crud
import coach_crud
import event_crud
import eventschedule_crud
import selectedevent_crud
import feedback_crud
import server

import datetime
import random

os.system("dropdb training")
os.system("createdb training")

model.connect_to_db(server.app)
model.db.create_all()

#ARTIFICIAL DATA
app_athletes = [
        {"fname" : "Tyson", 
        "lname": "Chandler",
        "username" : "tchandler",
        "email" : "tchandler@gmail.com",
        "password" : "test"} ,
    
        {"fname" : "Mary", 
        "lname": "Walters",
        "username" : "mwalters",
        "email" : "mwalters@gmail.com",
        "password" : "test"} ,
  
        {"fname" : "Justin", 
        "lname": "Mabin",
        "username" : "jmabin",
        "email" : "jmabin@gmail.com",
        "password" : "test"} ,
    
        {"fname" : "Kevin", 
        "lname": "Sumner",
        "username" : "ksumner",
        "email" : "ksumner@gmail.com",
        "password" : "test"} ,

        {"fname" : "Taylor", 
        "lname": "Bradford",
        "username" : "tbradford",
        "email" : "tbradford@gmail.com",
        "password" : "test"} , 

        {"fname" : "Reneé", 
        "lname": "Stewart",
        "username" : "rstewart",
        "email" : "rstewart@gmail.com",
        "password" : "test"} ,

        {"fname" : "Marcus", 
        "lname": "Nelson",
        "username" : "mnelson",
        "email" : "mnelson@gmail.com",
        "password" : "test"} ,

        {"fname" : "Tenita", 
        "lname": "Thomas",
        "username" : "tthomas",
        "email" : "tthomas@gmail.com",
        "password" : "test"} ,
    
        {"fname" : "Niles", 
        "lname": "Taylor",
        "username" : "ntaylor",
        "email" : "ntaylor@gmail.com",
        "password" : "test"} ,   

        {"fname" : "Aubrey", 
        "lname": "Adams",
        "username" : "aadams",
        "email" : "aadams@gmail.com",
        "password" : "test"} 
]

app_coaches = [
        {"fname" : "Corey", 
        "lname": "Brooks",
        "username" : "cbrooks",
        "email" : "cbrooks@gmail.com",
        "password" : "test"} ,
    
        {"fname" : "Zrah", 
        "lname": "Meyers",
        "username" : "zmeyers",
        "email" : "zmeyers@gmail.com",
        "password" : "test"} ,
  
        {"fname" : "Dustin", 
        "lname": "Ingram",
        "username" : "dingram",
        "email" : "dingram@gmail.com",
        "password" : "test"} ,
    
        {"fname" : "Amaal", 
        "lname": "Richards",
        "username" : "arichards",
        "email" : "arichards@gmail.com",
        "password" : "test"} ,

        {"fname" : "Rhianna", 
        "lname": "Burgess",
        "username" : "rburgess",
        "email" : "rburgess@gmail.com",
        "password" : "test"} 
]

app_events = [
    { "name" : "Football Training (Edge / ILB)",
    "location" : "Mustang-Panther Stadium 2909 Ira E Woods Ave, Grapevine, TX 76051",
    "description" : "Ladder/cone agility, Speed work, Position specific drills",
    },

    { "name" : "Basketball Training (All Positions)",
    "location" : "Grapevine Rec Main Gym - 1175 Municipal Way, Grapevine, TX 76051",
    "description" : "Ball handling, Shooting, Defensive drills, Conditioning",
    },

    { "name" : "Baseball Training (Infield / Outfield)",
    "location" : "Oak Grove Baseball Complex Field H - 2520 Oak Grove Loop S, Grapevine, TX 76051",
    "description" : "Fielding, Hitting, Speed work",
    },

    { "name" : "Volleyball Training (All Positions)",
    "location" : "Grapevine Rec Secondary Gym - 1175 Municipal Way, Grapevine, TX 76051",
    "description" : "Serving, Setting, Defense, Plyometrics",
    },

    { "name" : "Soccer Training (All Positions)",
    "location" : "Oak Grove Soccer Complex Field 4 - 1299 Oak Grove Loop North, Grapevine, TX 76051",
    "description" : "Ball Handling, Passsing, Goal Keeping",
    },

    { "name" : "General Workout",
    "location": "Grapevine Rec Fitness Center - 1175 Municipal Way, Grapevine, TX 76051",
    "description" : "Upper body lift, Lower body lift, Auxileries (biceps, triceps, calves, etc.)",
    }
]

coach_feedback_messages = [
    
    "Great job outh there! I can really tell you are working hard outside of our sessions.",

    "Make sure you bring water to every session. Hydration is key!", 

    "Your movements are starting to look more explosive. Keep working!", 

    "Don't sweat it. The next session will be better. Keep your head up.", 

    "Really enjoyed working with you at today's session. Great job.",

    "The effort you gave today was not your best. Let's get after it next time!",

    "Be sure to come with some areas of concern you want to see improvement in so we can develop a solid plan of attack.", 

    "Massive improvement since we began working with another. I am proud of you!",

    "Let's make sure that we are consistent with every rep. Wanna make sure we are stacking good days.",

    "Solid session today. That's the way to get after it."
]

#ATHLETES
athlete_accounts = []
for athlete in app_athletes:

    athlete_account = athlete_crud.create_athlete(athlete['fname'], 
                athlete["lname"], 
                athlete["username"], 
                athlete["email"], 
                athlete["password"])
    
    athlete_accounts.append(athlete_account)
    model.db.session.add_all(athlete_accounts)
    model.db.session.commit()

#Confirmation that athlete  have been added
# for account in athlete_accounts: 
#     print(f"{account} \n")
#**********************************************************************

#COACHES
coach_accounts = []
for coach in app_coaches: 
    
    coach = coach_crud.create_coach(coach["fname"], 
                      coach["lname"], 
                      coach["username"], 
                      coach["email"],
                      coach["password"])
    
    coach_accounts.append(coach)
    model.db.session.add_all(coach_accounts)
    model.db.session.commit()

#Confirmation coaches have been added
# for coach in coach_accounts: 
#     print(coach)
#*****************************************************************

#EVENTS
events = []
for event in app_events:
    event_type = event_crud.create_event(event['name'], 
            event["location"], 
            event["description"]) 
    
    events.append(event_type)
    model.db.session.add_all(events)
    model.db.session.commit()

#Confirmation events have been added
# for event in events: 
#     print(event, "\n")
#*********************************************************************

#EVENT SCHEDULE
#Time interval container
time_intervals = []

#Loop to add hour long time intervals from 9: AM to 3:00 PM
for i in range (9, 14):
    if i < 11: 
        time_intervals.append((f"{str(i)}:00 AM", f"{str(i + 1)}:00 AM"))
    elif i == 11: 
        time_intervals.append(("11:00 AM", "12:00 PM"))
    elif i == 12: 
        time_intervals.append(("12:00 PM", "1:00 PM"))
    else: 
        time_intervals.append((f"{str(i - 12)}:00 PM", f"{str(i - 11) }:00 PM"))
    
# print(time_intervals)

start_date = datetime.datetime(2023, 12, 11)
end_date = datetime.datetime(2024, 6, 30)
delta = datetime.timedelta(days = 1)

#Function to get days to schedule events
def generate_date_list(start_date, end_date, delta, separator = "/"):
    date_container = []

    current_date = start_date
    while current_date <= end_date:
        formatted_date = current_date.strftime(f'%m{separator}%d{separator}%Y')
        date_container.append(formatted_date)
        current_date += delta
    
    return date_container

date_list = generate_date_list(start_date, end_date, delta)

event_schedule = []
for date in date_list:

    #Gather date info for each date
    individual_date_list = date.split("/")
    month = int(individual_date_list[0])
    date = int(individual_date_list[1])
    year = int(individual_date_list[2])
    
    for i in range(3):
        #Get a random event object and its id
        event = random.choice(events)
        event_id = event.id

        #Grab a related start and end time 
        time_interval = random.choice(time_intervals)
        start_time = time_interval[0]
        end_time = time_interval[1]

        #Create EventSchedule object
        scheduled_event = eventschedule_crud.schedule_event(event_id,month, date, year, 
                                start_time, end_time)
        
        event_schedule.append(scheduled_event)

model.db.session.add_all(event_schedule)
model.db.session.commit()

# #Confirmation event schedule has been created
# for event in event_schedule: 
#     print(event)
#********************************************************************

#SELECTED EVENTS
selected_events = []
#Loop through each event in the event schedule list of objects from
# the EventSchedule class
for scheduled_event in event_schedule:
    #Identify today's date (MM/DD/YY)
    today = datetime.datetime.now().date()
    #identify the date of each object from the event_schedule list
    event_date = datetime.datetime(scheduled_event.year, scheduled_event.month, scheduled_event.date).date()
    
    #Condition for if an event is in the past 
    if event_date < today:
        #Select an athlete 
        athlete = random.choice(athlete_accounts)
        coach = random.choice(coach_accounts)

        selected_event = selectedevent_crud.select_event(athlete.id, coach.id, scheduled_event.id)
        selected_events.append(selected_event)

model.db.session.add_all(selected_events)
model.db.session.commit()

#Confirm selected events have been added 
# for event in selected_events: 
#     print(event)
#**************************************************************

#FEEDBACK
feedback_container = [] 

for athlete_selection in selected_events:
    feedback = feedback_crud.create_feedback_message(
        athlete_selection.id, 
        athlete_selection.coach_id,
        random.choice(coach_feedback_messages)
    ) 

    feedback_container.append(feedback)


model.db.session.add_all(feedback_container)
model.db.session.commit()


#Confirm feedback messages have been added 
# for feedback in feedback_container: 
#     print(feedback)













        
    
