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
    events = db.relationship("Event", back_populates = "user")
    
    def __repr__(self): 
        return f"<User{self.id} {self.username} {self.email}"
    

#Event Table
class Event(db.Model): 
    
    __tablename__ = "events"

    id = db.Column(db.Integer, 
                primary_key = True,
                index = True)
    
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("users.id"), 
                        nullable = False, 
                        index = True)
    
    event_name = db.Column(db.String, 
                           nullable = False,
                           index = True)
    
    event_description = db.Column(db.String, 
                            nullable = False,
                            index = True)
    
    #One event can belong to only one one user
    user = db.relationship("User", back_populates = "events")

    #One event can belong to only one day
    day = db.relationship("Day", back_populates = "events")

    #One event can only be held at one time
    time = db.relationship("Time", back_populates="event", uselist=False)
    
    
    def __repr__(self): 
        return f"<Event{self.id} {self.event_name} - {self.event_description}>"
    

#Month Table
class Month(db.Model): 
    __tablename__ = "months"

    id = db.Column(db.Integer, 
                primary_key = True,
                index = True)
    
    month_name = db.Column(db.String, 
                        nullable = False, 
                        index = True)
    
    #One month can have several days
    days = db.relationship("Day", back_populates = "month")
    
    def __repr__(self): 
        return f"<Month{self.id} - {self.month_name}>"
    

#Day Table
class Day(db.Model): 
    __tablename__ = "days"

    id = db.Column(db.Integer, 
                primary_key = True,
                index = True)
    
    month_id = db.Column(db.Integer,
                        db.ForeignKey("months.id"),
                        index = True)
    
    day_name = db.Column(db.String,
                        nullable = False, 
                        index = True)
    
    day_number= db.Column(db.Integer,
                        nullable = False, 
                        index = True)
    
    event_id = db.Column(db.Integer,
                        db.ForeignKey("events.id"), 
                        index = True)
    
    #One day can belong to only one month
    month = db.relationship("Month", back_populates = "days") 

    #One day can contain many events
    events = db.relationship("Event", back_populates = "day")

    #One day can contain many times 
    times = db.relationship("Time", back_populates = "day" )

    def __repr__(self): 
        return f"<{self.month_id}/{self.day_number} - {self.event_id}>"

    
#Time Table
class Time(db.Model): 
    __tablename__ = "times"

    id = db.Column(db.Integer,
                   primary_key = True, 
                   index = True)
    
    day_id = db.Column(db.Integer, 
                    db.ForeignKey("days.id"), 
                    index = True)
    
    event_id = db.Column(db.Integer, 
                    db.ForeignKey("events.id"), 
                    index = True)
    
    start_time  = db.Column(db.String, 
                        index = True)
    
    end_time = db.Column(db.String, 
                        index = True)
    
    #A single time could only belong to one day
    day = db.relationship("Day", back_populates = "times")

    #A single time belongs to one event
    event = db.relationship("Event", back_populates="time")
    
    def __repr__(self): 
        return f"<Event{self.event_id}: {self.start_time} - {self.end_time}>"


    
if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app, echo=False)