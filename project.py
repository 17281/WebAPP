'''
13/03/20,
Harry .C 
Project:webapp
'''
from flask import Flask, render_template, request, g, redirect, url_for, session, flash
from jinja2 import Template
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = "my precious"
DATABASE = "Menu.db"

#Database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

#Close the Dadtbase if database doesn't connect
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

#For tasks which needs Login
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else: 
            #flashes a message
            flash('Please login first')
            return redirect(url_for('login'))
    return wrap


#index page
@app.route('/')
def index():
    return render_template("index.html")#Not needed
#================================================================================================

@app.route('/fill/<int:post_id>', methods=['GET', 'POST']) #automatic updating item id
def fill(post_id):
    #display all comments from User
    cursor = get_db().cursor()
    sql = ("SELECT Comments, CommentID, FoodID FROM User WHERE FoodID = ?")#selects the selected items where foodid = pic id
    cursor.execute(sql,(post_id,))
    
    results = cursor.fetchall()
    return render_template("comment.html", results=results, id=post_id)

#Home Page
@app.route('/home', methods=['GET', 'POST'])
def home():
    #display all data from menu
    cursor = get_db().cursor()
    sql = ("SELECT Food.Name, Food.Description, Food.Filename, Food.ID FROM Food")#selects the selected items where the Food id = Forein key
    cursor.execute(sql)
    #reults == database
    results = cursor.fetchall()
    print (results)
    return render_template("shop.html", results=results) #renders a templet 



#Admin login 
@app.route('/login' , methods=['GET', 'POST'])
def login():
    #if user already logged in then stop them
    if 'logged_in' in session:
            flash('You have logged in already')#tells user that they logged in
            return redirect(url_for('home'))#redirect them to home page
    error = None
    if request.method == 'POST':
        #if user is correct then gain log in key
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':#required correct input from user
            #If user input doesn't match up
            error = 'Invalid Username or Password, please try again'
        else: 
            session['logged_in'] = True
            flash('You are logged in as Admin') #tell user that they logged in
            return redirect(url_for('home')) #Move to home if admin is true
    return render_template("login.html", error=error) #renders the login page

#Logout
@app.route('/logout')
@login_required #Need to login first before logout
def logout():
    #removes login key
    session.pop('logged_in', None)
    flash('You have logged out') #tells user that they logged out
    return redirect(url_for('index')) #send user back to index page


#Comment Deleting from Admin
@app.route('/delete/<int:post_id>', methods=["GET","POST"])
@login_required
def delete(post_id):
    if 'logged_in' in session:
        error = None
        if request.method == "POST":
            #get item and delete with data base
            cursor = get_db().cursor()
            item_name = int(request.form["CommentID"])
            sql = ("DELETE FROM User WHERE CommentID=?")
            #Delete comments where id == selected delete button
            cursor.execute(sql,(item_name,))
            get_db().commit()
    return redirect(url_for("fill", post_id=post_id))#renders delete page 

#Comment Adding from users
@app.route('/add/<int:post_id>', methods=["GET",'POST'])
def add(post_id):
    if request.method == "POST":
        #adds comments into table=================================
        cursor = get_db().cursor()
        new_name = request.form["Comment"]

        if len(new_name) == 0:#IF user tries to add Blanks or over 100 words into database
            flash('Incorrect input: Comments can not be empty')#NO+++++ Prevents SPAMMERS
        elif len(new_name) > 50:
            flash('Incorrect input: Comments can not exced 50 letters')
        
        else:
            food_ID = int(request.form["FoodID"])
            #when the FoodID matches the texts ID
            sql = "INSERT INTO User (Comments,FoodID) VALUES (?,?)" 
            cursor.execute(sql,(new_name,post_id))#Execute sql
            get_db().commit()
    return redirect(url_for("fill", post_id=post_id))#renders add comment page

#Debuging incase of error
if __name__ == '__main__':
    app.run(debug=True)
