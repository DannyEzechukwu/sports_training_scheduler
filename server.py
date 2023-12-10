from flask import Flask, render_template, request, flash, session, redirect, jsonify

from model import connect_to_db, db

import athlete_crud
import coach_crud
import event_crud
import selectedevent_crud
import eventschedule_crud
import feedback_crud

import os

import random

from jinja2 import StrictUndefined

app = Flask(__name__)

app.static_folder = 'static'

#Secret Key to enable session
app.secret_key = os.environ["APP_KEY"]
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage(): 
    return render_template("home.html")

#LOGIN FUNCTIONALITY
#Current Coach Login
@app.route("/coach_login/json", methods = ["POST"])
def coach_login():
    username = request.form.get("coach-username").strip()
    password = request.form.get("coach-password")
    coach = coach_crud.get_coach_by_username_and_password(username, password)

    if coach:
        session["id"] = coach.id
        coach = coach_crud.get_coach_by_id(session["id"])
        # Form validation handled on the front end
        return jsonify({"response" : "valid coach",
                        "id": coach.id,
                        "fname" : coach.fname,
                        "lname" : coach.lname})
    else: 
        return jsonify({"response" : "invalid"})

#Current Athlete Login
@app.route("/athlete_login/json", methods = ["POST"])
def athlete_login():
    username = request.form.get("athlete-username").strip()
    password = request.form.get("athlete-password")
    athlete = athlete_crud.get_athlete_by_username_and_password(username, password)

    if athlete:
        session["id"] = athlete.id
        athlete = athlete_crud.get_athlete_by_id(session["id"])
        # Form validation handled on the front end
        return jsonify({"response": "valid athlete",
                        "id": athlete.id,
                        "fname" : athlete.fname,
                        "lname" : athlete.lname})
    else:
        return jsonify({"response" : "invalid"})

#New Athlete Account Creation
@app.route("/new_athlete_account/json", methods = ["POST"])
def new_athlete(): 
    fname = request.form.get("new-athlete-fname").strip()
    lname = request.form.get("new-athlete-lname").strip()
    username = request.form.get("new-athlete-username").strip()
    email = request.form.get("new-athlete-email").strip()
    password = request.form.get("new-athlete-password")

    # See if athete username and/or athlete email already exists in database
    username_validation = athlete_crud.get_athlete_by_username(username)
    email_validation = athlete_crud.get_athlete_by_email(email)

    if fname and lname and username_validation == None and email_validation == None:
        athlete = athlete_crud.create_athlete(fname, lname, username, email, password)
        db.session.add(athlete)
        db.session.commit()
        session["id"] = athlete.id
        
        return jsonify({"response": "valid athlete",
                        "id": athlete.id,
                        "fname" : athlete.fname,
                        "lname" : athlete.lname})
    
    if username_validation: 
        return jsonify({"response" : "invalid username", 
            "message" : "Username is taken. Please enter a different username."})
    
    if email_validation: 
        return jsonify({"response" : "invalid email", 
            "message" : "Email is taken. Please enter a different email."})

        
#New Coach Account Creation
@app.route("/new_coach_account/json", methods = ["POST"])
def new_coach(): 
    fname = request.form.get("new-coach-fname").strip()
    lname = request.form.get("new-coach-lname").strip()
    username = request.form.get("new-coach-username").strip()
    email = request.form.get("new-coach-email").strip()
    password = request.form.get("new-coach-password")

    # See if athete username and/or athlete email already exists in database
    username_validation = coach_crud.get_coach_by_username(username)
    email_validation = coach_crud.get_coach_by_email(email)

    if fname and lname and username_validation == None and email_validation == None:
        coach = coach_crud.create_coach(fname, lname, username, email, password)
        db.session.add(coach)
        db.session.commit()
        session["id"] = coach.id
        
        return jsonify({"response": "valid coach",
                        "id": coach.id,
                        "fname" : coach.fname,
                        "lname" : coach.lname})
    
    if username_validation: 
        return jsonify({"response" : "invalid username", 
            "message" : "Username is taken. Please enter a different username."})
    
    if email_validation: 
        return jsonify({"response" : "invalid email", 
            "message" : "Email is taken. Please enter a different email."})

#***********************************************************************************   

#ATHLETE FEATURES

#Side nav JSON panel
@app.route("/athlete_info/json")
def identify_athlete_for_side_nav_bar(): 
    if session["id"]:
       athlete = athlete_crud.get_athlete_by_id(session["id"])
       return jsonify({"username" : athlete.username })

# Main Page
@app.route("/athlete/<int:id>/<fname><lname>")
def athlete(id, fname, lname):
    if session["id"]: 
        start_time_options =["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM"]
        coaches = coach_crud.all_coaches()
        athlete = athlete_crud.get_athlete_by_id(id)

        past_events = athlete_crud.athlete_past_present_future_events(id)[0]
        current_events = athlete_crud.athlete_past_present_future_events(id)[1]
        future_events = athlete_crud.athlete_past_present_future_events(id)[2]
        
        return render_template("athlete.html", 
                        athlete = athlete,
                        coaches = coaches,
                        past_events = past_events,
                        current_events = current_events,
                        future_events = future_events, 
                        start_time_options = start_time_options,)
    else: 
        return redirect("/")
    
#Route for athlete session selection form submission
@app.route("/session_options/json", methods = ["POST"])
def athlete_session_choices():
    front_end_events = []
    date_selection = request.form.get("selected-date")
    start_time = request.form.get("selected-start-time")
    coach_fname = request.form.get("selected-coach")

    # Parse selected date
    year_month_day = date_selection.split("-")
    month = year_month_day[1]
    date = year_month_day[2]
    year = year_month_day[0]
    #Get all the events on the calendar for that day
    events_on_schedule = eventschedule_crud.events_by_month_date_year_start_time(month, date, year, start_time)

    #Parse coach name to get the events that this 
    #coach has already been selected for
    coach_object = coach_crud.get_coach_by_fname(coach_fname)
    coach_id = coach_object.id
    coach_events = coach_object.events

    for coach_event in coach_events: 
        schedule_id = coach_event.event_schedule_id
        event_selected_with_coach = eventschedule_crud.get_scheduled_event_by_id(schedule_id)
        coach_month = event_selected_with_coach.month
        coach_date = event_selected_with_coach.date
        coach_year  = event_selected_with_coach.year
        coach_start_time = event_selected_with_coach.start_time
        print(coach_month, coach_date, coach_year, type(coach_start_time))
        # Condition for if the minth, date, year, and start time the coach is
        # chosen for is already taken
        #Values from client must be converted to int
        if coach_month == int(month) and coach_date == int(date) and coach_year == int(year) and coach_start_time == start_time:
            return f"Coach {coach_fname} is unavailable on {date_selection} at {start_time}"
        
    return"available"
            # return jsonify({"unavailable" : f"Coach {coach_fname} is unavailable on {date_selection} at {start_time}"})
        
        # else:   
        #     for scheduled_event in events_on_schedule:
        #         event_id = scheduled_event.event_id
        #         event_object = event_crud.get_event_by_id(event_id)
        #         front_end_events.append({"event_name" : event_object.name, 
        #                             "event_descritpion" : event_object.description, 
        #                             "event_duration" : f"{scheduled_event.start_time} - {scheduled_event.end_time}"})
        

        #         print("front_end_events:")
        #         print(front_end_events)
        #     return "Yes!"





    
#***********************************************************************************   

#COACH FEATURES
@app.route("/coach/<int:id>/<fname><lname>")
def coach(id, fname, lname): 
    return "gettin money too"


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
