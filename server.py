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

import datetime

from jinja2 import StrictUndefined

app = Flask(__name__)

app.static_folder = 'static'

#Secret Key to enable session
app.secret_key = os.environ["APP_KEY"]
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    if "id" in session:
        session.pop("id")
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
    if "id" in session: 

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
    
# JSON Endpoint to provide options to athletes to make event selections
# and coach to work with 
@app.route("/training_session_options/json")
def options_for_selected_date():

    #Empty list that will hold available events and coaches to
    # send to front end
    front_end_events_and_coaches = []

    #Start date selected from Add sessions view
    start_date_selection = request.args.get("selected-start-date")

    # Parse selected start date into month, date, year
    # Make them integers for valid database comparisons
    start_month_date_year = start_date_selection.split("-")
    start_month = int(start_month_date_year[1])
    start_date = int(start_month_date_year[2])
    start_year = int(start_month_date_year[0])

    # Get all events scheduled for the start date selected by athlete
    all_events_for_start_date = eventschedule_crud.events_by_month_date_year(start_month, start_date, start_year)
    # Put events gathered from the date selected in order by start time
    # %I: Hour (12-hour clock, zero-padded)
    # %M: Minute (zero-padded)
    # %p: AM or PM.
    all_events_for_start_date_ordered_by_start_time = sorted(all_events_for_start_date, key = lambda x: datetime.datetime.strptime(x.start_time, "%I:%M %p"))

    #Repeat same process above for end date
    end_date_selection = request.args.get("selected-end-date")

    end_month_date_year = end_date_selection.split("-")

    end_month = int(end_month_date_year[1])
    end_date = int(end_month_date_year[2])
    end_year = int(end_month_date_year[0])

    all_events_for_end_date = eventschedule_crud.events_by_month_date_year(end_month, end_date, end_year)

    all_events_for_end_date_ordered_by_start_time = sorted(all_events_for_end_date, key = lambda x: datetime.datetime.strptime(x.start_time, "%I:%M %p"))
    
    # Getting indexes for first event from the start date selected
    # and the last event from the end date selected
    # Generating list of events between those indexes
    first_event_index = eventschedule_crud.all_scheduled_events().index(all_events_for_start_date_ordered_by_start_time[0])
    final_event_index = eventschedule_crud.all_scheduled_events().index(all_events_for_end_date_ordered_by_start_time[-1])
    events = eventschedule_crud.all_scheduled_events()[first_event_index : final_event_index + 1]
    
    # List comprehension to get the available events for the date
    # An avalable event is an event that appears in the Event Schedule class
    # but does not appear in the SelectedEvent class
    available_events = [event for event in events if not selectedevent_crud.get_selectedevent_by_event_schedule_id(event.id)]

    #Condition for if end date is before start date
    if (datetime.datetime(start_year, start_month, start_date) >= 
        datetime.datetime(end_year, end_month, end_date)): 
        return jsonify({
            "response" : "start date not after end date", 
            "output" : f"End date must be after start date"})
    
    # Condition for if there are no events available for that day
    # due to them all being selected by other athletes 
    if available_events == []:
        return jsonify({
            "response" : "no events available", 
            "output" : f"No available events between {start_month}/{start_date}/{start_year} and {end_month}/{end_date}/{end_year}  "})
    
    # Loop through the EventSchedule objects in all available events
    # scheduled for the day selected by athlete
    for available_event in available_events:
        available_coaches = set()

        # Get the object from the Event class for each event
        # that is available using the event_id attribute
        # Define the attributes in understandable variables
        event_object = event_crud.get_event_by_id(available_event.event_id)
        event_name = event_object.name
        event_location = event_object.location
        event_description = event_object.description
        
        # Loop through each coach in the database
        for coach in coach_crud.all_coaches():

            # Loop through each event the coach has been selected for
            for coach_event in coach.events:
                # Get the object from the EventSchedule class for each event the coach
                # has been selected for using the event_schedule_id attribute
                event_on_coach_schedule = eventschedule_crud.get_scheduled_event_by_id(coach_event.event_schedule_id)

                # Condition for if coach is unavailable for this specific event
                if (
                    event_on_coach_schedule.month == available_event.month
                    and event_on_coach_schedule.date == available_event.date
                    and event_on_coach_schedule.year == available_event.year
                    and event_on_coach_schedule.start_time == available_event.start_time
                ):
                    break
                else:
                    available_coaches.add(coach.fname)

        front_end_events_and_coaches.append(
            {
                "id": available_event.id,
                "month": available_event.month,
                "date": available_event.date,
                "year": available_event.year,
                "duration": f"{available_event.start_time} - {available_event.end_time}",
                "event_name": event_name,
                "location": event_location,
                "description": event_description,
                "available_coaches": list(available_coaches),
            })
                
    return jsonify({
                "response" : "successful",
                "output": front_end_events_and_coaches})
    


# JSON Endpoint to handle events selected by by athlete
@app.route("/training_session_selections/json", methods = ["POST"])
def sessions_for_selected_date():
    
    # Get all elements from form sent back to the server
    selected_session_form_data = request.form

    

    # Loop through each key where data is present
    for key in selected_session_form_data: 
        if "event-schedule-" in key: 
            print(key)

    return jsonify({"response" : "mid"})


#***********************************************************************************   

#COACH FEATURES
@app.route("/coach/<int:id>/<fname><lname>")
def coach(id, fname, lname): 
    return "gettin money too"


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
