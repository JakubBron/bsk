import os
import hashlib
from Crypto.PublicKey import RSA

from config import LENGTHS


class PDF_Signer:
    """
    Class to sign PDF files using RSA keys.
    """
    private_key = None
    path_to_pdf = None
    path_to_signed_pdf = None

    def __init__(self, private_key, path: str) -> None:
        """
        Constructor of the class.
        """
        self.private_key = RSA.import_key(private_key)
        self.path_to_pdf = path
        self.path_to_signed_pdf = path.split('.pdf')[0]+"_SIGNED_.pdf"

    def create_signature(self, pdf_hash):
        """
            Returns a big number - signature
        """
        signature = pow(int.from_bytes(pdf_hash, byteorder='big'), self.private_key.d, self.private_key.n)
        return signature

    def create_binary_signature(self, pdf_hash):
        signature = self.create_signature(pdf_hash)
        return signature.to_bytes(LENGTHS.SIGNATURE_LENGTH, byteorder='big')

    def sign_pdf(self):
        pdf = None
        pdf_hash = None
        try:
            with open(self.path_to_pdf, 'rb') as f:
                pdf = f.read()
                pdf_hash = hashlib.sha256(pdf).digest()
                
        except Exception as e:
            msg = f"Unable to read unisgned PDF from {self.path_to_pdf} file! {e}"
            return msg
        
        signature_bin = self.create_binary_signature(pdf_hash)

        try:
            with open(self.path_to_signed_pdf, 'wb') as f:
                f.write(pdf+signature_bin)
        
        except Exception as e:
            msg = f"Unable to create signed PDF to {self.path_to_signed_pdf} file! {e}"
            return msg
        

        return "\n=================================\nPDF signed and created!\n=================================\n"


class PDF_Verifier:
    """
    Class to verify sign on PDF file.
    """
    public_key = None
    private_key = None
    path_to_signed_pdf = None

    def __init__(self, public_key, path: str) -> None:
        """
        Constructor of the class.
        """
        self.public_key = RSA.import_key(public_key)
        self.path_to_signed_pdf = path

    def validate_signature(self):
        pdf_content = None
        pdf_signature = None
        try:
            with open(self.path_to_signed_pdf, 'rb') as f:
                content = f.read()
                pdf_content, pdf_signature = content[:-LENGTHS.SIGNATURE_LENGTH], content[-LENGTHS.SIGNATURE_LENGTH:]
        except Exception as e:
            return f"Unable to read signed PDF. Exception: {e}"

        pdf_content_hash = hashlib.sha256(pdf_content).digest()
        signed_hash = pow(int.from_bytes(pdf_signature, byteorder='big'), self.public_key.e, self.public_key.n)

        try:
            decrypted_hash_bytes = signed_hash.to_bytes(LENGTHS.SHA_LENGTH//8, byteorder='big')
        except OverflowError:
            return "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nSignaure not valid, PDF was changed!\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"

        if pdf_content_hash == decrypted_hash_bytes:
            return "\n=================================\nSignature is valid!\n=================================\n"
        else:
            return "\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\nSignaure not valid, PDF was changed!\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n"