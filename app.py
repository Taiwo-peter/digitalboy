import os
import logging
import stripe
from flask import Flask, render_template, session, redirect, url_for, jsonify, request

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Set secret key for session management
app.secret_key = os.environ.get("SESSION_SECRET", "tyledeclouds_default_secret")

# Initialize Stripe
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
stripe_publishable_key = os.environ.get("STRIPE_PUBLISHABLE_KEY")

# Service package prices
service_prices = {
    "basic": {
        "name": "Basic Cloud Package",
        "price": 999,  # $9.99
        "currency": "usd",
        "description": "Basic cloud consulting services package"
    },
    "standard": {
        "name": "Standard Cloud Package",
        "price": 2999,  # $29.99
        "currency": "usd",
        "description": "Standard cloud consulting services with implementation support"
    },
    "premium": {
        "name": "Premium Cloud Package",
        "price": 4999,  # $49.99
        "currency": "usd",
        "description": "Premium cloud consulting with full implementation and ongoing support"
    }
}

# Simple in-memory storage for demonstration
users = {}
payments = {}

# Define routes
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/services.html')
def services():
    if not session.get('logged_in'):
        return redirect(url_for('signup'))
    return render_template('services.html')

@app.route('/aboutus.html')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contactus.html')
def contactus():
    return render_template('contactus_new.html')

@app.route('/signup.html')
def signup():
    return render_template('signup_new.html')

# Service detail pages - require authentication
@app.route('/cloud_migration.html')
def cloud_migration():
    if not session.get('logged_in'):
        return redirect(url_for('signup'))
    return render_template('cloud_migration.html')

@app.route('/cloud_optimization.html')
def cloud_optimization():
    if not session.get('logged_in'):
        return redirect(url_for('signup'))
    return render_template('cloud_optimization.html')

@app.route('/cloud_security.html')
def cloud_security():
    if not session.get('logged_in'):
        return redirect(url_for('signup'))
    return render_template('cloud_security.html')

@app.route('/cloud_implementation.html')
def cloud_implementation():
    if not session.get('logged_in'):
        return redirect(url_for('signup'))
    return render_template('cloud_implementation.html')

@app.route('/cloud_consulting.html')
def cloud_consulting():
    if not session.get('logged_in'):
        return redirect(url_for('signup'))
    return render_template('cloud_consulting.html')

@app.route('/managed_services.html')
def managed_services():
    if not session.get('logged_in'):
        return redirect(url_for('signup'))
    return render_template('managed_services.html')

# API Endpoints
@app.route('/api/signup', methods=['POST'])
def api_signup():
    """Handle user registration"""
    try:
        data = request.json
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Validate input
        if not first_name or not last_name or not username or not email or not password:
            return jsonify({"error": "All fields are required."}), 400
            
        # Validate email format
        import re
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, email):
            return jsonify({"error": "Invalid email format."}), 400
            
        # Check password strength
        if len(password) < 6:
            return jsonify({"error": "Password must be at least 6 characters long."}), 400
            
        # Check if user already exists
        if email in users:
            return jsonify({"error": "Email is already registered."}), 400
        
        # Store user in memory
        users[email] = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'password': password  # In a real app, this would be hashed
        }
        
        # Set session
        session['logged_in'] = True
        session['email'] = email
        session['username'] = username
        
        return jsonify({"message": "Sign-up successful! Welcome to Tyledeclouds."}), 201
    except Exception as e:
        logger.error(f"Error in signup: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500

@app.route('/api/login', methods=['POST'])
def api_login():
    """Handle user login"""
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"error": "Email and password are required."}), 400
        
        # Check if user exists and password matches
        if email in users and users[email]['password'] == password:
            session['logged_in'] = True
            session['email'] = email
            session['username'] = users[email]['username']
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"error": "Invalid email or password."}), 401
    except Exception as e:
        logger.error(f"Error in login: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500

@app.route('/api/logout', methods=['POST'])
def api_logout():
    """Handle user logout API for AJAX requests"""
    session.clear()
    return jsonify({"message": "Logged out successfully."}), 200

@app.route('/logout.html')
@app.route('/logout')
def logout():
    """Display logout page and clear session"""
    # Clear the user session
    session.clear()
    return render_template('logout.html')

@app.route('/api/contact', methods=['POST'])
def api_contact():
    """Handle contact form submissions"""
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        
        if not name or not email or not message:
            return jsonify({"error": "All fields are required."}), 400
            
        # In a real app, this would save to the database
        # For now, just log the message
        logger.info(f"Contact message from {name} ({email}): {message}")
        
        return jsonify({"message": "Thank you for your message! We'll get back to you soon."}), 201
    except Exception as e:
        logger.error(f"Error in contact form: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500

@app.route('/api/user-status')
def api_user_status():
    """Check if user is logged in"""
    if session.get('logged_in'):
        return jsonify({
            "isLoggedIn": True,
            "username": session.get('username'),
            "email": session.get('email')
        })
    else:
        return jsonify({"isLoggedIn": False})

# Payment routes
@app.route('/payment.html')
@app.route('/payment')
def payment():
    """Display payment page with service options"""
    if not session.get('logged_in'):
        return redirect(url_for('signup'))
    
    return render_template('payment_new.html', 
                          stripe_key=stripe_publishable_key,
                          services=service_prices)

@app.route('/api/create-payment-intent', methods=['POST'])
def create_payment_intent():
    """Create a payment intent with Stripe"""
    try:
        if not session.get('logged_in'):
            return jsonify({"error": "Please log in to make a payment"}), 401
            
        data = request.json
        service_id = data.get('serviceId')
        
        if not service_id or service_id not in service_prices:
            return jsonify({"error": "Invalid service selected."}), 400
            
        service = service_prices[service_id]
        
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=service['price'],
            currency=service['currency'],
            description=service['description'],
            metadata={
                'service_id': service_id,
                'user_email': session.get('email')
            }
        )
        
        # Store payment intent in our temporary storage
        payment_id = intent.id
        payments[payment_id] = {
            'service': service_id,
            'user_email': session.get('email'),
            'amount': service['price'],
            'status': 'pending'
        }
        
        return jsonify({
            'clientSecret': intent.client_secret,
            'payment_id': payment_id
        })
    except Exception as e:
        logger.error(f"Error creating payment intent: {str(e)}")
        return jsonify({"error": "Payment processing failed. Please try again."}), 500

@app.route('/api/payment-success', methods=['POST'])
def payment_success():
    """Process successful payment"""
    try:
        data = request.json
        payment_id = data.get('paymentId')
        
        if not payment_id or payment_id not in payments:
            return jsonify({"error": "Invalid payment reference."}), 400
            
        # Update payment status
        payments[payment_id]['status'] = 'completed'
        logger.info(f"Payment {payment_id} completed successfully")
        
        return jsonify({
            "success": True,
            "message": "Thank you for your payment! Your service is now active."
        })
    except Exception as e:
        logger.error(f"Error processing payment success: {str(e)}")
        return jsonify({"error": "Failed to record payment. Please contact support."}), 500

@app.route('/payment-success.html')
@app.route('/payment-success')
def payment_success_page():
    """Display payment success page"""
    if not session.get('logged_in'):
        return redirect(url_for('signup'))
    
    return render_template('payment_success.html')
