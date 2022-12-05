# Readme.md


# Overview

Welcome to Quizzify: a personality quiz that matches you with music you’d be likely to listen to. Using an algorithm based on a personality questionnaire, we compute certain metrics for a user: dance levels, energy levels, year, bpm, and live studio sound. These metrics are then compared to a database of 1000+ Billboard Top 100 songs from 2010-2019, and then, the songs that fit the user’s parameters are recommended. The website operates through flask and is tied to a database that features tables for users, songs, and recommendations. CSS and HTML files create the design, and python runs the application for the website. 


# Project’s Beginning

This project first began with the idea that songs have certain metrics according to Spotify API data. There are several metrics Spotfiy calculates using an algorithm (danceability, energy, valence, year, bpm, etc. ). We found this data interesting and practical for implementation. Though we eventually abandoned connecting directly to the Spotify API, we still accessed a database of  Spotify-valued songs through Kaggle to simulate the API environment. As such, to start, we had a .csv file with 1000+ songs and their metrics, and an idea.

We quickly realized that we would need an interface to have users register and login with our service. This feature is something we coded when doing our Finance problem set. This prior work helped us figure out what we need to implement to make the user login work: Flask (Python framework) and Jinja (Python web template). As well, we knew we needed HTML files for the web pages, CSS files for style, SQL databases to parse through information, and python to run our application.


# First Steps

After copying and pasting the baseline code from Finance, we began by downloading Github for Desktop and DB Browser for SQLite. Github allowed my partner Santi and me to work together in the same repository, pushing and pulling onto our main branch to easily transfer code. Getting that program set up took some time, but having Github paid off in the long run. Then, DB Browser gave us a visual interface with which we could easily create tables, modify them, and use the data to build our application.

Now, we will detail the simultaneous development that went on in both the frontend and backend.


# Frontend

On the frontend, we really wanted our design to stick out. The frontend from finance was relatively bland (no offense). We wanted a more minimalist vibe, one accompanied by animations, fun gradients, and cool art. To do so, we set out to find a guide that matched our needs. Luckily, we found a fantastic guide on YouTube that detailed how to build animations in a CSS file. By figuring out how to tailor the guide to our needs, we coded all the animations and style through CSS while preserving the functionality afforded to us by the code from Finance. This included creating a custom navbar, adding a “left” and “right” side of the page that both conformed to different animation and containers, and adding animations through keyframes and animation-move. This design is strong, insofar that the CSS table can be quickly modified to include different animations, fonts, and placement on the different web pages if needed. 

However, it’s worth noting that we do not have a “layout.html” file that gives a template for each page. Rather, each page is static. If we had more time for this project, we would have created a template for our pages, but given the time constraints, we found it easier to make static files for each one. As well, it’s important to note how that “form.html” and “songs.html” both include custom designs for forms and tables that make the design cleaner (a hover feature for songs, and a centered box with a shadow for the form, etc.)


# Backend

The backend process began with the baseline from finance. But we generated all the tables on our own using DB Browser.

For starters, we have four crucial tables: users, songs, recs, and tables_id. The users table stores all the information from “/register” so that a user database exists. Then, the songs tables store all the parsed information from our .csv files. This parsing is completed by a python script “database.py” that goes through the .csv file and runs a db.execute and inserts all the information we need from the .csv file into the songs table. Then, the recs table stores all the recommended songs following “app.py” computing the form’s values. Finally, “tables_id” exists so that a nested select works. These tables form the basis of our backend. The great thing about this design is that any .csv file can be parsed through and used so long as the table has Spotify’s metrics. As such, our code is modular in design, allowing for other lists to be used as long as Spotify’s data is present.

Then, we have two python files: app.py and database.py. These run the application and the parsing of data. These files are explained in design.md.
