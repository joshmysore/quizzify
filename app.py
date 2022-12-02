import os
from xml.etree.ElementTree import tostring
# comment


from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///quizzify.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# THIS IS WHERE EVERYTHING NEW BEGINS AND I DID NOT ALTER ANYTHING ABOVE FROM FINANCE

# This registers a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    print("TEST")

    if request.method == "POST":
        username = request.form.get("username")
        print(username)
        password = request.form.get("password")
        print(password)
        confirmation = request.form.get("confirmation")
        print(confirmation)
        print("POST")
        # checks of submitted username
        # could I combine these three for design?
        if not username:
            return apology("must provide username")

        # checks of submitted password
        elif not password:
            return apology("must provide password")

        # checks of submitted confirmation of password
        elif not confirmation:
            return apology("must confirm password")

        # checks if password and confirmation match
        if password != confirmation:
            return apology("Your password does not match the confirmation of your password")

        print("confirmation")

        # checks if username already exists
        if len(db.execute("SELECT username FROM users WHERE username = ?", username)) > 0:
            return apology("This username already exists. Please enter a unique username.")

        # adding new user to the database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        # log user in (getting this from the login route)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        session["user_id"] = rows[0]["user_id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


# Logs User In
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
        print("test")

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# Logs User Out
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# This takes the user to the homepage where they see their recommended list of songs
@app.route("/")
@login_required
def index():
    """Show show the list of recommended songs to the user"""
    # get the current user_id from the session
    user_id = session["user_id"]

    # this executes some type of SQL query where it gets the names and song analytics of the new table we create
    # list = db.execute("SELECT all the variables FROM newTable WHERE user_id = ? ORDER BY timestamp DESC LIMIT BY 1"  , user_id)

    return render_template("user.html", username=session["username"])

    # Step 3: print out the list somehow (refer to finance index)


# This takes the user to the homepage where they see their recommended list of songs
@app.route("/form")
@login_required
def form_fillout():
    """Takes the user to the form in order to fill out and then uses that data to figure out the precise number for the 5 variables and insert into the SQL database"""

    # Step 1: Look up data from the form and conduct average calculations
    dance = 0
    energy = 0
    live = 0
    year = 0
    bpm = 0

    values = [dance, energy, live, year, bpm]

    #2d array
    # row1 -> ["numbers1", 40 , 50, 65, 80, 90] -> dance
    # row2 -> ["numbers2", 40 , 50, 65, 80, 90] -> dance
    # row3 -> ["numbers3", 40 , 50, 65, 80, 90] -> energy
    # row4 -> ["numbers4", 40 , 50, 65, 80, 90] -> energy
    # ... 
    arr = [["numbers1", 40, 50, 65, 80, 90], ["numbers2", 40, 50, 65, 80, 90], ["numbers3", 50, 60, 75, 85, 90], ["numbers4", 50, 60, 75, 85, 90], ["numbers5", 6, 13, 20, 28, 38], ["numbers6", 6, 13, 20, 28, 38],  ["numbers7", 2011, 2013, 2015, 2017, 2019], ["numbers8", 2011, 2013, 2015, 2017, 2019], ["numbers9", 70, 100, 125, 155, 185], ["numbers10", 70, 100, 125, 155, 185]]
    sum = 0


    for i in range(1, 11):
        string = "numbers" ^ tostring(i)
        for j in range (1, 6):
            if request.form.get(string) == arr[string][j]:
                chosen_value = values[j]
        sum += chosen_value

        # if we are at the end of another set of 2 questions
        if i % 2 == 0:
            values[i] = round(sum / 2)
            sum = 0

    # makes bounds in order to get range estimates 
    boundDanceUpper = values[0] + 2
    boundDanceLower = values[0] - 2

    boundEnergyUpper = values[1] + 2
    boundEnergyLower = values[1] - 2

    boundLiveUpper = values[2] + 2
    boundLiveLower = values[2] - 2

    boundYearUpper = values[3] + .5
    boundYearLower = values[3] - .5

    boundBpmUpper = values[4] + 2
    boundBpmLower = values[4] - 2

    # Step 2: Go though the SQL database to see which songs fit into the range from the 5 variables

    result = db.execute("SELECT title FROM songs WHERE dance > ? AND dance < ? AND energy > ? AND energy < ? AND live > ? AND live < ? AND year > ? AND year < ? AND bpm > ? AND bpm < ?", boundDanceUpper, boundDanceLower, boundEnergyUpper, boundEnergyLower, boundLiveUpper, boundLiveLower, boundYearUpper, boundYearLower, boundBpmUpper, boundBpmLower)
    db.execute("INSERT INTO (title, ) WHERE user_id = x ")

    

    # Step 3: Insert the songs into a table corresponding to the user_id
    return redirect("/")