import os

# Use environment variables for proxy credentials for security
RESIDENTIAL_PROXY_URL = os.getenv('RESIDENTIAL_PROXY_URL', '')
DATACENTER_PROXY_URL = os.getenv('DATACENTER_PROXY_URL', '')

def residential_proxy():
    return RESIDENTIAL_PROXY_URL

def datacenter_proxy():
    return DATACENTER_PROXY_URL

def res_proxy():
    proxy_config = {
        "http": RESIDENTIAL_PROXY_URL,
        "https": RESIDENTIAL_PROXY_URL
    }
    return proxy_config

def datacenter_proxy_config():
    proxy_config = {
        "http": DATACENTER_PROXY_URL,
        "https": DATACENTER_PROXY_URL
    }
    return proxy_config