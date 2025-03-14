import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate  # Import Flask-Migrate

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Create base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize SQLAlchemy with the base class
db = SQLAlchemy(model_class=Base)

# Create Flask app
app = Flask(__name__)

# Set secret key for session management
app.secret_key = os.environ.get("SESSION_SECRET", "tyledeclouds_default_secret")

# Configure database connection
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///tyledeclouds.db")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the app with the database extension
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Import routes and models after app initialization to avoid circular imports
with app.app_context():
    from models import User, ContactMessage  # Ensure models are registered with SQLAlchemy
    
    # Optionally create database tables.
    # If you are using migrations, you can remove or comment this out.
    # db.create_all()
    
    # Import and register routes
    from routes import register_routes
    register_routes(app)
