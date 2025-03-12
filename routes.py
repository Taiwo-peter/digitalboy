import json
import logging
from flask import render_template, request, jsonify, redirect, url_for
from app import db
from models import User, ContactMessage

def register_routes(app):
    """Register all routes with the Flask application"""
    
    # Static page routes
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/home.html')
    def home():
        return render_template('home.html')
    
    @app.route('/services.html')
    def services():
        return render_template('services.html')
    
    @app.route('/aboutus.html')
    def aboutus():
        return render_template('aboutus.html')
    
    @app.route('/contactus.html')
    def contactus():
        return render_template('contactus.html')
    
    @app.route('/signup.html')
    def signup():
        return render_template('signup.html')
    
    # API endpoints
    @app.route('/api/signup', methods=['POST'])
    def api_signup():
        """Handle user registration"""
        try:
            data = request.json
            email = data.get('email')
            password = data.get('password')
            
            # Validate input
            if not email or not password:
                return jsonify({"error": "Email and password are required."}), 400
                
            # Validate email format
            email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            import re
            if not re.match(email_regex, email):
                return jsonify({"error": "Invalid email format."}), 400
                
            # Check password strength
            if len(password) < 6:
                return jsonify({"error": "Password must be at least 6 characters long."}), 400
                
            # Check if user already exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return jsonify({"error": "Email is already registered."}), 400
                
            # Create new user
            new_user = User(email=email)
            new_user.set_password(password)
            
            # Save user to database
            db.session.add(new_user)
            db.session.commit()
            
            return jsonify({"message": "Sign-up successful! Welcome to Tyledeclouds."}), 201
            
        except Exception as e:
            logging.error(f"Error during sign-up: {str(e)}")
            db.session.rollback()
            return jsonify({"error": "Internal server error. Please try again later."}), 500
    
    @app.route('/api/contact', methods=['POST'])
    def api_contact():
        """Handle contact form submissions"""
        try:
            data = request.json
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')
            
            # Validate input
            if not name or not email or not message:
                return jsonify({"error": "All fields are required."}), 400
            
            # Save contact message to database
            new_message = ContactMessage(name=name, email=email, message=message)
            db.session.add(new_message)
            db.session.commit()
            
            logging.info(f"New contact form submission: Name: {name}, Email: {email}")
            return jsonify({"message": "Your message has been received. We will get back to you soon!"}), 200
            
        except Exception as e:
            logging.error(f"Error saving contact message: {str(e)}")
            db.session.rollback()
            return jsonify({"error": "Internal server error. Please try again later."}), 500
    
    @app.route('/api/data')
    def api_data():
        """Example API endpoint to demonstrate data fetching"""
        return jsonify({"message": "Hello from the backend!"})
