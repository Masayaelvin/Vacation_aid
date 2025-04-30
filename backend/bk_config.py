from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from dotenv import load_dotenv 
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager

# Load environment variables from .env file
load_dotenv()

# Get credentials from environment variables
host = os.getenv("DB_HOST")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")

#instatiate application
app = Flask(__name__)

#app configuratios
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{user}:{password}@{host}/{database}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.app_context().push()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login' 
login_manager.login_message_category = 'info'

# Configure Flask-Limiter
limiter = Limiter(
    get_remote_address,  # Uses the client's IP address for rate limiting
    app=app,  # Attach to the Flask app
    default_limits=["200 per day", "50 per hour"]  # Default rate limits for all routes
)

import routes
