"""
Serializers for request/response validation in the lead scraper API.
"""
from rest_framework import serializers
from urllib.parse import urlparse


class ProfileURLSerializer(serializers.Serializer):
    """Serializer for profile URL input"""
    url = serializers.CharField(required=True, help_text="Profile URL or username to scrape")
    
    def validate_url(self, value):
        """Validate that the URL is a valid profile URL or username"""
        # Allow both full URLs and usernames
        if not value or not value.strip():
            raise serializers.ValidationError("URL or username cannot be empty")
        return value.strip()


class InstagramProfileURLSerializer(ProfileURLSerializer):
    """Serializer for Instagram profile URL input"""
    
    def validate_url(self, value):
        """Validate that the URL is an Instagram URL or username"""
        value = super().validate_url(value)
        # Accept Instagram URLs, usernames with @, and plain usernames
        return value


class TikTokProfileURLSerializer(ProfileURLSerializer):
    """Serializer for TikTok profile URL input"""
    
    def validate_url(self, value):
        """Validate that the URL is a TikTok URL or username"""
        value = super().validate_url(value)
        # Accept TikTok URLs, usernames with @, and plain usernames
        return value


class EmailSerializer(serializers.Serializer):
    """Serializer for email data"""
    email = serializers.EmailField()


class PhoneSerializer(serializers.Serializer):
    """Serializer for phone number data"""
    number = serializers.CharField(max_length=20)
    type = serializers.CharField(max_length=50)


class LeadDataSerializer(serializers.Serializer):
    """Serializer for lead data response"""
    url = serializers.URLField(read_only=True)
    bio = serializers.CharField(read_only=True, allow_blank=True)
    emails = EmailSerializer(many=True, read_only=True)
    phone = PhoneSerializer(many=True, read_only=True)


class ErrorSerializer(serializers.Serializer):
    """Serializer for error responses"""
    error = serializers.CharField(read_only=True)
    message = serializers.CharField(read_only=True)
    details = serializers.DictField(read_only=True, required=False)
