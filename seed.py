""""Seed Training database with Users and events"""

import os
import model
import athlete_crud
import coach_crud
import event_crud
import selectedevent_crud
import eventschedule_crud
import server

from datetime import datetime, timedelta
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
]

app_events = [
    { "name" : "Football Training (Edge / ILB)",
    "location" : "Mustang-Panther Stadium 2909 Ira E Woods Ave, Grapevine, TX 76051",
    "description" : "Ladder/cone agility, Speed work, Position specific drills",
    "coach_id" : 1
    },

    { "name" : "Basketball Training (All Positions)",
    "location" : "Grapevine Rec Main Gym - 1175 Municipal Way, Grapevine, TX 76051",
    "description" : "Ball handling, Shooting, Conditioning",
    "coach_id" : 2
    },

    { "name" : "Baseball Training (Infield / Outfield)",
    "location" : "Oak Grove Baseball Complex Field H - 2520 Oak Grove Loop S, Grapevine, TX 76051",
    "description" : "Fielding, Hitting, Speed work",
    "coach_id" : 3
    },

    { "name" : "General Workout",
    "location": "Grapevine Rec Fitness Center - 1175 Municipal Way, Grapevine, TX 76051",
    "description" : "Upper body lift, Lower body lift, Auxileries (biceps, triceps, calves, etc.)",
    "coach_id" : 4
    }
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
for coach in coach_accounts: 
    print(coach)

#EVENTS
events = []
for event in app_events:
    event_type = event_crud.create_event(event['name'], 
            event["location"], 
            event["description"], 
            event["coach_id"]) 
    
    events.append(event_type)
    model.db.session.add_all(events)
    model.db.session.commit()

#Confirmation events have been added
for event in events: 
    print(event, "\n")

#EVENT SCHEDULE
#Time interval container
time_intervals = []

#Loop to add hour long time intervals from 9: AM to 5:00 PM
for i in range (9, 17):
    if i < 11: 
        time_intervals.append((f"{str(i)}:00 AM", f"{str(i + 1)}:00 AM"))
    elif i == 11: 
        time_intervals.append(("11:00 AM", "12:00 PM"))
    elif i == 12: 
        time_intervals.append(("12:00 PM", "1:00 PM"))
    else: 
        time_intervals.append((f"{str(i - 12)}:00 PM", f"{str(i - 11) }:00 PM"))
    
# print(time_intervals)

start_date = datetime(2023, 11,  27)
end_date = datetime(2024, 6, 30)
delta = timedelta(days = 1)

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
    month = individual_date_list[0]
    date = individual_date_list[1]
    year = individual_date_list[2]
    
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

#Confirmation event schedule has been created
for event in event_schedule: 
    print(event)













        
    
