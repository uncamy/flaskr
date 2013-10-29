import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

#configuration 
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create schema 
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode ='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#create our application :)! 
app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite2.connect(app.config['DATABASE'])

if __name__ == '__main__':
    app.run()




