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


#User Table
class User(db.Model): 
    
    __tablename__ = "users"

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
    
    #User can schedule many events
    events = db.relationship("ScheduledEvent", back_populates = "user")
    
    def __repr__(self): 
        return f"<User{self.id} username : {self.username} email: {self.email}>"
    

#ScheduledEvent Table
class ScheduledEvent(db.Model): 
    
    __tablename__ = "scheduled_events"

    id = db.Column(db.Integer, 
                primary_key = True,
                index = True)
    
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("users.id"), 
                        nullable = False, 
                        index = True)
    
    event_id = db.Column(db.Integer, 
                        db.ForeignKey("events.id"),
                        index = True)

    weekday = db.Column(db.String, 
                index = True, 
                nullable = False)
    
    month = db.Column(db.String, 
                    index = True, 
                    nullable = False)
    
    date = db.Column(db.Integer, 
                    index = True, 
                    nullable = False)
    
    event_start_time = db.Column(db.String,
                        nullable = False,
                        index = True)
    
    event_end_time = db.Column(db.String,
                        nullable = False,
                        index = True)
    
    #1 scheduled event can be scheduled by 1 user
    user = db.relationship("User", back_populates = "events")

    #1 scheuled event can contain 1 event
    event = db.relationship("Event", back_populates = "events")
    
    def __repr__(self): 
        return f"<Event{self.event_id} - {self.weekday}- {self.event_description}>"


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
    

    #1 type of event can be schedule ,many times
    events = db.relationship("ScheduledEvent", back_populates = "event")

    def __repr__(self): 
        return f"<Event{self.id} - {self.name}, {self.description}>"

   
if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app, echo=False)