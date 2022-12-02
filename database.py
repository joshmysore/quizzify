import cs50
import csv

# db = SQL("sqlite:///quizzify.db")
# print(db.execute("SELECT * FROM Users;"))

print("START")
with open("top10s.csv") as f:
        reader = csv.reader(f)
        headers = next(reader)
        headers.pop(0)
        for row in reader:
            print(row)