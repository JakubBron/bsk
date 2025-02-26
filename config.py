DEFAULT_PIN = 1234

class LENGTHS:
    AES_LENGTH = 256
    SHA_LENGTH = 256
    RSA_LENGTH = 4096

class FILENAMES:
    DRIVE = "T:"
    PUBLIC_KEY = "T:\public_key.pem"
    PRIVATE_KEY_ENCRYPTED = "T:\private_key_encrypted.pem"

class MODES:
    AES_MODE = 2        # AES.MODE_CBC
    AES_IV = b"This is an IV456"    # 16 bytes