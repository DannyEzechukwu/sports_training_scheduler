from flask import Flask, render_template, request, flash, session, redirect, jsonify

from model import connect_to_db, db

import user_crud
import coach_crud
import event_crud
import selectedevent_crud
import eventschedule_crud

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

@app.route("/coach_login", methods = ["POST"])
def coach_login(): 
    username = request.form.get("coach_username")
    password = request.form.get("coach_password")

    if coach_crud.get_coach_by_username_and_password(username, password):
        print(True)
        flash("Hooray")
        return redirect('/')
    else:
        flash("Try again")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
