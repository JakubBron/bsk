## @file pdf.py
#  @brief Provides PDF signing and verification using RSA keys.

import hashlib

from Crypto.PublicKey import RSA

from config import LENGTHS


class PDF_Signer:
    """!
    @class PDF_Signer
    @brief Signs a PDF using RSA private keys.
    """
    private_key = None
    path_to_pdf = None
    path_to_signed_pdf = None

    def __init__(self, private_key, path: str, target_path: str) -> None:
        """!
		@brief Constructor for PDF_Signer.
        @param private_key PEM-encoded RSA private key.
        @param path Path to the original PDF file.
        @param target_path Path where the signed PDF will be saved.
        """
        self.private_key = RSA.import_key(private_key)
        self.path_to_pdf = path
        self.path_to_signed_pdf = target_path#+"_SIGNED_.pdf"

    def create_signature(self, pdf_hash):
        """!
		@brief Creates a numerical RSA signature from the PDF hash.
        @param pdf_hash SHA-256 hash of the PDF content.
        @return RSA signature as an integer.
        """
        signature = pow(int.from_bytes(pdf_hash, byteorder='big'), self.private_key.d, self.private_key.n)
        return signature

    def create_binary_signature(self, pdf_hash):
        """!
		@brief Converts numerical RSA signature into binary format.
        @param pdf_hash SHA-256 hash of the PDF content.
        @return Binary representation of the RSA signature.
        """
        
        signature = self.create_signature(pdf_hash)
        return signature.to_bytes(LENGTHS.SIGNATURE_LENGTH, byteorder='big')

    def sign_pdf(self):
        """!
		@brief Signs a PDF file and appends the signature.
        @return Status message indicating success or failure.
        """
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
                f.write(pdf+b"\nSIGNATURE\n"+signature_bin)
        
        except Exception as e:
            msg = f"Unable to create signed PDF to {self.path_to_signed_pdf} file! {e}"
            return msg
        

        return "\n=================================\nPDF signed and created!\n=================================\n"


class PDF_Verifier:
    """!
    @class PDF_Verifier
    @brief Verifies the signature of a signed PDF using the public key.
    """
    public_key = None
    path_to_signed_pdf = None

    def __init__(self, public_key, path: str) -> None:
        """!
		@brief Constructor for PDF_Verifier.
        @param public_key PEM-encoded RSA public key.
        @param path Path to the signed PDF file.
        """
        self.public_key = RSA.import_key(public_key)
        self.path_to_signed_pdf = path

    def validate_signature(self):
        """!
		@brief Verifies that the signature is valid and the file is unaltered.
        @return Status message indicating whether the signature is valid.
        """
        try:
            with open(self.path_to_signed_pdf, 'rb') as f:
                content = f.read()
                pdf_content, pdf_signature = content[:-LENGTHS.SIGNATURE_LENGTH-len("\nSIGNATURE\n")], content[-LENGTHS.SIGNATURE_LENGTH:]
                print(pdf_signature)
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