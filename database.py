import cs50
import csv
from cs50 import SQL


db = SQL("sqlite:///quizzify.db")

# print(db.execute("SELECT * FROM Users;"))

print("START")
with open("top10s.csv") as f:
        reader = csv.reader(f)
        headers = next(reader)
        headers.pop(0)
        for row in reader:
            db.execute("INSERT INTO songs (title, artist, genre, year, bpm, energy, dance, dB, live, val, duration, acoustic, speech, pop) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14])

