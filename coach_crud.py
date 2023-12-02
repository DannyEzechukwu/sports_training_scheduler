from model import db, connect_to_db, Coach

def create_coach(fname, lname, username, email, password):
     coach = Coach(fname = fname, 
                lname = lname, 
                username = username, 
                email = email,
                password = password)
     return coach

def get_coach_by_username_and_password(username, password): 
     return Coach.query.filter((Coach.username == username) & (Coach.password == password)).first()

def get_coach_by_id(id): 
     return Coach.query.get(id)