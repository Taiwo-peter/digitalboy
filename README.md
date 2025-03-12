
# Tyledeclouds - Cloud Consulting Services

A Flask-based web application providing information and services for cloud consulting.

## Project Overview

Tyledeclouds is a web application for a cloud consulting company that offers various cloud-related services including cloud migration, optimization, security, implementation, consulting, and managed services. The application includes user authentication, contact form submission, and detailed service pages.

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy with SQLite (development) / configurable for production
- **Authentication**: Flask-Login with password hashing (Werkzeug)
- **Frontend**: HTML, CSS, JavaScript

## Project Structure

- `app.py`: Main Flask application configuration
- `main.py`: Entry point for running the application
- `models.py`: Database models (User, ContactMessage)
- `routes.py`: All route definitions and API endpoints
- `templates/`: HTML templates for all pages
- `static/`: Static assets (CSS, JavaScript, images)

## Features

### Core Features

- User authentication (signup, login, logout)
- Detailed service pages with descriptions
- Contact form submission
- Responsive design

### Cloud Services Offered

1. **Cloud Migration**: Services to help businesses move to the cloud
2. **Cloud Optimization**: Performance tuning and cost optimization
3. **Cloud Security**: Comprehensive security solutions
4. **Cloud Implementation**: Technical deployment and integration
5. **Cloud Consulting**: Strategic guidance and planning
6. **Managed Services**: Ongoing cloud operations and maintenance

## Setup and Installation

### Prerequisites

- Python 3.6+
- pip package manager

### Local Development Setup

1. Clone the repository:
```
git clone https://github.com/yourusername/tyledeclouds.git
cd tyledeclouds
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
python main.py
```

4. Access the application at `http://0.0.0.0:5000`

### Environment Variables

The application uses the following environment variables:

- `SESSION_SECRET`: Secret key for session management (default: "tyledeclouds_default_secret")
- `DATABASE_URL`: Database connection string (default: "sqlite:///tyledeclouds.db")

## Database Models

### User Model

Stores user information for authentication:

- `id`: Primary key
- `email`: User's email (unique)
- `password_hash`: Hashed password
- `created_at`: Timestamp of user creation

### ContactMessage Model

Stores contact form submissions:

- `id`: Primary key
- `name`: Contact name
- `email`: Contact email
- `message`: Message content
- `created_at`: Timestamp of message submission

## API Endpoints

### Authentication

- `POST /api/signup`: User registration
- `POST /api/login`: User login
- `GET /api/logout`: User logout
- `GET /api/user/status`: Check user login status

### Contact

- `POST /api/contact`: Submit contact form

## Page Routes

- `/`: Index page
- `/home.html`: Home page
- `/services.html`: Services overview
- `/aboutus.html`: About us page
- `/contactus.html`: Contact form
- `/signup.html`: Signup/login page

### Service Detail Pages (Login Required)

- `/cloud_migration.html`: Cloud migration services
- `/cloud_optimization.html`: Cloud optimization services
- `/cloud_security.html`: Cloud security services
- `/cloud_implementation.html`: Cloud implementation services 
- `/cloud_consulting.html`: Cloud consulting services
- `/managed_services.html`: Managed cloud services

## Deployment

This application is configured to run on Replit. The service is already configured with Gunicorn for production use.

To deploy on Replit:

1. Use the Deployment tool in the Replit UI
2. Configure the deployment with the appropriate settings:
   - Build command: (leave empty)
   - Run command: `gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app`

## Security

- All passwords are hashed using Werkzeug's security functions
- Session management with secret key
- Login required for accessing detailed service pages

## License

[Your License Here]

## Contact

[Your Contact Information]
