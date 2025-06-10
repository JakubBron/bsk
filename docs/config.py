## @file config.py
#  @brief Configuration constants for cryptographic operations.

#DEFAULT_PIN = 1234

class LENGTHS:
    """!
    @class LENGTHS
    @brief Contains cryptographic key and hash lengths.
    """
    AES_LENGTH = 256
    SHA_LENGTH = 256
    RSA_LENGTH = 4096
    SIGNATURE_LENGTH = 512

class FILENAMES:
    """!
    @class FILENAMES
    @brief File names and paths for RSA key storage.
    """
    #DRIVE = "T:"
    DRIVE_LOCAL = "."
    #PUBLIC_KEY = os.path.join(DRIVE_LOCAL, "public_key.pem")
    #PRIVATE_KEY_ENCRYPTED = os.path.join(DRIVE, "\private_key_encrypted.pem")
    PUBLIC_KEY = "public_key.pem"
    PRIVATE_KEY_ENCRYPTED = "private_key_encrypted.pem"


class MODES:
    """!
    @class MODES
    @brief AES operation modes and IV settings.
    """
    AES_MODE = 2        # AES.MODE_CBC
    AES_IV = b"This is an IV456"    # 16 bytes