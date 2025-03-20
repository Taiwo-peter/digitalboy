import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set secret key for session management
app.secret_key = os.environ["SESSION_SECRET"]

# Configure database connection using DATABASE_URL
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import routes and models after app initialization
with app.app_context():
    from models import User, ContactMessage  # Example model imports
    from routes import register_routes
    register_routes(app)

# Optionally, create tables (but you may want to use migrations)
# db.create_all()

