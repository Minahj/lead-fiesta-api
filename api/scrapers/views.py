"""
DRF views for Instagram and TikTok profile scraping endpoints.
"""
import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import (
    InstagramProfileURLSerializer,
    TikTokProfileURLSerializer,
    LeadDataSerializer,
    ErrorSerializer
)
from .services import InstagramScraperService, TikTokScraperService, ScraperError

logger = logging.getLogger('scrapers')


class BaseScraperView(APIView):
    """Base view for scraper endpoints"""
    permission_classes = [AllowAny]  # Remove authentication for now
    
    def handle_scraper_error(self, error, platform):
        """Handle scraper errors and return appropriate response"""
        logger.error(f"{platform} scraper error: {error}")
        
        if isinstance(error, ScraperError):
            return Response(
                {
                    "error": "SCRAPER_ERROR",
                    "message": str(error),
                    "details": {"platform": platform}
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            return Response(
                {
                    "error": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred",
                    "details": {"platform": platform}
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class InstagramProfileLeadScraperView(BaseScraperView):
    """
    API endpoint for scraping Instagram profile lead data.
    
    Accepts a single Instagram profile URL and returns structured lead data
    including bio, emails, and phone numbers.
    """
    
    @extend_schema(
        request=InstagramProfileURLSerializer,
        responses={
            200: OpenApiResponse(
                response=LeadDataSerializer,
                description="Successfully scraped Instagram profile"
            ),
            400: OpenApiResponse(
                response=ErrorSerializer,
                description="Invalid request or scraping error"
            ),
            500: OpenApiResponse(
                response=ErrorSerializer,
                description="Internal server error"
            )
        },
        summary="Scrape Instagram Profile",
        description="Scrape an Instagram profile and extract lead information including bio, emails, and phone numbers.",
        tags=["Profile Scrapers"]
    )
    def post(self, request):
        """
        Scrape Instagram profile for lead data
        
        Args:
            request: HTTP request with JSON body containing 'url' field
            
        Returns:
            JSON response with lead data or error message
        """
        # Validate input
        serializer = InstagramProfileURLSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Invalid Instagram URL request: {serializer.errors}")
            return Response(
                {
                    "error": "VALIDATION_ERROR",
                    "message": "Invalid request data",
                    "details": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        url = serializer.validated_data['url']
        logger.info(f"Processing Instagram scrape request for URL: {url}")
        
        try:
            # Initialize scraper service
            scraper = InstagramScraperService()
            
            # Scrape profile
            lead_data = scraper.scrape_profile(url)
            
            # Serialize response
            response_serializer = LeadDataSerializer(lead_data)
            
            logger.info(f"Successfully processed Instagram scrape request for URL: {url}")
            return Response(response_serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return self.handle_scraper_error(e, "Instagram")


class TikTokProfileLeadScraperView(BaseScraperView):
    """
    API endpoint for scraping TikTok profile lead data.
    
    Accepts a single TikTok profile URL and returns structured lead data
    including bio, emails, and phone numbers.
    """
    
    @extend_schema(
        request=TikTokProfileURLSerializer,
        responses={
            200: OpenApiResponse(
                response=LeadDataSerializer,
                description="Successfully scraped TikTok profile"
            ),
            400: OpenApiResponse(
                response=ErrorSerializer,
                description="Invalid request or scraping error"
            ),
            500: OpenApiResponse(
                response=ErrorSerializer,
                description="Internal server error"
            )
        },
        summary="Scrape TikTok Profile",
        description="Scrape a TikTok profile and extract lead information including bio, emails, and phone numbers.",
        tags=["Profile Scrapers"]
    )
    def post(self, request):
        """
        Scrape TikTok profile for lead data
        
        Args:
            request: HTTP request with JSON body containing 'url' field
            
        Returns:
            JSON response with lead data or error message
        """
        # Validate input
        serializer = TikTokProfileURLSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Invalid TikTok URL request: {serializer.errors}")
            return Response(
                {
                    "error": "VALIDATION_ERROR",
                    "message": "Invalid request data",
                    "details": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        url = serializer.validated_data['url']
        logger.info(f"Processing TikTok scrape request for URL: {url}")
        
        try:
            # Initialize scraper service
            scraper = TikTokScraperService()
            
            # Scrape profile
            lead_data = scraper.scrape_profile(url)
            
            # Serialize response
            response_serializer = LeadDataSerializer(lead_data)
            
            logger.info(f"Successfully processed TikTok scrape request for URL: {url}")
            return Response(response_serializer.data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return self.handle_scraper_error(e, "TikTok")
