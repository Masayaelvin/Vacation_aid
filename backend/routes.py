from flask import render_template, url_for, flash, redirect
from backend import app, db
from models import User, Property, Excursion, Booking, BookingExcursion
from backend.forms import RegistrationForm, LoginForm
import uuid
from backend import encrypt

@app.route('/home')
def home():
    return render_template('home.html')


app.route('/register', methods=['POST'])
def register():
    pass

app.route('/login', methods=['POST'])
def login():
    pass

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    pass
