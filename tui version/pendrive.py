import hashlib
from config import *
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from Crypto.PublicKey import RSA
import base64

class Pendrive:
    """
    Class which represents a pendrive.
    """
    pin = None
    aes_key = None

    def __init__(self):
        """
        Constructor of the class.
        """
        self.pin = None
        self.aes_key = None
    
    def __init__(self, pin: int) -> None:
        """
        Constructor of the class.
        """
        if not os.path.exists(FILENAMES.DRIVE):
            raise Exception(f"Drive {FILENAMES.DRIVE} is not plugged in or is damaged!")
        self.pin = pin
        self.aes_key = self.generate_AES_key(pin)


    def set_pin(self, new_pin: int) -> None:
        """
        Method which sets the pin of the pendrive. Setting new pin must set new AES key as well.
        """
        self.pin = new_pin
        self.aes_key = self.generate_AES_key(new_pin)

    def get_pin(self) -> int:
        """
        Method which returns the pin
        """
        return self.pin

    def generate_AES_key(self, pin: int) -> str:
        # return 256 bit hash 
        return hashlib.sha256(str(pin).encode()).digest()

    def get_AES_key(self) -> str:
        return self.aes_key

    def encrypt_AES(self, message: str) -> str:
        message = pad(message.encode(), AES.block_size)
        cipher = AES.new(self.aes_key, AES.MODE_CBC, MODES.AES_IV)
        return base64.b64encode(cipher.encrypt(message)).decode()
    
    
    def decrypt_AES(self, encrypted: str) -> str:
        encrypted = base64.b64decode(encrypted)
        cipher = AES.new(self.aes_key, AES.MODE_CBC, MODES.AES_IV)
        return unpad(cipher.decrypt(encrypted), AES.block_size).decode()

    def generate_RSA_key(self, encrypt=True) -> (str, str):
        key = RSA.generate(LENGTHS.RSA_LENGTH)
        public_key = key.publickey().export_key().decode()
        private_key = key.export_key().decode()
        private_key_encrypted = private_key
        if encrypt == True:
            private_key_encrypted = self.encrypt_AES(private_key)

        return (public_key, private_key_encrypted)
    
    def save_RSA_keys(self) -> str:
        public_key, private_key_encrypted = self.generate_RSA_key()
        if not os.path.exists(FILENAMES.DRIVE):
            return f"Drive {FILENAMES.DRIVE} is not plugged in or is dagamed!"

        if not os.path.exists(FILENAMES.DRIVE_LOCAL):
            return f"Drive {FILENAMES.DRIVE_LOCAL} is not plugged in or is dagamed!"

        try:    
            with open(FILENAMES.PRIVATE_KEY_ENCRYPTED, "w") as f:
                f.write(private_key_encrypted)
        except Exception as e:
            return f"Unable to save {FILENAMES.PRIVATE_KEY_ENCRYPTED} file! {e}"
        
        try:
            with open(FILENAMES.PUBLIC_KEY, 'w') as f:
                f.write(public_key)
        except Exception as e:
            return f"Unable to save {FILENAMES.PUBLIC_KEY} file! {e}"

        return "RSA keys saved!"
    
    def get_RSA_public_key(self) -> str:
        try:
            with open(FILENAMES.PUBLIC_KEY, "r") as f:
                return f.read()
        except Exception as e:
            return f"UNABLE TO READ {FILENAMES.PUBLIC_KEY} file! {e}"
    
    def get_RSA_private_key(self) -> str:
        try:
            with open(FILENAMES.PRIVATE_KEY_ENCRYPTED, "r") as f:
                content = f.read()
                return self.decrypt_AES(content)
        except Exception as e:
            return f"UNABLE TO READ {FILENAMES.PRIVATE_KEY_ENCRYPTED} file! {e}"
    
    def get_RSA_private_key_encrypted(self) -> str:
        try:
            with open(FILENAMES.PRIVATE_KEY_ENCRYPTED, "r") as f:
                return f.read()
        except Exception as e:
            return f"UNABLE TO READ {FILENAMES.PRIVATE_KEY_ENCRYPTED} file! {e}"

    def check_if_RSA_keys_exist(self) -> bool:
        return os.path.isfile(FILENAMES.PRIVATE_KEY_ENCRYPTED)