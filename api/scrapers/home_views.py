"""
Home page views for the Lead Fiesta Profile API.
"""
from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    Home page view with the beautiful landing page.
    """
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'page_title': 'Lead Fiesta Profile API',
            'description': 'Extract valuable lead information from Instagram and TikTok profiles instantly',
            'features': [
                {
                    'icon': 'fas fa-envelope',
                    'title': 'Email Extraction',
                    'description': 'Automatically extract email addresses from profile bios with advanced regex patterns.'
                },
                {
                    'icon': 'fas fa-phone',
                    'title': 'Phone Detection', 
                    'description': 'Smart phone number detection with international format recognition and validation.'
                },
                {
                    'icon': 'fas fa-shield-alt',
                    'title': 'Retry Logic',
                    'description': 'Built-in retry mechanisms with exponential backoff for reliable data extraction.'
                }
            ]
        })
        return context
