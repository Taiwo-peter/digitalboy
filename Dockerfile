
FROM python:3.11-slim

WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY main.py .
COPY app.py .
COPY routes.py .
COPY models.py .
COPY templates/ ./templates/
COPY static/ ./static/

# Install Python dependencies
RUN pip install --no-cache-dir gunicorn flask flask-sqlalchemy flask-login werkzeug psycopg2-binary sqlalchemy email-validator flask-wtf python-dotenv

# Environment variables (will be overridden by docker-compose)
ENV PYTHONUNBUFFERED=1
ENV SESSION_SECRET=tyledeclouds_default_secret
ENV DATABASE_URL=sqlite:///instance/tyledeclouds.db

# Create instance directory for SQLite
RUN mkdir -p instance

# Expose port
EXPOSE 5000

# Start the application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "main:app"]
