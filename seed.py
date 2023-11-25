""""Seed Training database with Users and events"""

import os
import crud
import model
import server

os.system("dropdb training")
os.system("createdb training")

model.connect_to_db(server.app)
model.db.create_all()

app_users = {
    "user1" : {"fname" : "Tyson", 
        "lname": "Chandler",
        "username" : "tchandler",
        "email" : "tchandler@gmail.com",
        "password" : "test"},
    
    "user2" : {"fname" : "Mary", 
        "lname": "Walters",
        "username" : "mwalters",
        "email" : "mwalters@gmail.com",
        "password" : "test"},
  
    "user3" : {"fname" : "Justin", 
        "lname": "Mabin",
        "username" : "jmabin",
        "email" : "jmabin@gmail.com",
        "password" : "test"},
    
    "user4" : {"fname" : "Kevin", 
        "lname": "Sumner",
        "username" : "ksumner",
        "email" : "ksumner@gmail.com",
        "password" : "test"},

    "user5" : {"fname" : "Taylor", 
        "lname": "Bradford",
        "username" : "tbradford",
        "email" : "tbradford@gmail.com",
        "password" : "test"},
}

app_events = {
    "event1" : { "name" : "Football Training (Edge / ILB)",
        "location" : "Grapevine Rec Turf Field - 1175 Municipal Way, Grapevine, TX 76051",
        "description" : "Ladder/cone agility\nSpeed work\nPosition specific drills",
    },

    "event2" : { "name" : "Basketball Training (All Positions)",
    "location" : "Grapevine Rec Main Gym - 1175 Municipal Way, Grapevine, TX 76051",
    "description" : "Ball handling\nShooting\nConditioning",
    },

    "event3" : { "name" : "Baseball Training (Infield / Outfield)",
    "location" : "Oak Grove Baseball Complex Field H - 2520 Oak Grove Loop S, Grapevine, TX 76051",
    "description" : "Fielding\nHitting\nSpeed work",
    },

    "event4" : { "name" : "General Workout",
    "location": "Grapevine Rec Fitness Center - 1175 Municipal Way, Grapevine, TX 76051",
    "description" : "Upper body lift\nLower body lift\nAuxileries (biceps, triceps, calves, etc.)",
    },

}

#Create users
user_accounts = []
for user in app_users:

    user_account = crud.create_user(app_users[user]['fname'], 
                app_users[user]["lname"], 
                app_users[user]["username"], 
                app_users[user]["email"], 
                app_users[user]["password"])
    
    user_accounts.append(user_account)
    model.db.session.add_all(user_accounts)
    model.db.session.commit()


#Confirmation that users have been added
for account in user_accounts: 
    print(f"{account} \n")

#Create events
events = []
for event in app_events:

    event_type = crud.create_event(app_events[event]['name'], 
                app_events[event]["location"], 
                app_events[event]["description"]) 
    
    events.append(event_type)
    model.db.session.add_all(events)
    model.db.session.commit()


#Confirmation that users have been added
for event in events: 
    print(event)

    
