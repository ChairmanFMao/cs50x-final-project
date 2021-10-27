import sqlite3
import os
import requests
import re

from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, session, redirect, flash, jsonify
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
    if request.method == "POST":
        con = createConnection()
        cur = con.cursor()
        usernameMatches = cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),)).fetchall()
        con.commit()
        con.close()
        if not check_password_hash(usernameMatches[0][2], request.form.get("password")):
            return render_template("login.html", invalidPassword=True)
        session["user_id"] = usernameMatches[0]["id"]
        return redirect("/")
    return render_template("login.html", invalidPassword=False)

@app.route("/validateUsername")
def validateUsername():
    con = createConnection()
    cur = con.cursor()
    usernameMatches = cur.execute("SELECT * FROM users WHERE username = ?", (request.args.get("q"),)).fetchall()
    con.commit()
    con.close()
    return jsonify(usernameMatches)

@app.route("/validatePassword")
def validatePassword():
    password = request.args.get("p")
    return jsonify({
        "letter" : len(re.findall("[a-zA-z]", password)) >= 1,
        "number" : len(re.findall("[0-9]", password)) >= 1,
        "length" : len(password) >= 5,
        "match" : password == request.args.get("rp")
    })

@app.errorhandler(404)
def page_not_found():
    return render_template("404.html"), 404