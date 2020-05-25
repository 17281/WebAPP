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
app.database = "Menu.db"


def connect_db():
    return sqlite3.connect(app.database)

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

@app.route('/home', methods=['GET', 'POST'])
def home():
    #if session['logged_in'] in session: 
        #CHANGE stuff only if admin logs in-------
    g.db = connect_db() #estabilshes database connection
    cur = g.db.execute('select * FROM Food')
    posts = [dict(Name=row[0], Description=row[1]) for row in cur.fetchall()]
    return render_template("shop.html", posts=posts) #renders a templet 


#Admin login 
@app.route('/login' , methods=['GET', 'POST'])
def login():
    #if user already logged in
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
@login_required
def logout():
    #removes login key
    session.pop('logged_in', None)
    flash('You have logged out') #tells user that they logged out
    return redirect(url_for('index')) #send user back to index page

#Debuging incase of error
if __name__ == '__main__':
    app.run(debug=True)
