import csv
import os
import sqlite3

from flask import Flask, render_template, redirect, url_for, request, flash, session, g
from flask_login import login_required, logout_user, LoginManager, login_user, UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from forms import ContactForm, NewFriendForm, LoginForm

app = Flask(__name__, template_folder='templates')
app.secret_key = 'c66f0ce482c84e61a302750812fc7a36da2eaae6681a1a33'
app.config['UPLOAD_PHOTOS_DEST'] = 'data/photos/'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['USE_SESSION_FOR_NEXT'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///data/msg.sqlite"
db = SQLAlchemy(app)
conn = sqlite3.connect("data/msg.sqlite", check_same_thread=False)


class DBMsg(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    email = db.Column(db.Text(), nullable=False)
    message = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return "<Contact information from {}({}): {}>".format(self.name, self.email, self.message)


class User(UserMixin):
    def __init__(self, username, password=None):
        self.id = username
        self.password = password


# only one admin user
u = User(username='admin', password='abcde')


@login_manager.user_loader
def load_user(user_id):
    return u


@app.route('/')
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/experience')
def experience():
    return render_template('experience.html')


@app.route('/projects')
def projects():
    return render_template("projects.html")


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # use Post/Redirect/Get
    form = ContactForm()
    if form.validate_on_submit():
        # create db.Model object and insert it into database
        msgobj = DBMsg(name=form.name.data, email=form.email.data, message=form.message.data)
        db.session.add(msgobj)
        db.session.commit()
        return redirect(url_for('contact_response', name=form.name.data))
    return render_template('contact.html', form=form)


@app.route('/contact_response/<name>')
def contact_response(name):
    return render_template('contact_response.html', name=name)


@app.route('/friend_data', methods=['POST'])
def friend_data():
    return render_template('friend_data.html', form=request.form,
                           checkboxes=request.form.getlist('checkbox_group'))


@app.route('/new_friend', methods=['GET', 'POST'])
def new_friend():
    form = NewFriendForm()
    if form.validate_on_submit():
        if request.method == "POST" and request.files:
            f = form.photo.data
            f.save(os.path.join(
                app.config['UPLOAD_PHOTOS_DEST'], secure_filename(f.filename)))
        with open('data/newfrienddata.csv', 'a') as ff:
            writer = csv.writer(ff)
            writer.writerow([form.name.data, form.phonenumber.data, form.age.data, form.radio_group.data,
                             form.select.data, form.accounts.data, form.photo.data, form.description.data])
        return render_template('friend_data.html', form=request.form,
                               checkboxes=request.form.getlist('checkbox_group'))
    return render_template('friend_form.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == u.id and form.password.data == u.password:
            login_user(u)
            flash('Logged in successfully.')
            next_page = session.get('next', '/') # if log in successfully, redirect page to home page
            session['next'] = '/'
            return redirect(next_page)
        else:
            flash('Incorrect username/password!')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/protected')
@login_required
def protected():
    prefix = '/data/'
    # change tuples to dictionaries
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('select * from messages')
    return render_template('protected.html',
                           rows=c.fetchall(), # fetch all rows in the table in database
                           prefix=prefix)


if __name__ == '__main__':
    app.run(debug=True)