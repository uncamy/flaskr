import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort,\
                  render_template, flash
from contextlib import closing

app = Flask(__name__)

#configuration
app.config.update(dict(
    DATABASE = '/tmp/flaskr.db'
    DEBUG = True
    SECRET_KEY = 'development key'
    USERNAME = 'admin'
    PASSWORD = 'default'
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


# create schema
def connect_db():
    """connects to the database"""
    rv =sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode ='r') as open_database:
            db.cursor().executescript(open_database.read())
            db.commit()

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    cur  = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(titile=row[0], text=row[1]) for row in get_item.fetchall() ]
    return render_template('show_entries.html', entries = entries)


@app.route('/add', methods = ['POST'])
def new_entry():
    if not session.get('logged_in'):
        abort(401)
        g.db.execute('insert into entries (title, text) values (?, ?)',
                        [request.form['title'], request.form['text']])
        g.db.commit()
        flash('New entry wasa succcessfully posted')
        return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error_msg = 'Invalid username'
        elif request.form['password'] != app.config ['PASSWORD']:
            error_msg = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
        return render_template('login.html', error = error_msg)

@app.route('/logout')
def signout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
   app.run()
