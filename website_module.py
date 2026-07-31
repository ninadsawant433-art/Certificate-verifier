# website_module.py
import ssl
import socket
from urllib.parse import urlparse
import requests
from datetime import datetime

def validate_website(url):
    if not url:
        return False, "No issuer URL", "Suspicious"
    
    parsed = urlparse(url)
    domain = parsed.netloc
    
    if 'digilocker.gov.in' in domain or 'nad.gov.in' in domain:
        return True, "Official DigiLocker/NAD domain", "Trusted"
    
    # Add SSL check
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:
                cert = ssock.getpeercert()
                expiry = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                if expiry < datetime.now():
                    return False, "SSL expired", "Suspicious"
        return True, "Valid SSL", "Trusted"
    except Exception:
        return False, "Invalid SSL/domain", "Suspicious"