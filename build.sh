#!/bin/bash
# Build script for Render deployment

# Update pip to latest version
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate --noinput
