import os

#DEFAULT_PIN = 1234

class LENGTHS:
    AES_LENGTH = 256
    SHA_LENGTH = 256
    RSA_LENGTH = 4096
    SIGNATURE_LENGTH = 512

class FILENAMES:
    #DRIVE = "T:"
    DRIVE_LOCAL = "."
    #PUBLIC_KEY = os.path.join(DRIVE_LOCAL, "public_key.pem")
    #PRIVATE_KEY_ENCRYPTED = os.path.join(DRIVE, "\private_key_encrypted.pem")
    PUBLIC_KEY = "public_key.pem"
    PRIVATE_KEY_ENCRYPTED = "private_key_encrypted.pem"

class MODES:
    AES_MODE = 2        # AES.MODE_CBC
    AES_IV = b"This is an IV456"    # 16 bytes