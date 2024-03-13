from hashlib import pbkdf2_hmac

ITERATION = 1000000

def derive_key(password, salt):
    return pbkdf2_hmac('sha256', password.encode('utf-8'), salt, ITERATION)
