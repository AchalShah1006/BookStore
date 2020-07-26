import os

from flask import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE_URL = "postgres://eifioctroozojj:20d3ca6dd8fd403f9adb9e58e46a6273ae2e7dd31066ce06b9c0b417f6ed4c31@ec2-34-195-169-25.compute-1.amazonaws.com:5432/da19bikahiqjh6"

# Set up database
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))

def main():
    # Create User Table
    engine.execute('CREATE TABLE users ('
        'id SERIAL PRIMARY KEY,'
        'username VARCHAR UNIQUE NOT NULL,'
        'password VARCHAR NOT NULL);')  
    print("User Table Created")

    # Create Books Table
    engine.execute('CREATE TABLE books ('
        'isbn VARCHAR PRIMARY KEY,'
        'title VARCHAR  NOT NULL,'
        'author VARCHAR NOT NULL,'
        'year VARCHAR  NOT NULL);')
    print("Book Table Created")

    # Create Review Table
    engine.execute('CREATE TABLE reviews ('
        'id SERIAL PRIMARY KEY,'
        'username VARCHAR  NOT NULL,'
        'rating VARCHAR  NOT NULL,'
        'review VARCHAR  NOT NULL,'
        'book_id VARCHAR NOT NULL);')
    print("Reviews Table Created")

if __name__ == "__main__":    
    main()