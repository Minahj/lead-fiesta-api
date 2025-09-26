from django.urls import path
from . import views

urlpatterns = [
    path('instagram-profile-lead-scraper/', views.InstagramProfileLeadScraperView.as_view(), name='instagram-scraper'),
    path('tiktok-profile-lead-scraper/', views.TikTokProfileLeadScraperView.as_view(), name='tiktok-scraper'),
]
