""""Models for app"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_to_db(flask_app, db_uri="postgresql:///training", echo=False):
        flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        flask_app.config["SQLALCHEMY_ECHO"] = echo
        flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        db.app = flask_app
        db.init_app(flask_app)

        print("Connected to the db!")

#Athlete Table
class Athlete (db.Model): 
    
    __tablename__ = "athletes"

    id = db.Column(db.Integer, 
                primary_key = True,
                index = True)

    fname = db.Column(db.String, 
                    index = True, 
                    nullable = False)
    
    lname = db.Column(db.String,
                    index = True,
                    nullable = False)
    
    username = db.Column(db.String,
                    index = True,
                    nullable = False,
                    unique = True)
    
    email = db.Column(db.String,
                    index = True, 
                    nullable = False, 
                    unique = True)
    
    password = db.Column(db.String,
                    index = True, 
                    nullable = False)
    
    #Athlete can have multiple selected events
    selected_events = db.relationship("SelectedEvent", back_populates = "athlete")
    
    def __repr__(self): 
        return f"<Athlete ID : {self.id},  Username : {self.username},  Email: {self.email}>"
    

#Coach Table 
class Coach(db.Model): 
    __tablename__ = "coaches"

    id = db.Column(db.Integer, 
                primary_key = True,
                index = True)

    fname = db.Column(db.String, 
                index = True, 
                nullable = False)
    
    lname = db.Column(db.String,
                index = True,
                nullable = False)
    
    username = db.Column(db.String,
                index = True,
                nullable = False,
                unique = True)

    email = db.Column(db.String,
                index = True, 
                nullable = False, 
                unique = True)
    
    password = db.Column(db.String,
                index = True, 
                nullable = False)
    
    #ONLY 1 coach can be assigned to 1 event
    event = db.relationship('Event', uselist = False, back_populates = "coach")

    def __repr__(self): 
        return f"<Coach ID : {self.id},  Username : {self.username},  Email : {self.email}>"


#SelectedEvent Table
class SelectedEvent(db.Model): 
    
    __tablename__ = "selected_events"

    id = db.Column(db.Integer, 
                primary_key = True,
                index = True)
    
    athlete_id = db.Column(db.Integer, 
                        db.ForeignKey("athletes.id"), 
                        nullable = False, 
                        index = True)
    
    event_schedule_id = db.Column(db.Integer, 
                        db.ForeignKey("event_schedule.id"),
                        nullable = False,
                        index = True)
    
    event_id = db.Column(db.Integer, 
            db.ForeignKey("events.id"),
            nullable = False,
            index = True)

    #1 selected event can be owned by 1 athlete
    athlete  = db.relationship("Athlete", back_populates = "selected_events")

    #ONLY 1 selection can be made for a scheduled event
    selection = db.relationship('EventSchedule', uselist = False, back_populates = "specific_event_selected")

    def __repr__(self): 
        return f"<Athlete ID {self.user_id}, Scheduled Event ID : {self.event_schedule_id}, Event ID : {self.event_id} >"


#Event Table
class Event(db.Model): 
    __tablename__ = "events"

    id = db.Column(db.Integer, 
                primary_key = True,
                index = True)
    
    name = db.Column(db.String,
                        nullable = False, 
                        index = True)
    
    location = db.Column(db.String,
                nullable = False, 
                index = True)
    
    description = db.Column(db.String,
                        nullable = False,
                        index = True)
    
    coach_id = db.Column(db.Integer, 
                    db.ForeignKey("coaches.id"), 
                    nullable = False, 
                    index = True)

    #An event can be appear on the Schedule MANY times
    schedule_appearances = db.relationship("EventSchedule", back_populates = "specific_event_scheduled")

    #ONLY 1 event can be assigned to 1 coach
    coach = db.relationship('Coach', back_populates = "event")

    def __repr__(self): 
        return f"<Event ID : {self.id}, Event Name : {self.name}, Event Description : {self.description}>"


#Event Schedule Table
class EventSchedule(db.Model): 
    __tablename__ = "event_schedule"
    
    id = db.Column(db.Integer, 
        primary_key = True,
        index = True)
    
    event_id = db.Column(db.Integer, 
            db.ForeignKey("events.id"), 
            nullable = False, 
            index = True)
    
    month = db.Column(db.Integer, 
                    index = True, 
                    nullable = False)
    
    date = db.Column(db.Integer, 
                    index = True, 
                    nullable = False)

    year = db.Column(db.Integer, 
                index = True, 
                nullable = False)
    
    start_time = db.Column(db.String,
                        nullable = False,
                        index = True)
    
    end_time = db.Column(db.String,
                        nullable = False,
                        index = True)
    
    #A scheduled event can only contain 1 event from the Event table
    specific_event_scheduled = db.relationship("Event", back_populates = "schedule_appearances")

    #A scheduled event can ONLY be selected 1 time
    specific_event_selected = db.relationship("SelectedEvent", back_populates = "selection")

    def __repr__(self): 
        return f"<Event Schedule ID : {self.id}, Event ID : {self.event_id}, Date : {self.month}/{self.date}/{self.year}, Time : {self.start_time} - {self.end_time}>"
    

if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app, echo=False)