"""
Service modules that wrap the existing scrapers with retry logic and error handling.
"""
import logging
import requests
import json
import re
from typing import Optional, List, Dict, Any
from urllib.parse import urlparse
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from django.conf import settings
import phonenumbers
from phonenumbers import PhoneNumberMatcher
from parsel import Selector

logger = logging.getLogger('scrapers')


class ScraperError(Exception):
    """Custom exception for scraper errors"""
    pass


class ProxyService:
    """Service for managing proxy configurations"""
    
    @staticmethod
    def get_residential_proxy_config():
        """Get residential proxy configuration"""
        proxy_url = getattr(settings, 'RESIDENTIAL_PROXY_URL', '')
        if proxy_url:
            return {
                "http": proxy_url,
                "https": proxy_url
            }
        return None
    
    @staticmethod
    def get_datacenter_proxy_config():
        """Get datacenter proxy configuration"""
        proxy_url = getattr(settings, 'DATACENTER_PROXY_URL', '')
        if proxy_url:
            return {
                "http": proxy_url,
                "https": proxy_url
            }
        return None


class ContactExtractor:
    """Service for extracting contact information from text"""
    
    @staticmethod
    def extract_emails(text: Optional[str]) -> List[str]:
        """Extract all emails from text using regex"""
        if not text:
            return []
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text)
        return emails

    @staticmethod
    def extract_phone_numbers_smart(text: Optional[str], priority_regions: List[str] = None) -> List[str]:
        """
        Smart phone number extraction that automatically tries multiple regions.
        
        Strategy:
        1. First try international format parsing (no region needed)
        2. If no valid numbers found, try region-specific parsing with priority regions
        3. Stop at first valid match for each potential number
        4. Return numbers in their original format (don't add international codes)
        
        Args:
            text: Text to extract phone numbers from
            priority_regions: List of regions to try in order (default: common regions)
        
        Returns:
            List of phone numbers in their original format
        """
        if not text:
            return []
        
        if priority_regions is None:
            # Common regions to try, ordered by likelihood
            priority_regions = ["GB", "US", "IN", "BR", "MX", "AU", "CA", "DE", "FR"]
        
        phone_numbers = []
        found_numbers = set()  # To avoid duplicates
        
        # Step 1: Try international format parsing (no region needed)
        try:
            for match in PhoneNumberMatcher(text, None):  # None = international format
                if phonenumbers.is_valid_number(match.number):
                    # Return the original text as found
                    original_number = text[match.start:match.end]
                    if original_number not in found_numbers:
                        phone_numbers.append(original_number)
                        found_numbers.add(original_number)
        except phonenumbers.NumberParseException:
            pass
        
        # Step 2: Try region-specific parsing for national numbers
        for region in priority_regions:
            try:
                for match in PhoneNumberMatcher(text, region):
                    if phonenumbers.is_valid_number(match.number):
                        # Return the original text as found
                        original_number = text[match.start:match.end]
                        if original_number not in found_numbers:
                            phone_numbers.append(original_number)
                            found_numbers.add(original_number)
            except phonenumbers.NumberParseException:
                continue
        
        return phone_numbers

    @staticmethod
    def get_phone_type(phone_number: str) -> str:
        """
        Determine if phone number is international or get likely country code.
        
        Args:
            phone_number: The phone number to analyze
        
        Returns:
            "international" if has country code, otherwise "Likely [COUNTRY_CODE]"
        """
        if phone_number.startswith('+'):
            return "international"
        
        # Try to detect country from the number format
        try:
            for region in ["US", "IN", "BD", "GB", "AU", "CA", "DE", "FR", "BR", "MX"]:
                try:
                    parsed_number = phonenumbers.parse(phone_number, region)
                    if phonenumbers.is_valid_number(parsed_number):
                        return f"Likely {region}"
                except phonenumbers.NumberParseException:
                    continue
        except:
            pass
        
        # If no country detected, return "unknown"
        return "unknown"


class InstagramScraperService:
    """Service for scraping Instagram profiles"""
    
    def __init__(self):
        self.timeout = getattr(settings, 'SCRAPER_TIMEOUT', 30)
        self.retry_attempts = getattr(settings, 'SCRAPER_RETRY_ATTEMPTS', 3)
        self.retry_wait = getattr(settings, 'SCRAPER_RETRY_WAIT', 2)
        self.contact_extractor = ContactExtractor()
        self.proxy_service = ProxyService()
    
    def extract_username_from_url(self, url: str) -> str:
        """Extract username from Instagram URL"""
        try:
            # Handle various Instagram URL formats
            if 'instagram.com/' in url:
                # Remove trailing slash and split
                clean_url = url.rstrip('/')
                parts = clean_url.split('/')
                
                # Find the username part
                for i, part in enumerate(parts):
                    if part == 'instagram.com' and i + 1 < len(parts):
                        username = parts[i + 1]
                        # Remove @ if present
                        return username.lstrip('@')
                
                # If direct format like instagram.com/username
                if parts[-1] and parts[-1] != 'instagram.com':
                    return parts[-1].lstrip('@')
            
            # If it's just a username
            return url.lstrip('@')
            
        except Exception as e:
            logger.error(f"Error extracting username from URL {url}: {e}")
            raise ScraperError(f"Invalid Instagram URL format: {url}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((requests.RequestException, json.JSONDecodeError))
    )
    def _fetch_profile_bio(self, username: str) -> str:
        """Fetch Instagram profile biography with retry logic"""
        proxy_config = self.proxy_service.get_residential_proxy_config()
        
        url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={username}"
        headers = {
            "x-ig-app-id": "936619743392459",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
        }
        
        logger.info(f"Fetching Instagram profile for username: {username}")
        
        try:
            response = requests.get(
                url, 
                headers=headers, 
                proxies=proxy_config,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            bio = data.get("data", {}).get("user", {}).get("biography", "")
            
            logger.info(f"Successfully fetched bio for {username}")
            return bio
            
        except requests.RequestException as e:
            logger.error(f"Request error for Instagram profile {username}: {e}")
            raise
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"JSON parsing error for Instagram profile {username}: {e}")
            raise
    
    def scrape_profile(self, url: str) -> Dict[str, Any]:
        """
        Scrape Instagram profile and return normalized lead data
        
        Args:
            url: Instagram profile URL or username
            
        Returns:
            Dictionary with normalized lead data
        """
        try:
            username = self.extract_username_from_url(url)
            bio = self._fetch_profile_bio(username)
            
            # Extract contact information
            emails = self.contact_extractor.extract_emails(bio)
            phone_numbers = self.contact_extractor.extract_phone_numbers_smart(bio)
            
            # Format the response
            profile_url = f"https://www.instagram.com/{username}/"
            
            # Handle multiple emails
            email_list = [{"email": email} for email in emails]
            
            # Handle multiple phone numbers
            phone_list = []
            for phone_number in phone_numbers:
                phone_type = self.contact_extractor.get_phone_type(phone_number)
                phone_list.append({
                    "number": phone_number,
                    "type": phone_type
                })
            
            result = {
                "url": profile_url,
                "bio": bio,
                "emails": email_list,
                "phone": phone_list
            }
            
            logger.info(f"Successfully scraped Instagram profile: {username}")
            return result
            
        except Exception as e:
            logger.error(f"Error scraping Instagram profile {url}: {e}")
            raise ScraperError(f"Failed to scrape Instagram profile: {str(e)}")


class TikTokScraperService:
    """Service for scraping TikTok profiles"""
    
    def __init__(self):
        self.timeout = getattr(settings, 'SCRAPER_TIMEOUT', 30)
        self.retry_attempts = getattr(settings, 'SCRAPER_RETRY_ATTEMPTS', 3)
        self.retry_wait = getattr(settings, 'SCRAPER_RETRY_WAIT', 2)
        self.contact_extractor = ContactExtractor()
        self.proxy_service = ProxyService()
    
    def extract_username_from_url(self, url: str) -> str:
        """Extract username from TikTok URL"""
        try:
            # Handle various TikTok URL formats
            if 'tiktok.com/' in url:
                # Remove trailing slash and split
                clean_url = url.rstrip('/')
                parts = clean_url.split('/')
                
                # Find the username part (usually starts with @)
                for part in parts:
                    if part.startswith('@'):
                        return part[1:]  # Remove @ symbol
                
                # If direct format like tiktok.com/@username
                if parts[-1] and parts[-1].startswith('@'):
                    return parts[-1][1:]
            
            # If it's just a username
            return url.lstrip('@')
            
        except Exception as e:
            logger.error(f"Error extracting username from URL {url}: {e}")
            raise ScraperError(f"Invalid TikTok URL format: {url}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((requests.RequestException, json.JSONDecodeError))
    )
    def _fetch_profile_bio(self, username: str) -> str:
        """Fetch TikTok profile biography with retry logic"""
        proxy_config = self.proxy_service.get_residential_proxy_config()
        
        url = f"https://www.tiktok.com/@{username}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "identity",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        
        logger.info(f"Fetching TikTok profile for username: {username}")
        
        try:
            response = requests.get(
                url, 
                headers=headers, 
                proxies=proxy_config,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            selector = Selector(text=response.text)
            script_text = selector.css(
                'script[id="__UNIVERSAL_DATA_FOR_REHYDRATION__"]::text'
            ).get()
            
            if script_text:
                data = json.loads(script_text)
                user_info = data["__DEFAULT_SCOPE__"]["webapp.user-detail"]["userInfo"]["user"]
                bio = user_info.get("signature", "")
                
                logger.info(f"Successfully fetched bio for {username}")
                return bio
            else:
                logger.warning(f"No script data found for TikTok profile {username}")
                return ""
                
        except requests.RequestException as e:
            logger.error(f"Request error for TikTok profile {username}: {e}")
            raise
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"JSON parsing error for TikTok profile {username}: {e}")
            raise
    
    def scrape_profile(self, url: str) -> Dict[str, Any]:
        """
        Scrape TikTok profile and return normalized lead data
        
        Args:
            url: TikTok profile URL or username
            
        Returns:
            Dictionary with normalized lead data
        """
        try:
            username = self.extract_username_from_url(url)
            bio = self._fetch_profile_bio(username)
            
            # Extract contact information
            emails = self.contact_extractor.extract_emails(bio)
            phone_numbers = self.contact_extractor.extract_phone_numbers_smart(bio)
            
            # Format the response
            profile_url = f"https://www.tiktok.com/@{username}/"
            
            # Handle multiple emails
            email_list = [{"email": email} for email in emails]
            
            # Handle multiple phone numbers
            phone_list = []
            for phone_number in phone_numbers:
                phone_type = self.contact_extractor.get_phone_type(phone_number)
                phone_list.append({
                    "number": phone_number,
                    "type": phone_type
                })
            
            result = {
                "url": profile_url,
                "bio": bio,
                "emails": email_list,
                "phone": phone_list
            }
            
            logger.info(f"Successfully scraped TikTok profile: {username}")
            return result
            
        except Exception as e:
            logger.error(f"Error scraping TikTok profile {url}: {e}")
            raise ScraperError(f"Failed to scrape TikTok profile: {str(e)}")
