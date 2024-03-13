from Crypto.Cipher import AES
import pathlib

def encrypt(zip_file_path:str, dest:str, key:bytes):
    cipher = AES.new(key, AES.MODE_GCM)
    with open(zip_file_path, 'rb') as f:
        data = f.read()
        ciphertext, tag = cipher.encrypt_and_digest(data)
        with open(dest, 'wb') as f:
            [f.write(x) for x in (cipher.nonce, tag, ciphertext)]
    return True
            
