from Crypto.Cipher import AES
import pathlib
from uuid import uuid4

def encrypt(zip_file_path:str, dest:str, key:bytes, key_salt:bytes):
    cipher = AES.new(key, AES.MODE_GCM)
    with open(zip_file_path, 'rb') as f:
        data = f.read()
        ciphertext, tag = cipher.encrypt_and_digest(data)
        with open(dest, 'wb') as f:
            [f.write(x) for x in (key_salt, cipher.nonce, tag, ciphertext)]
    return True

def decrypt(file_path:str, key:bytes):
    dest = f"/tmp/{uuid4()}"
    with open(file_path, 'rb') as f:
        _, nonce, tag, ciphertext = [f.read(x) for x in (16,16, 16, -1)]
        cipher = AES.new(key, AES.MODE_GCM, nonce)
        try:
            data = cipher.decrypt_and_verify(ciphertext, tag)
            with open(dest, 'wb') as f:
                f.write(data)
            return dest
        except ValueError:
            return None
            
def get_key_salt(file_path:str):
    with open(file_path, 'rb') as f:
        key_salt = f.read(16)
    return key_salt