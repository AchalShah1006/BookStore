import os, requests
from flask import *
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

key = "ekMV24VguYBUOSeqlhwdnw"
DATABASE_URL = "postgresql://eifioctroozojj:20d3ca6dd8fd403f9adb9e58e46a6273ae2e7dd31066ce06b9c0b417f6ed4c31@ec2-34-195-169-25.compute-1.amazonaws.com:5432/da19bikahiqjh6"

app = Flask(__name__)



# Configure session to use filesystem
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"]=os.urandom(24)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(DATABASE_URL)
db = scoped_session(sessionmaker(bind=engine))
# db.init_app(app)
     
#GoodRead API
def gdApi(isbn):
    data = requests.get("https://www.goodreads.com/book/review_counts.json", params={ "key": key, "isbns": isbn})
    print(data)
    data = data.json()
    return data

# HomePage Route
@app.route('/')
def index():
    if 'user_id' in session:
        name = session["user_id"].capitalize()
        return render_template("index.html", name = name)
    return render_template('index.html')
    
# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        name = request.form['username']
        password = request.form['password']
        
        # Validation for existing User
        data = db.execute("SELECT * FROM users WHERE username=:name and password=:password",
        {"name":name, "password":password}).fetchone()
        if data is not None:
            session["user_id"] = name
            session["user"] = True
            return redirect(url_for('index'))
        return render_template("login.html", error = "Username or Password not matched!")
    return render_template("signup.html")

# Sign Up Route
@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        name = request.form['username']
        passw = request.form['password']

        existed = db.execute("SELECT username FROM users WHERE username=:name",
        {"name":name}).fetchone()
        
        # Submit New User Details into DB
        if existed is None: 
            db.execute("INSERT INTO users (username, password) VALUES  (:name, :passw)",
            {"name": name, "passw": passw})
            db.commit()
            flash('New entry was successfully posted')   
        else:
            return render_template("error.html", error = "UserName Already Exist. Try Diffrent Name") 
        return redirect(url_for('login'))
    return redirect(url_for('index'))
    
# Logout Route
@app.route("/logout")
def logout():
    # Removing User From Session
    session.pop("user_id", None)  
    session["user"] = False
    return redirect(url_for('index'))

# Search For Book By ISBN, Title and Author Name.
@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        abort(403)
    if request.method == 'POST':
        search = request.form.get('getinput')
        data = db.execute("SELECT * FROM books WHERE (isbn LIKE '%' || :isbn || '%') OR (title LIKE '%' || :title || '%') OR (author LIKE '%' || :author || '%') ORDER BY year DESC", 
        {"isbn": search, "title": search, "author": search}).fetchall()
        
        # If Book Does Not Exist In DB
        if not data:
            return render_template("error.html", error="No Books Found")
        # Creating Session For List Items of Books
        session["val"] = True
        session["book"] = False
        return render_template("books.html", data = data) 
    return "HELLO"

# Book Data => Reviews Rating etc
@app.route("/book/<id>", methods=["GET", "POST"])
def book(id):
    comments= []
    user = session["user_id"]

    # If User Submit The Review And Rating Then This Section Will Response
    if request.method == 'POST':
        isbn = request.form["post_id"]
        review = request.form["review"] 
        rating = int(request.form["rating"])
        book = db.execute("SELECT * FROM reviews WHERE username= :username AND book_id= :book_id",
        {"username": user, "book_id": isbn}).first()
        if book == None:
            db.execute("INSERT INTO reviews (username, rating, review, book_id) VALUES (:username, :rating, :review, :book_id)",
            {"username": user, "rating": rating, "review": review, "book_id": isbn})
            db.commit()
        return redirect(url_for('book', id = isbn))
    # ===== END ======

    if request.method == "GET":
        if 'user' not in session:
            return redirect(url_for('login'))

        # Creating Session For Books
        session["val"] = False
        session["book"] = True
        book = db.execute("SELECT * FROM books WHERE isbn= :id",
        {"id": id}).first()   

        # Search The Reviews And Rating Of The Book in DB
        data = db.execute("SELECT * FROM reviews WHERE username= :username AND book_id= :id",
        {"username": user,"id": id}).first()
        if data is None:
            session["review"] = False
        else:
            session["review"] = True
            comments = data

    # GoodRead Api Data
        api = gdApi(id)

    return render_template("books.html", book = book, api = api, comments = comments)


    

# API => Get JSON Data 
@app.route("/api/<int:isbn>", methods=['GET', 'POST'])
def api(isbn):
    if request.method == 'GET':
        dbapi = db.execute("SELECT * FROM books WHERE isbn= :isbn",
        {"isbn": isbn}).first()
        if dbapi is None:
            return jsonify({
                'error': 'No Books Found'
            })

        # GoodRead Api Data
        api = gdApi(isbn)

        # Return JSON Data
        return jsonify({ 
            "books": {
                "reviews_count": api["books"][0]["reviews_count"], 
                "title": dbapi.title,
                "author": dbapi.author,
                "year": dbapi.year,
                "isbn": dbapi.isbn, 
                "average_rating": api["books"][0]["average_rating"]
                }
            })



if __name__ == "__main__":     
    app.run()
    