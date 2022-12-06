import cs50
import csv
from cs50 import SQL


db = SQL("sqlite:///quizzify.db")

# insert each row of the CSV file into the quizzify.db file that we created
# use the csv reader function in order to read csv file 
with open("top10s.csv") as f:
        reader = csv.reader(f)
        # return the next item in the iterator reader and assign it to a variable called headers
        headers = next(reader)
        # pop the first row in the csv file in order to not input it onto our database
        headers.pop(0)
        for row in reader:
            db.execute("INSERT INTO songs (title, artist, genre, year, bpm, energy, dance, dB, live, val, duration, acoustic, speech, pop) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])

