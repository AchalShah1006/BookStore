import os, requests, csv
from flask import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = "postgres://eifioctroozojj:20d3ca6dd8fd403f9adb9e58e46a6273ae2e7dd31066ce06b9c0b417f6ed4c31@ec2-34-195-169-25.compute-1.amazonaws.com:5432/da19bikahiqjh6"


# Check for environment variable
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(DATABASE_URL)
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
