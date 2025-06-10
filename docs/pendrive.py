## @file pendrive.py
#  @brief Represents a pendrive for secure RSA key management and AES encryption.

import hashlib
from config import *
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.PublicKey import RSA
import base64

class Pendrive:
"""!
@class Pendrive
@brief Represents a pendrive storing encrypted RSA keys and providing AES-based encryption.
"""
pin = None
aes_key = None
drive = None
private_key_path = None
public_key_path = None

def __init__(self, drive, public_key_path=None, pin=None):
"""!
@brief Constructor for Pendrive class.
@param drive Path to the mounted pendrive.
@param public_key_path Directory where the public key is or will be stored.
@param pin PIN used to derive AES key.
"""
if not os.path.exists(drive):
    raise Exception(f"Drive {drive} is not plugged in or is damaged!")
self.pin = pin
self.aes_key = self.generate_AES_key(pin) if pin else None
self.drive = drive
self.private_key_path = os.path.join(drive, FILENAMES.PRIVATE_KEY_ENCRYPTED)
self.public_key_path = os.path.join(public_key_path, FILENAMES.PUBLIC_KEY)


def set_pin(self, new_pin: int) -> None:
"""!
@brief Sets the PIN and regenerates AES key.
@param new_pin The new PIN value.
"""
self.pin = new_pin
self.aes_key = self.generate_AES_key(new_pin)

def get_pin(self) -> int:
"""!
@brief Returns the current PIN.
@return PIN value.
"""
return self.pin

def generate_AES_key(self, pin: int) -> str:
"""!
@brief Generates a 256-bit AES key from a PIN.
@param pin Integer PIN.
@return AES key derived via SHA-256.
""" 
return hashlib.sha256(str(pin).encode()).digest()

def get_AES_key(self) -> str:
"""!
@brief Gets the AES key.
@return Current AES key.
"""
return self.aes_key

def encrypt_AES(self, message: str) -> str:
"""!
@brief Encrypts a message using AES.
@param message Plaintext message.
@return Base64-encoded ciphertext.
"""

message = pad(message.encode(), AES.block_size)
cipher = AES.new(self.aes_key, AES.MODE_CBC, MODES.AES_IV)
return base64.b64encode(cipher.encrypt(message)).decode()


def decrypt_AES(self, encrypted: str) -> str:
"""!
@brief Decrypts a Base64-encoded AES-encrypted message.
@param encrypted Base64-encoded ciphertext.
@return Decrypted plaintext.
"""
encrypted = base64.b64decode(encrypted)
cipher = AES.new(self.aes_key, AES.MODE_CBC, MODES.AES_IV)
return unpad(cipher.decrypt(encrypted), AES.block_size).decode()

def generate_RSA_key(self, encrypt=True) -> (str, str):
"""!
@brief Generates RSA public/private key pair.
@param encrypt Whether to AES-encrypt the private key.
@return Tuple containing public key and (optionally encrypted) private key.
"""
key = RSA.generate(LENGTHS.RSA_LENGTH)
public_key = key.publickey().export_key().decode()
private_key = key.export_key().decode()
private_key_encrypted = private_key
if encrypt == True:
    private_key_encrypted = self.encrypt_AES(private_key)

return (public_key, private_key_encrypted)

def save_RSA_keys(self) -> str:
"""!
@brief Saves the generated RSA keys to the pendrive and public key path.
@return Message indicating result.
"""
public_key, private_key_encrypted = self.generate_RSA_key()
if not os.path.exists(self.drive):
    return f"Drive {self.drive} is not plugged in or is dagamed!"

try:
    with open(self.private_key_path, "w") as f:
    f.write(private_key_encrypted)
except Exception as e:
    return f"Unable to save {self.private_key_path} file! {e}"

try:
    with open(self.public_key_path, 'w') as f:
    f.write(public_key)
except Exception as e:
    return f"Unable to save {self.public_key_path} file! {e}"

return f"RSA keys saved {self.private_key_path} {self.public_key_path}!"

def get_RSA_public_key(self) -> str:
"""!
@brief Reads and returns the stored public key.
@return Public key or error message.
"""
try:
    with open(self.public_key_path, "r") as f:
    return f.read()
except Exception as e:
    return f"UNABLE TO READ {self.public_key_path} file! {e}"

def get_RSA_private_key(self) -> str:
"""!
@brief Reads and decrypts the private key.
@return Private key or error message.
"""
try:
    with open(self.private_key_path, "r") as f:
    content = f.read()
    return self.decrypt_AES(content)
except Exception as e:
    return f"UNABLE TO READ {FILENAMES.PRIVATE_KEY_ENCRYPTED} file! {e}"

def get_RSA_private_key_encrypted(self) -> str:
"""!
@brief Reads the encrypted private key file.
@return Encrypted private key or error message.
"""
try:
    with open(self.drive+'\\'+FILENAMES.PRIVATE_KEY_ENCRYPTED, "r") as f:
    return f.read()
except Exception as e:
    return f"UNABLE TO READ {FILENAMES.PRIVATE_KEY_ENCRYPTED} file! {e}"

def check_if_RSA_keys_exist(self) -> bool:
"""!
@brief Checks if the public key exists on the drive.
@return True if it exists, False otherwise.
"""
return os.path.isfile(self.public_key_path)