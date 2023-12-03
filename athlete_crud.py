from model import db, connect_to_db, Athlete

def create_athlete(fname, lname, username, email, password):
    
    user = Athlete(fname = fname, 
            lname = lname, 
            username = username, 
            email = email,
            password = password)
    
    return user

def get_athlete_by_username_and_password(username, password): 
     return Athlete.query.filter((Athlete.username == username) & (Athlete.password == password)).first()

def get_athlete_by_id(id): 
     return Athlete.query.get(id)
 
def get_athlete_by_email(email): 
     return Athlete.query.filter((Athlete.email == email)).first() 

def get_athlete_by_username(username): 
     return Athlete.query.filter((Athlete.username == username)).first() 