# Use the official Python image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (if needed)
ENV SESSION_SECRET="tyledeclouds_default_secret"
ENV DATABASE_URL="sqlite:///tyledeclouds.db"

# Expose the port Flask runs on
EXPOSE 5000

# Run the table creation script and then start the Flask app with Gunicorn
CMD /bin/bash -c "python init_db.py && gunicorn --bind 0.0.0.0:5000 main:app"
