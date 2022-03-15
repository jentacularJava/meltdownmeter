import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
#app.jinja_env.filters["usd"] = usd

# TODO: Figure out how to create custom filter for date time format on index, entries, and account pages.

# from https://jinja.palletsprojects.com/en/3.0.x/api/
def datetime_format(value, format="%H:%M %d-%m-%y"):
    return value.strftime(format)
app.jinja_env.filters["datetime_format"] = datetime_format

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///meltdown.db")

# Configure to use the postgresql db
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://")
db = SQL(uri)

# Make sure API key is set
# if not os.environ.get("API_KEY"):
#    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show entries added and give option to add entry from this page"""
    entries = db.execute("""
        SELECT *
        FROM entries
        WHERE user_id = ?""", session["user_id"])

    username = db.execute("""
        SELECT username
        FROM users
        WHERE id = ?""", session["user_id"])[0]["username"]

    return render_template("index.html", entries=entries, username=username)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Buy shares of stock"""
    if request.method == "POST":
        # Validate that required fields are completed
        if not request.form.get("datetime"):
            return apology("Missing Date and Time", 400)
        elif not request.form.get("during"):
            return apology("Please complete the Child's Behaviour field", 400)
        else:
            insert_inputs_into_db = db.execute("""
                INSERT INTO entries (datetime, before, during, response, resolved, user_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """, request.form.get("datetime"), request.form.get("before"), request.form.get("during"), request.form.get("response"), request.form.get("resolved"), session["user_id"])
            # row = db.execute("SELECT * FROM entries WHERE user_id = ?",transaction_id)
            flash("Entry added!")
            return redirect("/")

    return render_template("add.html")


@app.route("/entries")
@login_required
def entries():
    # Show entries added and give option to add entry from this page
    entries = db.execute("""
        SELECT *
        FROM entries
        WHERE user_id = ?""", session["user_id"])
    username = db.execute("""
        SELECT username
        FROM users
        WHERE id = ?""", session["user_id"])[0]["username"]

    return render_template("entries.html", entries=entries, username=username)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/about", methods=["GET", "POST"])
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (i.e., submitted form)
    if request.method == "POST":
        # User did not enter name or password or confirmation
        if not request.form.get("username"):
            return apology("Please provide username", 400)

        elif not request.form.get("password"):
            return apology("Please provide password", 400)

        elif not request.form.get("confirmation"):
            return apology("Please confirm password", 400)

        else:
            # Query database for username
            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

            # Ensure username exists and password is correct
            if len(rows) > 0:
                return apology("Username taken", 400)

            elif request.form.get("password") != request.form.get("confirmation"):
                return apology("Passwords must match", 400)

            else:
                rows = db.execute("""
                    INSERT INTO users (username, hash)
                    VALUES (?, ?)""", request.form.get("username"), generate_password_hash(request.form.get("password")))
                # Query database to use for session id
                rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

                # Remember which user has logged in
                session["user_id"] = rows[0]["id"]

                # Redirect user to home page
                flash('Registered!')
                return redirect("/")

    # User reached route via GET
    else:
        return render_template("register.html")

@app.route("/account", methods=["GET"])
@login_required
def account():
    users = db.execute("""
        SELECT *
        FROM users
        WHERE id = ?""", session["user_id"])
    username = users[0]["username"]
    return render_template("account.html", username=username, users=users)


@app.route("/changepw", methods=["POST"])
@login_required
def changepw():
    if request.method == "POST":
        if not request.form.get("currentpw"):
                return apology("Please enter current password", 400)
        # Query database for current hash
        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        hash = rows[0]["hash"]
        if not check_password_hash(hash, request.form.get("currentpw")):
            return apology("Current password incorrect", 400)
        elif not request.form.get("confirmation"):
            return apology("Please confirm password", 400)
        elif request.form.get("newpw") != request.form.get("confirmation"):
                return apology("New passwords must match", 400)
        else:
            # Update password in users table
            rows = db.execute("""
                UPDATE users
                SET hash = ?
                WHERE id = ?
                """, generate_password_hash(request.form.get("newpw")), session["user_id"])
            flash('Password changed!')
            return redirect("/account")
    return redirect("/account")
