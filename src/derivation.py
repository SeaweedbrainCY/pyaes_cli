from hashlib import pbkdf2_hmac
from Crypto.Random import get_random_bytes

ITERATION = 1000000

def derive_key(password, salt=""):
    if not salt:
        salt = get_random_bytes(16)
    return pbkdf2_hmac('sha256', password.encode('utf-8'), salt, ITERATION)
