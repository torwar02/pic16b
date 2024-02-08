'''
At the command line, run 

conda activate PIC16B-24W
export FLASK_ENV=development
flask run

# Sources

This set of lecture notes is based in part on previous materials developed by [Erin George](https://www.math.ucla.edu/~egeo/) (UCLA Mathematics) and the tutorial [here](https://stackabuse.com/deploying-a-flask-application-to-heroku/). 
'''
import sqlite3
import pandas as pd
#html changes dinamically when we use flask, and this is one of the easier ways to do it
#(base) ziongassner@Zions-MacBook-Air Downloads % cd flask_1
#(base) ziongassner@Zions-MacBook-Air flask_1 % conda activate PIC16b-24W
#(PIC16b-24W) ziongassner@Zions-MacBook-Air flask_1 % export FLASK_ENV = development
#zsh: bad assignment
#(PIC16b-24W) ziongassner@Zions-MacBook-Air flask_1 % FLASK_ENV=development
#(PIC16b-24W) ziongassner@Zions-MacBook-Air flask_1 %
from flask import g, Flask, render_template, request #Flask class is the most important, other things just help out
from flask import redirect, url_for, abort

app = Flask(__name__) #Making a Flask object with `__name`--all HTML files go here.

# www.google.com/
@app.route("/") # decorators #Route method of the Flask instance. Decorators are functions that modify functions.
def redirect_page():
    return redirect(url_for("submit"))


@app.route("/submit/", methods=['POST', 'GET']) #Two different methods in the API
def submit():
    if request.method == 'GET':
        # if the user just visits the url
        return render_template('submit.html')
    else:
        insert_message(request)
        return render_template('submit.html', sec = True)

@app.route("/view/")
def view():
    if request.method == 'GET':
        postings = random_messages(5)
        length = 5
        message_tuples = []
        for i in range(length):
            message_tuples.append(tuple(postings.iloc[i,:]))
        return render_template('view.html', message_tuples = message_tuples)
    
    
def get_message_db():
    try:
        return g.message_db
    except:
        g.message_db = sqlite3.connect("messages_db.sqlite")
        cursor = g.message_db.cursor()
        cmd = """
        CREATE TABLE IF NOT EXISTS messages(
        handle TEXT,
        message TEXT
        );
        """
        cursor.execute(cmd)
        cursor.close()
        return g.message_db
        
def insert_message(request):
    message = request.form['message']
    handle = request.form['handle']
    db = get_message_db()
    info = pd.DataFrame([{'handle': handle, 'message' : message}])
    info.to_sql("messages", db, if_exists = "append", index = False)
    db.commit()
    db.close()
    
def random_messages(n):
    
    db = get_message_db()
    cmd = f""" SELECT * FROM messages ORDER BY RANDOM() LIMIT {n}; """
    postings = pd.read_sql_query(cmd, db)
    db.close()
    return postings
    
