import os
from xml.etree.ElementTree import tostring
# comment
import smtplib
from email.message import EmailMessage
import imghdr
import pdfkit 

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, apology2, login_required

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

# This registers a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        
        #gets the username, password, and confirmation from the form by requesting 
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # checks of submitted username
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
        session["user_id"] = rows[0]["user_id"]
        session["username"] = rows[0]["username"]

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
    return redirect("/register")


# This takes the user to the homepage where they see their recommended list of songs
@app.route("/")
@login_required
def index():
    """Show the list of recommended songs to the user"""

    # renders the user.html template as the homepage 
    return render_template("user.html", username=session["username"])


@app.route("/songs", methods=["GET"])
@login_required
def display():
    """Show everything to the user"""
    
    user_id = session["user_id"]
    
    # Gets the variables from the recommendation table where the user_id is that of the person who is logged in 
    list1 = db.execute("SELECT id, dance, energy, live, year, bpm FROM recs WHERE user_id = ? ORDER BY id DESC LIMIT 1", user_id)
    
    # check's if the user has yet to fill out a form
    if len(list1) == 0:
        return apology2("You must fill out the form first in order to see any results", 403)
    
    # gets the recommendation id specifically from the list1 query 
    recom_id = list1[0]["id"]   
    
    # select all of our variables from the songs table where the song id is in the song id from the tables_id table 
    # conducting a nested select here
    list2 = db.execute("SELECT title, artist, dance, energy, live, year, bpm FROM songs WHERE songid IN (SELECT songsid FROM tables_id WHERE user_id = ? AND recs_id = ? )", user_id, recom_id)

    # provides an initialized empty statement
    statement = "" 
    
    # changes statement to present songs depending on whether there are songs that matched the users preferences in the list2 query. 
    if list2:
        statement = "Here are your songs."
    else: 
        statement = "Sorry, none of the songs in the database match your quiz results. Retake for different results." 

    return render_template("songs.html", list1=list1, list2=list2, statement=statement)


# This takes the user to the homepage where they see their recommended list of songs
@app.route("/form", methods=["GET", "POST"])
@login_required
def form_fillout():
    """Takes the user to the form in order to fill out and then uses that data to figure out the precise number for the 5 variables and insert into the SQL database"""

    user_id = session["user_id"]
    
    if request.method == "POST":
        
        
        # Step 1: Look up data from the form and conduct average calculations
        # Initializes variables to 0 and creates a list with them  
        dance = 0
        energy = 0
        live = 0
        year = 0
        bpm = 0

        values = [dance, energy, live, year, bpm]

        # This creates a 2d array that is supposed to emulate a matrix and sets each row from the first column as the question number from the form 
        # The array sets the corresponding values we will assign from the user's answer being 1-5.  
        # row1 -> ["numbers1", 40 , 50, 65, 80, 90] -> dance
        # row2 -> ["numbers2", 40 , 50, 65, 80, 90] -> dance
        # row3 -> ["numbers3", 40 , 50, 65, 80, 90] -> energy
        # row4 -> ["numbers4", 40 , 50, 65, 80, 90] -> energy
         
        arr = [["numbers1", 40, 50, 65, 80, 90], ["numbers2", 40, 50, 65, 80, 90], ["numbers3", 50, 60, 75, 85, 90], ["numbers4", 50, 60, 75, 85, 90], ["numbers5", 6, 13, 20, 28, 38], ["numbers6", 6, 13, 20, 28, 38],  ["numbers7", 2011, 2013, 2015, 2017, 2019], ["numbers8", 2011, 2013, 2015, 2017, 2019], ["numbers9", 70, 100, 125, 155, 185], ["numbers10", 70, 100, 125, 155, 185]]
        sum = 0

        # iterates through each of the 10 questions
        for i in range(1,11):
            # create a string variable that appends “numbers” to whatever number question the loop is on.
            string = "numbers" + str(i)
            # CONDUCTS ERROR CHECKING FOR THE FORM 
            if not request.form.get(string):
                return apology2("must provide answers to all of the questions", 403)
            # set the assigned value within the array to the user’s chosen value from the question
            for j in range (1, 6): 
                if int(request.form.get(string)) == j:
                    chosen_value = arr[i - 1][j]
                    sum += chosen_value

            # if we are at the end of another set of 2 questions
            if i % 2 == 0:
                values[(i // 2) - 1] = round(sum / 2)
                sum = 0

        # makes bounds in order to get range estimates 
        boundDanceUpper = values[0] + 10
        boundDanceLower = values[0] - 10

        boundEnergyUpper = values[1] + 10
        boundEnergyLower = values[1] - 10

        boundLiveUpper = values[2] + 10
        boundLiveLower = values[2] - 10

        boundYearUpper = values[3] + 2
        boundYearLower = values[3] - 2

        boundBpmUpper = values[4] + 10
        boundBpmLower = values[4] - 10

        # Step 2: Go though the SQL database to see which songs fit into the range from the 5 variables

        # determine which songs fit into the range of all of the 5 variables obtained from the user’s quiz answer results
        result = db.execute("SELECT songid FROM songs WHERE dance < ? AND dance > ? AND energy < ? AND energy > ? AND live < ? AND live > ? AND year < ? AND year > ? AND bpm < ? AND bpm > ?", boundDanceUpper, boundDanceLower, boundEnergyUpper, boundEnergyLower, boundLiveUpper, boundLiveLower, boundYearUpper, boundYearLower, boundBpmUpper, boundBpmLower)
        
        # inserts the user’s preferred listening variables from the quiz into the recs table
        db.execute("INSERT INTO recs (user_id, dance, energy, live, year, bpm) VALUES (?, ?, ?, ?, ?, ?)", user_id, values[0], values[1], values[2], values[3], values[4])
        
        # get the specific recommendation id 
        rec_id = db.execute("SELECT id FROM recs WHERE user_id = ? ORDER BY id DESC LIMIT 1", user_id)[0]["id"]

        # insert the user, song, and recommendation ids into another table called tables_id. Stores all of the ids needed for each query in the songs route
        for song in result: 
            db.execute("INSERT INTO tables_id (user_id, songsid, recs_id) VALUES (?, ?, ?)", user_id, song["songid"], rec_id)
            
        # Step 3: Insert the songs into a table corresponding to the user_id
        return redirect("/songs")
    
    else:
        return render_template("form.html")


@app.route("/friends", methods=["GET", "POST"])
@login_required
def find_friends():
    """Send Email of User's results"""
    
    if request.method == "POST":
        
        # gets the username from the user's form input 
        username = request.form.get("username")

        # checks if the username is not the current user's username 
        if username == session["user_id"]:
            return apology2("Bro... This is you, not a friend.", 403)

        # checks if the user inputted a friend's username 
        if not username:
            return apology2("must provide username", 403)
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1:
            return apology2("The username you have inputed does not match with anyone who has registered for Quizzify", 403)
        
        # gets the specific user id that falls under the username 
        new_id = db.execute("SELECT user_id FROM users WHERE username = ?", username)[0]['user_id']

        # Gets the variables from the recommendation table where the user_id is that of the person who is logged in 
        list1 = db.execute("SELECT id, dance, energy, live, year, bpm FROM recs WHERE user_id = ? ORDER BY id DESC LIMIT 1", new_id)

        if len(list1) == 0:
            return apology2("Sorry, but it seems like your friend hasn't filled out a form yet. This means you can't see any results.", 403)
        
        recom_id = list1[0]["id"]   
        
        list2 = db.execute("SELECT title, artist, dance, energy, live, year, bpm FROM songs WHERE songid IN (SELECT songsid FROM tables_id WHERE user_id = ? AND recs_id = ? )", new_id, recom_id)

        statement = "" 
        if list2:
            statement = "Here are your friend's songs."
        else: 
            statement = "Sorry, none of the songs in the database matched your friend's most recent quiz results." 

        return render_template("songs2.html", list1=list1, list2=list2, statement=statement, username=username)
            
    else: 
        return render_template("friends.html")


# Email feature. Took 5 hours to implement, TF said the code was correct, only problem is the GMAIL API verification takes too long and is super strict. 
@app.route("/email")
@login_required
def send_email():
    """Send Email of User's results"""

    user_id = session["user_id"]

    pdfkit.from_url('http://127.0.0.1:5000/songs', 'results.pdf')

    # this gives the port needed for the gmail -- this is from the python article
    port = 465
    # this is from the video ???
    port = 587 

    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    # Get email from SQL query 
    user_email = db.execute("SELECT email FROM users WHERE user_id = ?", user_id)

    # Get msg 
    msg = EmailMessage()
    msg['Subject'] = 'Check out your results!'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = user_email
    msg.set_content('Thank you for checking out Quizzify! Attatched below are a couple of pictures we wanted to include for you as well as a PDF of your results')

    # lists for JPGs and PDFs
    files = ['creators.jpg', 'city.jpg']
    pdffiles = ['results.pdf']

    # for loop for JPGs
    for file in files:
        # adds an attachment of an image to the email
        with open(file, 'rb') as f: 
            file_data = f.read()
            file_type = imghdr.what(f.name)
            filename = f.name

    # for loop for PDF 
    for pdffile in pdffiles:
        # adds an attachment of an image to the email
        with open(pdffile, 'rb') as x: 
            pdffile_data = x.read()
            pdffilename = x.name

    #adds attatchments to the email 
    msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=filename)
    msg.add_attachment(pdffile_data, maintype='application', subtype="octet-stream", filename=pdffilename)

    msg.add_alternative("""\ 
    <! DOCTYPE html>
    <html>
        <body>
            <h1 style="color: SlateGray;">This is an HTML Email!</h1>
        </body>
    </html>
    """, subtype='html')

    with smtplib.SMTP('smtp.gmail.com', port) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()

            # send the email and the message
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

    return redirect("/")
