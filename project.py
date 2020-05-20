'''
13/03/20,
Harry .C 
Project:webapp
'''
from flask import Flask, render_template, request, g, redirect, url_for
import sqlite3

DATABASE = 'User.db'
app = Flask(__name__)

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

database = None
#home page for the users
@app.route('/')
def home():
    cursor = get_db().cursor()
    error = None

    return render_template("index.html")

#Admin login 
@app.route('/login' , methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Username or Password, please try again'
        else: 
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template("login.html", error=error)

@app.route('/logout')
    def logout():
       session.pop('logged_in', None)
       return redirect(url_for('home')) 

#Debuging incase of error
if __name__ == '__main__':
    app.run(debug=True)
