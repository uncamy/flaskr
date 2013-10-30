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
def init_datab():
    with closing(connect_datab()) as datab:
        with app.open_resource('schema.sql', mode ='r') as read_database:
            datab.cursor().executescript(f.read())
            datab.commit()

#create our application :)!
my_app = Flask(__name__)
my_app.config.from_object(__name__)
def connect_datab():
    return sqlite2.connect(app.config['DATABASE'])
if __name__ == '__main__':
   my_app.run()

@app.before_request
def before_request():
    g.datab = connect_datab()

@app.teardown_request
def teardown_request(exception):
    datab = getattr(g, 'datab', None)
    if db is not None:
        db.close()

@app.route('/')
def show_entries():
    get_item = g.datab.execute('select title, text from entries order by id desc')
    blog_post = [dict(titile=row[0], text=row[1]) for row in get_item.fetchall() ]
    return render_template('show_entries.html', entries = blog_post)


@app.route('/add', methods = ['POST'])
def new_entry():
    if not session.get('logged_in'):
        abort(401)
        g.datab.execute('insert into entries (title, text) values (?, ?)',
                        [request.form['title'], request.form['text']])
        g.datab.commit()
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
