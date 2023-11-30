from model import db, connect_to_db, User

def create_user(fname, lname, username, email, password):
    
    user = User(fname = fname, 
            lname = lname, 
            username = username, 
            email = email,
            password = password)
    
    return user

    
