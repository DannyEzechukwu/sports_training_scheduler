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

today = datetime.datetime.now().date()
parsed_date = datetime.datetime.strptime(str(today), "%Y-%m-%d")
formatted_date_string = parsed_date.strftime("%m/%d/%Y")

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
    return redirect("/")

# Main Athlete Page
@app.route("/athlete/<int:id>/<fname><lname>")
def athlete(id, fname, lname):
    if "id" in session:
    
        athlete = athlete_crud.get_athlete_by_id(id)

        past_events = sorted(athlete_crud.athlete_past_present_future_events_by_id(id)[0], key = lambda k: (k["date"], k["start_time_object"]))
        current_events = sorted(athlete_crud.athlete_past_present_future_events_by_id(id)[1], key = lambda k: (k["date"], k["start_time_object"]))
        future_events = sorted(athlete_crud.athlete_past_present_future_events_by_id(id)[2], key = lambda k: (k["date"], k["start_time_object"]))
        
        return render_template("athlete.html", 
                        athlete_fname = athlete.fname,
                        athlete_lname = athlete.lname,
                        past_events = past_events,
                        current_events = current_events,
                        future_events = future_events, )
     
    return redirect("/")
    
# JSON Endpoint to provide options to athletes to make event selections
# and coach to work with 
@app.route("/training_session_options/json")
def options_for_selected_date():
    if "id" in session:

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

        #Repeat same process above for end date
        end_date_selection = request.args.get("selected-end-date")

        end_month_date_year = end_date_selection.split("-")

        end_month = int(end_month_date_year[1])
        end_date = int(end_month_date_year[2])
        end_year = int(end_month_date_year[0])

        # # Condition for if start date is before today
        # if (datetime.datetime(start_year, start_month, start_date).date() < 
        #     datetime.datetime.now().date()): 
        #     return jsonify({"response" : "event in the past", 
        #                 "output" : f"Start date must be after {formatted_date_string}."})
        
        #Condition for if end date is before start date
        if (datetime.datetime(start_year, start_month, start_date).date() > 
            datetime.datetime(end_year, end_month, end_date).date()): 
            return jsonify({
                "response" : "start date not after end date", 
                "output" : f"End date must be after start date"})  

        # Filter for all the ebvents in the given time frame 
        # entered by the athlete
        events_filtered_by_date = eventschedule_crud.filter_events(start_month, start_date, start_year, end_month, end_date, end_year)
        
        # List comprehensions to get the available events for the date range entered
        # An avalable event is an event that appears in the EventSchedule class
        # but does not appear in the SelectedEvent class
        # and does not conflict with an existing event that the ethlete in th sesession 
        # has already selected
        available_events_first_pass = [
            event for event in events_filtered_by_date 
            if not selectedevent_crud.get_selectedevent_by_event_schedule_id(event.id)
        ]
        
        available_events = [
            event for event in available_events_first_pass
            if not
            athlete_crud.athlete_rejected_events(session["id"], event.month, event.date, event.year, event.start_time)
        ]

        final_available_events = sorted(available_events, key = lambda k: (datetime.datetime(k.year, k.month, k.date).date(), 
                                                    datetime.datetime.strptime(k.start_time, '%I:%M %p').time()))
    
        # Condition for if there are no events available for that day
        # due to them all being selected by other athletes 
        if final_available_events == []:
            return jsonify({
                "response" : "no events available", 
                "output" : f"No available events between {start_month}/{start_date}/{start_year} and {end_month}/{end_date}/{end_year}  "})
        
        # Loop through the EventSchedule objects in all available events
        # scheduled for the interval selected by athlete
        for available_event in final_available_events:
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

                    if coach: 
                        available_coaches.add(coach.fname)
                    
                    # Condition for if coach is unavailable for this specific event
                    if (
                        event_on_coach_schedule.month == available_event.month
                        and event_on_coach_schedule.date == available_event.date
                        and event_on_coach_schedule.year == available_event.year
                        and event_on_coach_schedule.start_time == available_event.start_time
                    ):
                        available_coaches.discard(coach.fname)
                    

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
    
    return redirect("/")

# JSON Endpoint to handle events selected by by athlete
@app.route("/training_session_selections/json", methods = ["POST"])
def sessions_for_selected_date():
    if "id" in session:
        # Get athlete in session
        athlete_object = athlete_crud.get_athlete_by_id(session["id"])

        # Get all elements from form sent back to the server
        selected_session_form_data = request.form

        # Container for event_schedule ids selected by athlete
        event_schedule_ids_from_athlete = []

        # Container for coaches to hold events selected
        coach_id_selected_by_athlete = []

        # Container to hold selected event objects
        selected_event_objects = []

        # Loop through each key where data is present
        # Max keys will be 6 (3 schedule ids, 3 coach names)
        for key in selected_session_form_data:
            # If the key is for an event_schedule ID 
            if "event-schedule-" in key:
                # Get the value and append it to correct list
                value = selected_session_form_data[key]
                event_schedule_ids_from_athlete.append(value)
            # If the key is for a coach name
            if "event-coach-" in key:
                # Get the value, get the object from the Coach class, 
                # append it to correct list
                value = selected_session_form_data[key]
                coach_object = coach_crud.get_coach_by_fname(value)
                coach_id_selected_by_athlete.append(coach_object.id)
        
        # Loop through the selected events from the schedule
        # Add the selectons to the database
        for i in range(len(event_schedule_ids_from_athlete)):
            coach_id = coach_id_selected_by_athlete[i]
            event_schedule_id = event_schedule_ids_from_athlete[i]
            selected_event = selectedevent_crud.select_event(athlete_object.id, 
                                coach_id,
                                event_schedule_id)
            
            db.session.add(selected_event)
            db.session.commit()

            selected_event_objects.append(selected_event)
            
            # Default feed back message for all sessions once they are added to the database
            default_feedback = feedback_crud.create_feedback_message(selected_event.id, coach_id)
            db.session.add(default_feedback)
            db.session.commit()
        
        if len(selected_event_objects) == 1:
            return jsonify({"response" : "Session added!"})
        return jsonify({"response" : "Sessions added!"})
    
    return redirect("/")
#***********************************************************************************   

#COACH FEATURES
#Side nav JSON panel
@app.route("/coach_info/json")
def identify_coach_for_side_nav_bar(): 
    if session["id"]:
       coach = coach_crud.get_coach_by_id(session["id"])
       return jsonify({"username" : coach.username })
    return redirect("/")


# Main Coach Page
@app.route("/coach/<int:id>/<fname><lname>")
def coach(id, fname, lname):
    if "id" in session:

        times = ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM"]

        # Get the coach in the session
        coach = coach_crud.get_coach_by_id(session["id"])
        # Get the events this coach has created using the created_events
        # relatiosnhip variable in the Coach class
        coach_created_events = coach.created_events
        

        # Container to hold the events the coach has created in the frontend
        coach_created_events_frontend = []

        # Create a count varible to compare selected vs scheduled events
        count = 0

        # Loop through the events created by this coach
        for event in coach_created_events:
            # Get the EventSchedule id of the event created by the coach 
            event_on_schedule = eventschedule_crud.get_scheduled_event_by_event_id(event.id)

            if event_on_schedule.specific_event_selected:
                count += 1

            available_sessions_remaining = len(event.schedule_appearances) - count 

            coach_created_events_frontend.append({"location" : event.location,
                                                  "event" : event.name,
                                                  "description" : event.description,
                                                  "available" : available_sessions_remaining 
                                                })


        past_events = sorted(coach_crud.coach_past_present_future_events_by_id(id)[0], key = lambda k: (k["date"], k["start_time_object"]))
        current_events = sorted(coach_crud.coach_past_present_future_events_by_id(id)[1], key = lambda k: (k["date"], k["start_time_object"]))
        future_events = sorted(coach_crud.coach_past_present_future_events_by_id(id)[2], key = lambda k: (k["date"], k["start_time_object"]))
        
        return render_template("coach.html",
                        coach_fname = coach.fname,
                        coach_lname = coach.lname, 
                        times = times,
                        past_events = past_events,
                        current_events = current_events,
                        future_events = future_events,
                        coach_created_events_frontend = coach_created_events_frontend)
    
    return redirect("/")
    
# JSON Endpoint to handle events added by coaches
@app.route("/add_event/json", methods = ["POST"])
def new_coach_event(): 
    if "id" in session:
        new_event = request.form.get("event-name").strip()
        new_event_location = request.form.get("event-location").strip()
        new_event_description = request.form.get("event-description").strip()
        new_event_start_time = request.form.get("event-start-time").strip()
        new_event_end_time = request.form.get("event-end-time").strip()
        
        # New event start date datetime object
        new_event_start_date = request.form.get("event-start-date").strip()
        new_event_start_month_date_year = new_event_start_date.split("-")
        new_event_start_month = int(new_event_start_month_date_year[1])
        new_event_start_date = int(new_event_start_month_date_year[2])
        new_event_start_year = int(new_event_start_month_date_year[0])
        new_event_start_date_object = datetime.datetime(new_event_start_year,
                                                new_event_start_month,
                                                new_event_start_date)
        
        # New event end date datetime object
        new_event_end_date  = request.form.get("event-end-date").strip()
        new_event_end_month_date_year = new_event_end_date.split("-")
        new_event_end_month = int(new_event_end_month_date_year[1])
        new_event_end_date = int(new_event_end_month_date_year[2])
        new_event_end_year = int(new_event_end_month_date_year[0])
        new_event_end_date_object = datetime.datetime(new_event_end_year,
                                                new_event_end_month,
                                                new_event_end_date)
        
        # Condition if start date is before today
        if new_event_start_date_object.date() < datetime.datetime.now().date(): 
            return jsonify({"response" : "event in the past", 
                        "output" : f"Start date must no earlier than {formatted_date_string}."})
        
        # Condition if start date is after end date
        if new_event_start_date_object.date() > new_event_end_date_object.date(): 
            return jsonify({"response" : "start date not after end date", 
                        "output" : "End date must be after start date."})
    
        # Create event object 
        event_object = event_crud.create_event(new_event,
                                            new_event_location, 
                                            new_event_description, 
                                            coach_id = session["id"])
        
        db.session.add(event_object)
        db.session.commit()

        # Function to create a list of dates from
        # dates entered by coach
        # Will loop through the list to create objects of 
        # the EventSchedule class
        def generate_date_list(start_date, 
                            end_date,
                            separator = "/"):
            
            delta = datetime.timedelta(days = 1)
            
            date_container = []

            current_date = start_date
            while current_date <= end_date:
                formatted_date = current_date.strftime(f'%m{separator}%d{separator}%Y')
                date_container.append(formatted_date)
                current_date += delta
    
            return date_container

        # Create date list with the function defined above
        date_list = generate_date_list(new_event_start_date_object,
                                new_event_end_date_object)
        
        event_schedule_objects = [] 
        
        for date in date_list:

            # Gather date info for each date
            individual_date_list = date.split("/")
            month = int(individual_date_list[0])
            date = int(individual_date_list[1])
            year = int(individual_date_list[2])

            # Create EventSchedule object, append it to list,
            #  add it to database
            event_schedule_object = eventschedule_crud.schedule_event(event_object.id,
                                                            month, 
                                                            date, 
                                                            year,
                                                            new_event_start_time, 
                                                            new_event_end_time)
            
            db.session.add(event_schedule_object)
            db.session.commit()

            event_schedule_objects.append(event_schedule_object)

        
        front_end_event_data = {"location" : event_object.location,
                                            "event" : event_object.name,
                                            "description" : event_object.description,
                                            "available" : len(event_object.schedule_appearances)}
        

        return jsonify({"response" : "successful",
                        "output" : front_end_event_data})
    
    return redirect("/")

# JSON Endpoint to handle feedback added by coaches
@app.route("/add_feedback/json", methods = ["POST"])
def add_feedback():
    # Get feedback message and id from the frontend
    feed_back_id = int(request.form.get("feedback-id"))
    feed_back_text = request.form.get("feedback-text")
    
    # Get the feedback_object corresponding to the feed_back_id
    feedback_object = feedback_crud.feedback_by_id(feed_back_id)

    # Update the feedback attribute in tfor the feedback_object
    # commit change to data base
    feedback_object.feedback = feed_back_text
    db.session.commit()
    

    return jsonify({"response" : "Feedback added!",
                    "output" : feedback_object.feedback})

    
    



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
