import requests
from parsel import Selector
from proxy import res_proxy, datacenter_proxy
import json
import re
from typing import Optional, List
import phonenumbers
from phonenumbers import PhoneNumberMatcher

res_proxy = res_proxy()
datacenter_proxy = datacenter_proxy()

def scrape_instagram_profile(handle, proxy=res_proxy):
    url = f"https://i.instagram.com/api/v1/users/web_profile_info/?username={handle}"
    headers = {
        "x-ig-app-id": "936619743392459",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    } 
    response = requests.get(url, headers=headers, proxies=proxy)
    data = response.json()
    return data["data"]["user"]["biography"]

def extract_emails(text: Optional[str]) -> List[str]:
    """Extract all emails from text using regex"""
    if not text:
        return []
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'  # Corrected regex string
    emails = re.findall(email_pattern, text)
    return emails

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
        priority_regions = ["GB", "US", "IN", "BR", "MX", "AF", "AL", "DZ", "AD", "AO", "AG", "AR", "AM", "AU", "AT", "AZ", "BS", "BH", "BD", "BB", "BY", "BE", "BZ", "BJ", "BT", "BO", "BA", "BW", "BN", "BG", "BF", "BI", "KH", "CM", "CA", "CV", "CF", "TD", "CL", "CN", "CO", "KM", "CD", "CG", "CR", "HR", "CU", "CY", "CZ", "DK", "DJ", "DM", "DO", "TL", "EC", "EG", "SV", "GQ", "ER", "EE", "SZ", "ET", "FJ", "FI", "FR", "GA", "GM", "GE", "DE", "GH", "GR", "GD", "GT", "GN", "GW", "GY", "HT", "HN", "HU", "IS", "ID", "IR", "IQ", "IE", "IL", "IT", "JM", "JP", "JO", "KZ", "KE", "KI", "KP", "KR", "KW", "KG", "LA", "LV", "LB", "LS", "LR", "LY", "LI", "LT", "LU", "MG", "MW", "MY", "MV", "ML", "MT", "MH", "MR", "MU", "FM", "MD", "MC", "MN", "ME", "MA", "MZ", "MM", "NA", "NR", "NP", "NL", "NZ", "NI", "NE", "NG", "MK", "NO", "OM", "PK", "PW", "PA", "PG", "PY", "PE", "PH", "PL", "PT", "QA", "RO", "RU", "RW", "KN", "LC", "VC", "WS", "SM", "ST", "SA", "SN", "RS", "SC", "SL", "SG", "SK", "SI", "SB", "SO", "ZA", "SS", "ES", "LK", "SD", "SR", "SE", "CH", "SY", "TW", "TJ", "TZ", "TH", "TG", "TO", "TT", "TN", "TR", "TM", "TV", "UG", "UA", "AE", "UY", "UZ", "VU", "VA", "VE", "VN", "YE", "ZM", "ZW"]
    
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

def save_profile_data(username: str, bio: str, emails: List[str], phone_numbers: List[str]) -> dict:
    """
    Save profile data in the specified format.
    
    Args:
        username: Instagram username
        bio: Biography text
        emails: List of extracted emails
        phone_numbers: List of extracted phone numbers
    
    Returns:
        Dictionary in the specified format
    """
    url = f"https://www.instagram.com/{username}/"
    
    # Handle multiple emails
    email_list = []
    for email in emails:
        email_list.append({
            "email": email
        })
    
    # Handle multiple phone numbers
    phone_list = []
    for phone_number in phone_numbers:
        phone_type = get_phone_type(phone_number)
        phone_list.append({
            "number": phone_number,
            "type": phone_type
        })
    
    return {
        "url": url,
        "bio": bio,
        "emails": email_list,
        "phone": phone_list
    }


# Example usage:
# data = scrape_instagram_profile("mehta0403")
handle = "mehta0403"
data = scrape_instagram_profile(handle)
emails = extract_emails(data)
phone_numbers = extract_phone_numbers_smart(data)

# Save in the specified format
profile_data = save_profile_data(handle, data, emails, phone_numbers)
print(json.dumps(profile_data, indent=2))