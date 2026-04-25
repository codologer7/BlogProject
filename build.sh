#!/bin/bash
# Build script for Render deployment

# Update pip and install build tools
pip install --no-cache-dir --upgrade pip setuptools wheel

# Install requirements with no cache
pip install --no-cache-dir -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input --clear

# Run migrations
python manage.py migrate --noinput

