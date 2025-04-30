from flask import render_template, url_for, flash, redirect, request, jsonify
from models import User, Property
import os
from bk_config import app, db, bcrypt, limiter
from flask_login import login_user, current_user
import uuid
import jwt
import datetime
from functools import wraps

@app.route('/home')
def home():
    return render_template('home.html')

'''The following routes are for logging in, registering, and logging out'''
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    #validate email
    existing_user_email = User.query.filter_by(email=email).first()
    existing_user_name = User.query.filter_by(user_name=username).first()
    if existing_user_email:
        return jsonify({'message':'This EMAIL is already taken try another one!'})
    if existing_user_name:
        return jsonify({'message':'This USERNAME is already taken try another one!'})
    # Validate input data
    if not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create a new user instance
    new_user = User(user_name=username, email=email, password=hashed_password,
                    user_id=str(uuid.uuid4()))

    # Save to the database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limit to prevent brute-force attacks
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Validate input data
    if not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    # Retrieve user from the database
    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, os.getenv('SECRET_KEY'), algorithm='HS256').decode('utf-8')

        return jsonify({'token': token}), 200  # Return JSON response
    
    return jsonify({'message': 'Invalid email or password'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    # Since JWT is stateless, the frontend should handle token removal.
    return jsonify({'message': 'Logged out successfully'}), 200

#validating the jwttoken
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing Please ensure that you are logged in!'}), 401

        try:
            data = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
            current_user = User.query.filter_by(user_id=data['user_id']).first()
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/add_listing', methods=['POST'])
@token_required
def add_listing(current_user):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    location = data.get('location')
    price_per_night = data.get('price_per_night')

    # Check if the user is a host and provide feedback if not
    if current_user.role != 'host':
        return jsonify({'message': 'Only hosts can add listings.'}), 403

    # Create a new property instance
    new_property = Property(
        property_id=str(uuid.uuid4()),  # Generate a unique ID for the property
        host_id=current_user.user_id,
        title=title,
        description=description,
        location=location,
        price_per_night=price_per_night
    )

    # Save to the database
    db.session.add(new_property)
    db.session.commit()

    return jsonify({'message': 'Property listing added successfully.'}), 201

@app.route('/upgrade_user', methods=['PUT','POST'])
@token_required
def upgrade_user(current_user):
    data = request.get_json()
    national_id = data.get('national_id')

    # Validate national ID
    if not national_id:
        return jsonify({'message': 'National ID is required.'}), 400

    # Check if the user is already a host
    if current_user.role == 'host':
        return jsonify({'message': 'User is already a host.'}), 400

    # Update the user's role to host
    current_user.role = 'host'
    db.session.commit()

    return jsonify({'message': 'User role upgraded to host successfully.'}), 200
