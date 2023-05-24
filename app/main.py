from flask import render_template, redirect, url_for, Blueprint, request, session, flash
from .models import Users
from . import db
from datetime import datetime

signin_blueprint = Blueprint("signin", __name__)
login_blueprint = Blueprint("login", __name__)
dashboard_blueprint = Blueprint("dashboard", __name__)
logout_blueprint = Blueprint("logout", __name__)

@signin_blueprint.route('/', methods=["POST", "GET"])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = Users.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists.", "error")
        else:
            new_user = Users(username=username, password=password, email=None)
            db.session.add(new_user)
            db.session.commit()

            session['username'] = username
            # session['email'] = None #
            # session.update({"username": username})
            return redirect(url_for("dashboard.dashboard"))

    return render_template('signin.html')

@login_blueprint.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        found_user = Users.query.filter_by(username=username).first()

        if found_user:
            if found_user.password == password:
                session['username'] = username
                user_duration = datetime.now() - found_user.sign_in_date
                flash("You have been successfully logged in.", "success")
                flash(f"{found_user.username}, you are with us for {user_duration}")
            else:
                flash("Invalid username or password.", "error")
        else:
            flash("Invalid username or password.", "error")

    elif request.method == "GET" and "username" not in session:
        return render_template("login.html")
    elif request.method == "GET" and "username" in session:
        flash("Already logged in!", "warning")

    return redirect(url_for("dashboard.dashboard"))


@logout_blueprint.route('/logout')
def logout():
    if "username" in session:
        session.pop("username", None)
        session.pop("email", None)
        flash("You have been logged out!", "success")
    else:
        flash("You are not logged in!", "warning")

    return redirect(url_for("login.login"))


@dashboard_blueprint.route('/dashboard', methods=["POST", "GET"])
def dashboard():
    if "username" in session:
        username = session["username"]

        if request.method == "POST":
            found_user = Users.query.filter_by(username=username).first()
            email = request.form["email"]
            found_user.email = email
            db.session.commit()
            session.update({"email": email})

        return render_template("dashboard.html", username=username)
    else:
        flash("You are not logged in!", "warning")

    return redirect(url_for("login.login"))
