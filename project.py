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
database = None
DATABASE = ''

#Data base connection 
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
#-----------------------------------------------------------------------------


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
    return render_template("shop.html")


#Admin login 
@app.route('/login' , methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        #if user is correct then gain log in key
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Username or Password, please try again'
        else: 
            session['logged_in'] = True
            flash('You are logged in as Admin')
            return redirect(url_for('home'))
    return render_template("login.html", error=error)

#Logout
@app.route('/logout')
@login_required
def logout():
    #removes login key
    session.pop('logged_in', None)
    flash('You have logged out')
    return redirect(url_for('index')) 

#Debuging incase of error
if __name__ == '__main__':
    app.run(debug=True)
