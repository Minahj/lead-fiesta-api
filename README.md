# 🎯 Lead Fiesta Profile API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-5.x-green?style=for-the-badge&logo=django)
![DRF](https://img.shields.io/badge/DRF-3.15+-red?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Extract valuable lead information from Instagram and TikTok profiles instantly**

[🚀 Live Demo](http://localhost:8000) • [📖 Documentation](http://localhost:8000/api/docs/) • [🐛 Report Bug](https://github.com/Minahj/lead-fiesta-profile-api/issues)

</div>

## ✨ Features

- 🎨 **Beautiful Landing Page** - Interactive web interface with real-time testing
- 📱 **Instagram & TikTok** - Support for both major social platforms  
- 📧 **Email Extraction** - Advanced regex patterns for email detection
- 📞 **Phone Detection** - Smart international phone number recognition
- 🔄 **Retry Logic** - Exponential backoff for reliable scraping
- 📚 **API Documentation** - Auto-generated OpenAPI/Swagger docs
- 🐳 **Production Ready** - Complete with environment configuration

## 🚀 Quick Start

**One command setup:**
```bash
./run_local.sh
```

This will automatically:
- Create virtual environment
- Install dependencies  
- Run database migrations
- Start the API server at http://localhost:8000

## Project Structure

```
Profile Scraper/
├── api/                    # 🎯 Django REST API
│   ├── .env               # Environment configuration
│   ├── .gitignore         # Git ignore rules
│   ├── README.md          # Detailed API documentation
│   ├── requirements.txt   # Python dependencies
│   ├── manage.py          # Django management
│   ├── lead_scraper_api/  # Django project settings
│   └── scrapers/          # API endpoints & scraper logic
├── ig-lead-scraper.py     # Original Instagram scraper
├── tiktok-lead-scraper.py # Original TikTok scraper
├── proxy.py               # Proxy configuration
├── quick_test.py          # Test API setup
├── run_local.sh          # One-click startup script
└── venv/                 # Virtual environment
```

## API Endpoints

Once running, visit:
- **API Documentation**: http://localhost:8000/api/docs/
- **Instagram Scraper**: `POST /api/instagram-profile-lead-scraper/`
- **TikTok Scraper**: `POST /api/tiktok-profile-lead-scraper/`

## Usage

**Test Instagram:**
```bash
curl -X POST http://localhost:8000/api/instagram-profile-lead-scraper/ \
  -H "Content-Type: application/json" \
  -d '{"url": "username"}'
```

**Test TikTok:**
```bash
curl -X POST http://localhost:8000/api/tiktok-profile-lead-scraper/ \
  -H "Content-Type: application/json" \
  -d '{"url": "username"}'
```

## 📸 Screenshots

### Beautiful Landing Page
![Landing Page](https://via.placeholder.com/800x400/667eea/ffffff?text=Beautiful+Landing+Page+with+Real-time+API+Testing)

### API Documentation
![API Docs](https://via.placeholder.com/800x400/764ba2/ffffff?text=Interactive+OpenAPI+Documentation)

## 🛠️ Installation

### Prerequisites
- Python 3.11+
- Git

### Manual Setup
```bash
# Clone the repository
git clone https://github.com/Minahj/lead-fiesta-profile-api.git
cd lead-fiesta-profile-api

# Run the setup script
./run_local.sh
```

### Environment Configuration
Copy the environment file and update with your settings:
```bash
cp api/.env.example api/.env
# Edit api/.env with your proxy credentials and configuration
```

## 🔧 Configuration

Key environment variables in `api/.env`:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Scraper Configuration  
SCRAPER_TIMEOUT=30
SCRAPER_RETRY_ATTEMPTS=3
SCRAPER_RETRY_WAIT=2

# Proxy Settings (Optional)
RESIDENTIAL_PROXY_URL=your-proxy-url
DATACENTER_PROXY_URL=your-proxy-url
```

## 🚀 Deployment

### Production Setup
1. Set `DEBUG=False` in `api/.env`
2. Configure `ALLOWED_HOSTS` with your domain
3. Use a production WSGI server like Gunicorn:

```bash
cd api
gunicorn --bind 0.0.0.0:8000 --workers 4 lead_scraper_api.wsgi:application
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and legitimate business purposes only. Please ensure compliance with Instagram and TikTok's Terms of Service and applicable laws in your jurisdiction.

## 📞 Support

- 📖 [Documentation](http://localhost:8000/api/docs/)
- 🐛 [Report Issues](https://github.com/Minahj/lead-fiesta-profile-api/issues)
- 💬 [Discussions](https://github.com/Minahj/lead-fiesta-profile-api/discussions)

---

<div align="center">
Made with ❤️ by <a href="https://github.com/Minahj">Minahj</a>
</div>
