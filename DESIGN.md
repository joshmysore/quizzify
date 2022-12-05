# Design.md


# Frontend 

To explain the frontend, let’s go through the .css files first:

Login-style.css: This file is the main stylesheet for our website. The other .css files, in general, adopt variations of this parent file. First, we import a custom url and set the body font equal to Rubik, a nice sans serif font. Then, we set up a custom navbar, rather than using bootstrap, so that the top left corner would be an overlay on the website, and could be changed to different implementations depending on the actual page. We set up the company name with a certain design and then created a hover color, adding a nice visual effect. Next, we set up three classes: container, left, and right. These define the constraints for elements added to the left and right sides of the pages, as well as delineate the animations, sizes, and images used. Then, we have a class called “header” which accounts for differently-styled texts, as well as a “form-field” class, which gives the boxes a blue border when selected and a button with an aesthetic linear gradient. Finally, we included two sets of keyframes (move and left) that detail how the animations looks, and then we set up the animation as well as its subclasses to have delays (making the website flow in smoothly). All in all, this stylesheet has the font, background, text, and animations needed to build the website’s groundwork.

User-portal.css: Same as login-style.css, but the image is changed.

Form.css: Same as login-style.css, but the body text is centered, and a form style guide is created, in that the form has margins in the middle and a shadow. Form control, then, aligns the text and adds custom style to the form selection process.

Songs.css: Same as login-stlye.css, but “left” is styled to have the same style as the “form” in form.css, but without the “form-control” pieces. As well, the “company-name:hover” is made white.

Now, let’s go over the .html files. This is a much simpler process, as .html files encode the actual text and content, not design.

Register.html: We set the file as an HTML file, include meta fields to allow browser compatibility, and then fill out the body section to have all the text and forms needed for registration for our website.

Login.html: Similar to register.html, but the form-fields and buttons are reduced so that only the login is available.

User.html: Simple in design, but features a logout button in the top left and text that takes the user to the form and allows them to see their previous result.

Form.html: This page features the most text, insofar that all the questions and their answers are written into this page’s form.

Songs.html: This page features a lot of Jinja, insofar that the user gets a table printed with their specific data from the form submission.

Apology.html: This page comes from the Finance problem set. An Error is printed based on what has gone wrong in registration, and the user is redirected to register.html (/register).

Apology2.html: This page is the same as the apology.html, but the redirect button routes to user.html (/user).


# Backend

To begin, let’s go through each of our .py files: 

Helpers.py: In this python file, we have two important functions in relation to the login and error checking parameters of our program, which was provided for the finance CS50 PSET. For the apology function, it returns new special characters when old ones are inputted through the escape function and also returns apology.html in order to provide a page in which presents the user with an error they may have run into while going through the website. This may be inputting login parameters that don’t exist or writing two different passwords when registering. It also has a login_required function which was obtained from the finance PSET as well (so no need to get in depth on what that does here). 

Database.py:  In this python file, we insert each row of the CSV file into the quizzify.db file that we created. We do this by opening the “top10s.csv” file, give it a name, and then use the csv reader function in order to read it. We then use the python next() function in order to return the next item in the iterator reader and assign it to a variable called headers. We also pop the first row in the csv file in order to not input it onto our database. Importantly, we include a for loop that for each row in the csv file, we conduct a SQL INSERT INTO statement in order to add all the columns of each row of the csv file into the db file. 

app.py (high level): After importing everything, we first configure the application and the session to use the filesystem instead of signed cookies through linking Flask to the app and using app.config. Later, we configure our CS50 library to use the SQLite database we have created, quizzify.db. Next we conduct an after request, which ensures responses aren't cached.  

app.py (register): Our register route is “/register” and uses the methods of GET and POST. In the register function to register a new user, our program conducts a conditional statement to see whether the user’s request method was POST or GET. If it is POST, then the program requests the username, password, and confirmation from the form in order to conduct a series of error-checking conditionals, such as making sure the user inputted a username, password, or confirmation, as well as making sure the password matched the confirmation. After also checking if a username that the user inputted exists through another error checking statement, the register function adds the new user to the database by adding their username and a hash of their password into the users table of quizzify.db. This then logs the user in and redirects them to the home page of our website. If the request method is GET, then the program just renders the register.html template again for the user. 

app.py (login): Our register route is “/login” and uses the methods of GET and POST. The login function starts with clearing a session in order to forget any user_id. This function also conducts a conditional statement to see whether the user’s request method was POST or GET. If POST, then the program requests the username and password to conduct error checking statements to see if a username or password was submitted, as well as query the database to see if there is a username that matches the current user's input for such username and checks if the password is correct. It then sets session[“user_id”] and session[“username”] equal to certain elements in the rows variable—which queries the database for a username—in order to remember which user has logged in. It then redirects the user to the home page. If GET, the function just renders the login.html template. 

app.py (logout): Our logout route is “/logout”. The logout function is super simple, as it just clears the current session and redirects the user to the login form. 

app.py (/): Our home page route is “/”. In the index function, this just returns the user.html template under the username of the current session, denoted as session[“username”].  

app.py (songs): Our songs route is “/songs” and uses the method of GET. To start, the display function initializes the user_id variable to the session[“user_id”]. Next, it conducts a SQL query to get the variables from the recommendation table where the user_id is that of the person who is logged in, ordering it by id in descending order and limiting it to one. It then conducts an if statement to see if the length of list1 gotten through the SQL query is equal to 0, because, if it is, then it will return an apology statement because it means that the user has yet to fill out a form. We implemented this feature because it means that the user would be able to click a button from the homepage to see their most previous quiz results; we conduct this error checking in order to make sure a new user submits a quiz in the first place. Next, we conduct another SQL query into list2 to select all of our variables from the songs table where the song id is in the song id from the tables_id table, conducting a nested select here. We then conduct a conditional to check if there are elements in list2 to provide different statements for the user depending on whether their quiz results matched to certain songs or not. We then render the template for songs.html.  

app.py (form). Our form route is “/form” and uses the methods GET and POST. To start, it gets the user_id of the user in the current session. If POST, it initializes all of our 5 variables to 0 and puts them in a list called values. We then create an array for each of the questions, assigning values into the array corresponding to what values we want to give to certain answers from 1 through 5 in the quiz. We then conduct a for loop that iterates through each of the 10 questions, creating a string variable that appends “numbers” to whatever number question the loop is on. It then conducts an error-checking conditional statement to make sure the user gave an answer for that question. Then there’s a nested for loop that goes from 1 through 5 to determine which place in the array matches with the user’s answer in order to set the assigned value within the array to the user’s chosen value from the question. It then adds it to the sum. Next, there’s a mod conditional to go through every two of the questions in order to set each variable in the values list to the average of the assigned values the user obtained from their answers. Then, the program sets bounds for each five of the variables and conducts a SQL query to determine which songs fit into the range of all of the 5 variables obtained from the user’s quiz answer results. It then inserts the user’s preferred listening variables from the quiz into the recs table and then gets the most recent recs_id from the recs table. Then, for each song in the result list gotten from the query for what songs match the user’s listening preferences, we conduct a for loop to insert the user, song, and recommendation ids into another table called tables_id, which stores all of the ids needed for each query in the songs route. It then redirects the user to the songs page. If GET, the function renders the form.html template.
