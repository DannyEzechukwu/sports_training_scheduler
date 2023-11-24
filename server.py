from flask import Flask, render_template, request, flash, session, redirect, jsonify

from model import connect_to_db, db

import os

import random

from jinja2 import StrictUndefined

app = Flask(__name__)

#Secret Key to enable session
app.secret_key = os.environ["APP_KEY"]
app.jinja_env.undefined = StrictUndefined