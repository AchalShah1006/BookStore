import os

from flask import *
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")



# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
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