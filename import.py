import os, requests, csv
from flask import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker




# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
#db.init_app(app)



def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn,title,author,year) VALUES (:isbn, :title, :author, :year)",
        {"isbn":isbn,"title":title, "author":author, "year":year})
        db.commit()
        print("Added Book With ISBN: " + isbn + " Title: " + title +  " Author: " + author + " Year: " + year)
    return (print("Data Submitted"))

if __name__ == "__main__":
        main()
