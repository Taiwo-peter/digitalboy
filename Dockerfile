
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY main.py .
COPY app.py .
COPY routes.py .
COPY models.py .
COPY templates/ ./templates/
COPY static/ ./static/

RUN pip install --no-cache-dir gunicorn flask flask-sqlalchemy flask-login werkzeug psycopg2-binary sqlalchemy email-validator

ENV PYTHONUNBUFFERED=1
ENV SESSION_SECRET=tyledeclouds_default_secret
ENV DATABASE_URL=sqlite:///tyledeclouds.db

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "main:app"]
