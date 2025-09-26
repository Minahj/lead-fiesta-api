"""
URL configuration for lead_scraper_api project.
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from scrapers.home_views import HomeView

urlpatterns = [
    # Homepage
    path('', HomeView.as_view(), name='home'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/', include('scrapers.urls')),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
