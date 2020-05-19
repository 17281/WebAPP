'''
13/03/20,
Harry .C 
Project:webapp
'''
from flask import Flask,render_template,request,g,redirect
import sqlite3

app = Flask(__name__)




database = None
#home page for the users
@app.route ('/')
def home():
    return render_template("index.html")

#Admin login 
@app.route ('/login', methods=['GET,' 'POST'])
def login():
    error = None
    if request.method == 'POST':
        #if the password or username doesn't ==
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Password or Username, Please try again.'
        else:
            #if all correct
            return redirect(url_for('index.html'))
    return render_template("login.html", error=error)

#Debuging incase of error
if __name__ == '__main__':
    app.run(debug=True)
