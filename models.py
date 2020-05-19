import os, requests

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
url = "https://www.goodreads.com/book/review_counts.json"
data = requests.get(url, params={ "key": "ekMV24VguYBUOSeqlhwdnw", "isbns": "1632168146"})
data = data.json()
print(data)