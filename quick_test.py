#!/usr/bin/env python
"""
Quick test script to verify the API setup works without Docker.
"""
import os
import sys

# Navigate to the api directory
api_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api')
os.chdir(api_dir)
sys.path.insert(0, api_dir)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lead_scraper_api.settings')

try:
    import django
    django.setup()
    
    print("✅ Django setup successful!")
    
    # Test imports
    from scrapers.services import InstagramScraperService, TikTokScraperService
    print("✅ Scraper services imported successfully!")
    
    from scrapers.views import InstagramProfileLeadScraperView, TikTokProfileLeadScraperView
    print("✅ API views imported successfully!")
    
    from scrapers.serializers import InstagramProfileURLSerializer, TikTokProfileURLSerializer
    print("✅ Serializers imported successfully!")
    
    print("\n🎉 All components loaded successfully!")
    print("\nTo start the API server, run:")
    print("./run_local.sh")
    print("\nOr manually:")
    print("cd api && python manage.py runserver")
    print("\nThen visit:")
    print("- API Docs: http://localhost:8000/api/docs/")
    print("- Instagram endpoint: http://localhost:8000/api/instagram-profile-lead-scraper/")
    print("- TikTok endpoint: http://localhost:8000/api/tiktok-profile-lead-scraper/")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure to install dependencies with: pip install -r requirements.txt")
except Exception as e:
    print(f"❌ Setup error: {e}")
    print("Check your .env file configuration")
