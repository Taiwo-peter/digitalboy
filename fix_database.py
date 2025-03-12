
from app import app, db
from models import User, ContactMessage

with app.app_context():
    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()
    
    print("Database tables have been successfully recreated.")
