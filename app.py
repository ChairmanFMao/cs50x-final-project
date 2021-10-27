import sqlite3
import os
import requests

from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, session, redirect, flash
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import abort, default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response
 
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    # I had this as decorated() for about an hour and spent an hour debugging it ;-;
    return decorated

def createConnection():
    return sqlite3.connect("atlas.db")

@app.route("/")
def index():
    if "user_id" not in session:
        session["user_id"] = None
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    return render_template("post.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.errorhandler(404)
def page_not_found():
    return render_template("404.html"), 404