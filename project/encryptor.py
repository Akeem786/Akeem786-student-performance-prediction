from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os
import hashlib

def derive_key(password):
    """Generate a 32-byte (256-bit) key from password"""
    return hashlib.sha256(password.encode()).digest()

def encrypt_file(file_path, password):
    """Encrypt a file using AES-256"""
    key = derive_key(password)
    iv = get_random_bytes(16)  # AES uses a 16-byte IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    with open(file_path, "rb") as f:
        data = f.read()
    
    # Padding for AES block size (16 bytes)
    padding_length = 16 - (len(data) % 16)
    data += bytes([padding_length]) * padding_length

    encrypted_data = cipher.encrypt(data)

    with open(file_path + ".enc", "wb") as f:
        f.write(iv + encrypted_data)

    print(f"✅ File Encrypted: {file_path}.enc")

def decrypt_file(file_path, password):
    """Decrypt a file using AES-256"""
    key = derive_key(password)

    with open(file_path, "rb") as f:
        iv = f.read(16)  # Read IV
        encrypted_data = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)

    # Remove padding
    padding_length = decrypted_data[-1]
    decrypted_data = decrypted_data[:-padding_length]

    decrypted_file = file_path.replace(".enc", "_decrypted")
    with open(decrypted_file, "wb") as f:
        f.write(decrypted_data)

    print(f"✅ File Decrypted: {decrypted_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AES-256 File Encryption Tool")
    parser.add_argument("-m", "--mode", choices=["encrypt", "decrypt"], required=True, help="Mode: encrypt or decrypt")
    parser.add_argument("-f", "--file", required=True, help="File to encrypt/decrypt")
    parser.add_argument("-p", "--password", required=True, help="Encryption password")

    args = parser.parse_args()

    if args.mode == "encrypt":
        encrypt_file(args.file, args.password)
    elif args.mode == "decrypt":
        decrypt_file(args.file, args.password)
