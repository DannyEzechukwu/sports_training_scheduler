from flask import Flask, render_template, request, flash, session, redirect, jsonify

from model import connect_to_db, db

import os

import random

from jinja2 import StrictUndefined

app = Flask(__name__)

#Secret Key to enable session
app.secret_key = os.environ["APP_KEY"]
app.jinja_env.undefined = StrictUndefined

@app.route("/calendar")
def show_cal(): 
    return render_template("calendar.html")

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
