#!/bin/bash

# Coolify startup script for Django Lead Fiesta Profile API

echo "🚀 Starting Lead Fiesta Profile API..."

# Run database migrations
echo "📊 Running database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Start the application with Gunicorn
echo "🎯 Starting Gunicorn server..."
exec gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 --access-logfile - --error-logfile - lead_scraper_api.wsgi:application
