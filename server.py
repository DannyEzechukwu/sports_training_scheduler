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
        athlete = athlete_crud.get_athlete_id(session["id"])
        return jsonify({"response": "valid athlete",
                        "id": athlete.id,
                        "fname" : athlete.fname,
                        "lname" : athlete.lname})
    else:
        return jsonify({"response" : "invalid"})

#New Athlete Account
@app.route("/new_athlete_account", methods = ["POST"])
def new_athlete(): 
    fname = request.form.get("new-athlete-fname").strip()
    lname = request.form.get("new-athlete-lname").strip()
    username = request.form.get("new-athlete-username").strip()
    email = request.form.get("new-athlete-email").strip()
    password = request.form.get("new-athlete-password").strip()

    inputs = [fname, lname, username, email, password]

    if inputs[0] == "":
        print("First name not included. Please try again.")
        return redirect("/")
    elif inputs[1] == "": 
        print("Last name not included. Please try again.")
        return redirect("/")
    elif inputs[2] == "":
        print("Username not included. Please try again.")
        return redirect("/")
    elif athlete_crud.get_athlete_by_username(inputs[2]): 
        print("Username already exists. Please try again.")
        return redirect("/")
    elif inputs[3] == "": 
        print("Email not included. Please try again.")
        return redirect("/")
    elif athlete_crud.get_athlete_by_email(email): 
        flash("Email already exists. Please try again.")
        return redirect("/")
    else: 
        new_athlete = athlete_crud.create_athlete(fname, lname, username, email, password)
        db.session.add(new_athlete)
        db.session.commit()
        session['id'] = new_athlete.id
        return redirect('/')
    
#New Coach Account
@app.route("/new_coach_account", methods = ["POST"])
def new_coach(): 
    fname = request.form.get("new-coach-fname").strip()
    lname = request.form.get("new-coach-lname").strip()
    username = request.form.get("new-coach-username").strip()
    email = request.form.get("new-coach-email").strip()
    password = request.form.get("new-coach-password").strip()

    inputs = [fname, lname, username, email, password]

    if inputs[0] == "":
        print("First name not included. Please try again.")
        return redirect("/")
    elif inputs[1] == "": 
        print("Last name not included. Please try again.")
        return redirect("/")
    elif inputs[2] == "":
        print("Username not included. Please try again.")
        return redirect("/")
    elif athlete_crud.get_athlete_by_username(inputs[2]): 
        print("Username already exists. Please try again.")
        return redirect("/")
    elif inputs[3] == "": 
        print("Email not included. Please try again.")
        return redirect("/")
    elif athlete_crud.get_athlete_by_email(email): 
        flash("Email already exists. Please try again.")
        return redirect("/")
    else: 
        new_coach = coach_crud.create_coach(fname, lname, username, email, password)
        db.session.add(new_coach)
        db.session.commit()
        session['id'] = new_coach.id
        return redirect('/')

#***********************************************************************************   

#ATHLETE FEATURES
@app.route("/athlete/<int:id>/<fname><lname>")
def athlete(id, fname, lname): 
    return "money"

#***********************************************************************************   

#COACH EATURES
@app.route("/coach/<int:id>/<fname><lname>")
def coach(id, fname, lname): 
    return "gettin money too"


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
