import os, requests
from flask import *
#from models import *
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"]=os.urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
#db.init_app(app)

#       Index Route
@app.route('/')
def index():
    return render_template('index.html')
    
#       Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        #session['user'] = False
        name = request.form['username']
        password = request.form['password']
        #data = db.execute("SELECT * FROM users WHERE username = :name and password =:password",
        #{"name": name, "password": password})
        data = db.execute('SELECT * FROM users WHERE username=:name and password=:password',
        {"name":name, "password":password}).fetchone()
        print(data.username)
        if data is not None:
            session["user_id"] = name
            session["user"] = True
            return render_template("index.html", name = name)
        return render_template("login.html", error = "Username or Password not matched!")
    return render_template("signup.html")

#       Sign Up Route
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        name = request.form['username']
        passw = request.form['password']
        db.execute("INSERT INTO users (username, password) VALUES  (:name, :passw)",
        {"name": name, "passw": passw})
        db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('login'))
    return redirect(url_for('index'))
    
#       Logout Route
@app.route("/logout")
def logout():
    session.pop("user_id", None)  
    session["user"] = False
    return redirect(url_for('index'))

#       Search For Book Route
@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search = request.form.get('getinput')
        data = db.execute("SELECT * FROM books WHERE isbn= :isbn", # or title= :title or author= :author
        {"isbn": search}).fetchall()#, "title": search, "author": search
        if book is None:
            abort(404)
        return render_template("books.html", isbns = data.isbn, title = data.title, author = data.author, year = data.year)
    return "HELLO"

@app.route("/book/<id>", methods=['GET', 'POST'])
def book(id):
    if request.method == 'POST':
        _book = db.execute("SELECT * FROM books WHERE isbn= :id",
        {"id": id}).first()
        return render_template("books.html", author = _book.author,  title = _book.title, isbns = _book.isbn, year = _book.year)
    return redirect(url_for('signup'))

#       API Route
@app.route("/api/<isbn>")
def api(isbn):
    getapi = db.execute("SELECT * FROM books WHERE isbn= :isbn",
    {"isbn": isbn}).first()
    if getapi is None:
        return jsonify({
            'error': 'No Books Found'
        })
    #   Api GoodReads
    url = "https://www.goodreads.com/book/review_counts.json"
    data = requests.get(url, params={ "key": "ekMV24VguYBUOSeqlhwdnw", "isbns": isbn})
    data = data.json()
    _count = data['books'][0]['reviews_count']
    _avg_rating = data['books'][0]['average_rating']
    return jsonify({ 
        'books': {
            'reviews_count': _count, 
            'title': getapi.title,
            'author': getapi.author,
            'year': getapi.year,
            'isbn': getapi.isbn, 
            'average_rating': _avg_rating
            }
        })


if __name__ == "__main__":     
    app.run()
    