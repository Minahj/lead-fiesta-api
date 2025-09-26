#!/bin/bash

# Local development startup script

echo "Setting up Lead Scraper API for local development..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Navigate to API directory
cd api

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from example..."
    cat > .env << EOF
# Django Configuration
SECRET_KEY=django-insecure-development-key-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# API Configuration
API_KEY=dev-api-key

# Scraper Configuration
SCRAPER_TIMEOUT=30
SCRAPER_RETRY_ATTEMPTS=3
SCRAPER_RETRY_WAIT=2

# Proxy Configuration (update with your proxy credentials)
RESIDENTIAL_PROXY_URL=
DATACENTER_PROXY_URL=

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
EOF
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser if needed (optional)
echo "To create a superuser, run: cd api && python manage.py createsuperuser"

# Start development server
echo "Starting development server on http://localhost:8000"
echo ""
echo "Available endpoints:"
echo "  - API Base: http://localhost:8000/api/"
echo "  - Instagram Scraper: http://localhost:8000/api/instagram-profile-lead-scraper/"
echo "  - TikTok Scraper: http://localhost:8000/api/tiktok-profile-lead-scraper/"
echo "  - API Documentation: http://localhost:8000/api/docs/"
echo "  - Admin Panel: http://localhost:8000/admin/"
echo ""

python manage.py runserver
