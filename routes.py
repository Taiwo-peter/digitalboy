import json
import logging
from flask import render_template, request, jsonify, redirect, url_for, session
from app import db
from models import User, ContactMessage
from werkzeug.security import check_password_hash
from functools import wraps

def login_required(f):
    """Decorator to require login for specific routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('signup'))
        return f(*args, **kwargs)
    return decorated_function

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
    
    # Detailed service pages (require login)
    @app.route('/cloud_migration.html')
    @login_required
    def cloud_migration():
        return render_template('cloud_migration.html')
    
    @app.route('/cloud_optimization.html')
    @login_required
    def cloud_optimization():
        return render_template('cloud_optimization.html')
    
    @app.route('/cloud_security.html')
    @login_required
    def cloud_security():
        return render_template('cloud_security.html')
    
    @app.route('/cloud_implementation.html')
    @login_required
    def cloud_implementation():
        return render_template('cloud_implementation.html')
    
    @app.route('/cloud_consulting.html')
    @login_required
    def cloud_consulting():
        return render_template('cloud_consulting.html')
    
    @app.route('/managed_services.html')
    @login_required
    def managed_services():
        return render_template('managed_services.html')
    
    # Authentication API endpoints
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
            
            # Set the user session
            session['user_id'] = new_user.id
            session['email'] = new_user.email
            
            return jsonify({"message": "Sign-up successful! Welcome to Tyledeclouds."}), 201
            
        except Exception as e:
            logging.error(f"Error during sign-up: {str(e)}")
            db.session.rollback()
            return jsonify({"error": "Internal server error. Please try again later."}), 500
    
    @app.route('/api/login', methods=['POST'])
    def api_login():
        """Handle user login"""
        try:
            data = request.json
            email = data.get('email')
            password = data.get('password')
            
            # Validate input
            if not email or not password:
                return jsonify({"error": "Email and password are required."}), 400
            
            # Find the user
            user = User.query.filter_by(email=email).first()
            
            # Check if user exists and password is correct
            if not user or not user.check_password(password):
                return jsonify({"error": "Invalid email or password."}), 401
            
            # Set the user session
            session['user_id'] = user.id
            session['email'] = user.email
            
            return jsonify({"message": "Login successful!"}), 200
            
        except Exception as e:
            logging.error(f"Error during login: {str(e)}")
            return jsonify({"error": "Internal server error. Please try again later."}), 500
    
    @app.route('/api/logout')
    def api_logout():
        """Handle user logout"""
        session.pop('user_id', None)
        session.pop('email', None)
        return redirect(url_for('index'))
    
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
    
    @app.route('/api/user/status')
    def api_user_status():
        """Check if user is logged in"""
        if 'user_id' in session:
            return jsonify({
                "logged_in": True,
                "email": session.get('email')
            })
        else:
            return jsonify({"logged_in": False})
