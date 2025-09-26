# Lead Scraper API

A simple Django REST Framework API that wraps Instagram and TikTok scrapers to extract lead information from social media profiles.

## Features

- **Single URL Lead Scraping**: Extract lead data from individual Instagram and TikTok profile URLs
- **Structured Data**: Returns normalized lead data including bio, emails, and phone numbers
- **Retry Logic**: Built-in retry mechanism with exponential backoff using Tenacity
- **Proxy Support**: Configurable proxy support for reliable scraping
- **Simple Setup**: Easy Python setup with no Docker required
- **API Documentation**: Auto-generated OpenAPI documentation with Swagger UI

## Tech Stack

- **Python 3.11+**
- **Django 5.x**
- **Django REST Framework 3.15+**
- **Tenacity** for retry logic
- **Requests** for HTTP requests
- **Parsel** for HTML parsing
- **PhoneNumbers** for phone number validation

## Quick Start

### Simple Setup (Recommended)

1. **Navigate to the project:**
   ```bash
   cd "/Volumes/Programming/5_APIFY_ACTORS/LeadF/RapidAPI/Profile Scraper"
   ```

2. **Run the setup script:**
   ```bash
   ./run_local.sh
   ```
   
   Or manually:
   
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run migrations
   python manage.py migrate
   
   # Start server
   python manage.py runserver
   ```

3. **Access the API:**
   - API Base URL: http://localhost:8000/api/
   - Swagger Documentation: http://localhost:8000/api/docs/
   - ReDoc Documentation: http://localhost:8000/api/redoc/

## API Endpoints

### Instagram Profile Lead Scraper

**Endpoint:** `POST /api/instagram-profile-lead-scraper/`

**Request:**
```json
{
  "url": "https://www.instagram.com/username/"
}
```

**Response:**
```json
{
  "url": "https://www.instagram.com/username/",
  "bio": "Sample bio text with contact info",
  "emails": [
    {
      "email": "contact@example.com"
    }
  ],
  "phone": [
    {
      "number": "+1234567890",
      "type": "international"
    }
  ]
}
```

### TikTok Profile Lead Scraper

**Endpoint:** `POST /api/tiktok-profile-lead-scraper/`

**Request:**
```json
{
  "url": "https://www.tiktok.com/@username"
}
```

**Response:**
```json
{
  "url": "https://www.tiktok.com/@username/",
  "bio": "Sample bio text with contact info",
  "emails": [
    {
      "email": "contact@example.com"
    }
  ],
  "phone": [
    {
      "number": "+1234567890",
      "type": "international"
    }
  ]
}
```

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# API Configuration
API_KEY=your-api-key-here

# Scraper Configuration
SCRAPER_TIMEOUT=30
SCRAPER_RETRY_ATTEMPTS=3
SCRAPER_RETRY_WAIT=2

# Proxy Configuration
RESIDENTIAL_PROXY_URL=http://user:pass@proxy.example.com:8000
DATACENTER_PROXY_URL=http://user:pass@proxy.example.com:8001

# CORS Configuration
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Proxy Configuration

The API supports both residential and datacenter proxies:

- **Residential Proxy**: Used by default for more reliable scraping
- **Datacenter Proxy**: Fallback option
- **No Proxy**: Set proxy URLs to empty strings to disable

## Usage Examples

### Using cURL

**Instagram:**
```bash
curl -X POST http://localhost:8000/api/instagram-profile-lead-scraper/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.instagram.com/username/"}'
```

**TikTok:**
```bash
curl -X POST http://localhost:8000/api/tiktok-profile-lead-scraper/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.tiktok.com/@username"}'
```

### Using Python Requests

```python
import requests

# Instagram
response = requests.post(
    'http://localhost:8000/api/instagram-profile-lead-scraper/',
    json={'url': 'https://www.instagram.com/username/'}
)
lead_data = response.json()

# TikTok  
response = requests.post(
    'http://localhost:8000/api/tiktok-profile-lead-scraper/',
    json={'url': 'https://www.tiktok.com/@username'}
)
lead_data = response.json()
```

## Error Handling

The API returns structured error responses:

```json
{
  "error": "SCRAPER_ERROR",
  "message": "Failed to scrape profile: Invalid URL format",
  "details": {
    "platform": "Instagram"
  }
}
```

Common error types:
- `VALIDATION_ERROR`: Invalid request data
- `SCRAPER_ERROR`: Scraping-related errors
- `INTERNAL_ERROR`: Unexpected server errors

## Monitoring and Logs

- **Application logs**: Available in `lead_scraper.log`
- **Django logs**: Check the console output or log files
- **Health check**: Visit `/admin/` to verify the API is running

## Production Deployment

1. **Set production environment:**
   ```env
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
   ```

2. **Use production WSGI server:**
   ```bash
   pip install gunicorn
   gunicorn --bind 0.0.0.0:8000 --workers 4 lead_scraper_api.wsgi:application
   ```

3. **Set up reverse proxy** (Nginx recommended)

4. **Configure SSL/TLS** for HTTPS

## Development

### Project Structure

```
Profile Scraper/
├── api/                      # Django API project
│   ├── lead_scraper_api/     # Django project settings
│   ├── scrapers/             # Main app with scraping logic
│   │   ├── services.py       # Scraper services with retry logic
│   │   ├── views.py          # DRF API views
│   │   ├── serializers.py    # Request/response serializers
│   │   └── urls.py           # App URL configuration
│   └── manage.py             # Django management script
├── requirements.txt          # Python dependencies
├── run_local.sh             # Simple startup script
├── quick_test.py            # Test script
└── .env                     # Environment configuration
```

### Adding New Scrapers

1. Create a new service class in `api/scrapers/services.py`
2. Add corresponding serializers in `api/scrapers/serializers.py`
3. Create API view in `api/scrapers/views.py`
4. Add URL pattern in `api/scrapers/urls.py`

### Manual Commands

If you need to run Django commands manually:

```bash
cd api
python manage.py migrate
python manage.py runserver
python manage.py createsuperuser
python manage.py test_scrapers --instagram username
```

## License

This project is for internal use. Please ensure compliance with platform terms of service when scraping.

## Support

For issues and questions, please check the API documentation at `/api/docs/` or review the application logs.
