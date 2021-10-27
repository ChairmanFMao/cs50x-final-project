import sqlite3
from datetime import datetime
from flask import Flask, render_template, request
from flask_session import Session
from werkzeug.exceptions import abort, default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

def createConnection():
    return sqlite3.connect("atlas.db") 

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post", methods=["GET", "POST"])
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