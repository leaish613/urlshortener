import hashlib
import base64
import string
import random

def generate_short_url(original_url, length=7):
    """
    Generate a short URL using a combination of hashing and randomization.
    
    Args:
        original_url (str): The original URL to shorten
        length (int): The length of the short URL code
        
    Returns:
        str: A short URL code
    """
    # Create a hash of the original URL
    hash_object = hashlib.md5(original_url.encode())
    hash_digest = hash_object.digest()
    
    # Convert the hash to a base64 string and remove non-alphanumeric characters
    hash_b64 = base64.urlsafe_b64encode(hash_digest).decode()
    alphanumeric_hash = ''.join(c for c in hash_b64 if c.isalnum())
    
    # Take the first 'length' characters, or append random characters if needed
    if len(alphanumeric_hash) >= length:
        short_code = alphanumeric_hash[:length]
    else:
        # Unlikely, but handle edge cases by appending random characters
        additional_chars = ''.join(random.choices(
            string.ascii_letters + string.digits, 
            k=length-len(alphanumeric_hash)
        ))
        short_code = alphanumeric_hash + additional_chars
    
    return short_code

def is_valid_url(url):
    """
    Validate if the URL is properly formatted.
    
    Args:
        url (str): The URL to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    # This is a basic check that could be enhanced
    return url.startswith(("http://", "https://"))