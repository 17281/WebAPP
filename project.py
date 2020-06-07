'''
13/03/20,
Harry .C 
Project:webapp
'''
from flask import Flask, render_template, request, g, redirect, url_for, session, flash
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = "my precious"
DATABASE = "Menu.db"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else: 
            flash('Please login first')
            return redirect(url_for('login'))
    return wrap


#index page
@app.route('/')
def index():
    return render_template("index.html")

#Home Page
@app.route('/home', methods=['GET', 'POST'])
def home():
    #display all data from menu
    cursor = get_db().cursor()
    sql = ("SELECT * FROM Food")
    cursor.execute(sql)
    #reults == database
    results = cursor.fetchall()
    
    #Show user comments where ID = FoodID
    cursor = get_db().cursor()
    sql = ("SELECT User.Comments, User.CommentID FROM Food JOIN User ON Food.ID=User.FoodID")
    cursor.execute(sql)
    #comments == database
    comments = cursor.fetchall()

    return render_template("shop.html", results=results, comments=comments) #renders a templet 



#Admin login 
@app.route('/login' , methods=['GET', 'POST'])
def login():
    #if user already logged in then stop them
    if 'logged_in' in session:
            flash('You have logged in already')
            return redirect(url_for('home'))
    error = None
    if request.method == 'POST':
        #if user is correct then gain log in key
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Username or Password, please try again'
        else: 
            session['logged_in'] = True
            flash('You are logged in as Admin') #tell user that they logged in
            return redirect(url_for('home')) #Move to home if admin is true
    return render_template("login.html", error=error) #renders the templet

#Logout
@app.route('/logout')
@login_required #Need to login first before logout
def logout():
    #removes login key
    session.pop('logged_in', None)
    flash('You have logged out') #tells user that they logged out
    return redirect(url_for('index')) #send user back to index page


#Comment Deleting from Admin
@app.route('/delete', methods=["GET","POST"])
@login_required
def delete():
    if 'logged_in' in session:
        if request.method == "POST":
            #get item and delete with data base
            cursor = get_db().cursor()
            id = int(request.form["item_name"])
            sql = ("DELETE FROM User WHERE CommentID=?")
            cursor.execute(sql,(id,))
            get_db().commit()
    return redirect('/home')

#Comment Adding from users
@app.route('/add', methods=["GET",'POST'])
def add():
    if request.method == "POST":
        #adds comments into table
        cursor = get_db().cursor()
        new_name = request.form["Comment"]
        food_ID = int(request.form["FoodID"])
        #when the FoodID matches the texts ID
        sql = "INSERT INTO User (Comments,FoodID) VALUES (?,?)"
        cursor.execute(sql,(new_name,food_ID))
        get_db().commit()
    return redirect('/home')

#Debuging incase of error
if __name__ == '__main__':
    app.run(debug=True)
