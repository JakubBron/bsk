from pendrive import Pendrive
from config import DEFAULT_PIN
from pdf import PDF_Signer, PDF_Verifier

import os

def get_RSA() -> (str, str):
    try:
        print("Checking if any RSA keys are saved...")

        p = Pendrive(DEFAULT_PIN)
        if p.check_if_RSA_keys_exist():
            print("RSA keys exist!")
            again = True
            RSA_public_key = None
            RSA_private_key = None

            while again:
                print("Enter password to get private key")
                pin = int(input("Enter pin: "))
                p = Pendrive(pin)
                print("Trying to obtain keys... \n")

                RSA_public_key = p.get_RSA_public_key()
                RSA_private_key = p.get_RSA_private_key()
                if "UNABLE TO READ" in RSA_private_key:
                    print("Error, password is incorrect!")
                    print("Try again.")
                    again = True
                else:
                    again = False

            print("Public key (stored somewhere else)\n" + "Len is: " + str(len(RSA_public_key)))
            print("Private key: \n" + "Len is " + str(len(RSA_private_key)))
            return RSA_public_key, RSA_private_key
        
        else:
            print("RSA keys do not exist!")
            print("Use pendrive_app.py to create new RSA.")
            return 1,1
    except Exception as e:
        print(e)

def get_PDF_to_sign(priv):
    print("Enter path to PDF file to sign:")
    path = input("Path: ")
    if os.path.isfile(path) and ".pdf" in path:
        print("Trying to sign PDF...")
        pdf = PDF_Signer(priv, path)
        result = pdf.sign_pdf()
        print(result)
    else:
        print("\nFile does not exist or is not supported!")

def get_PDF_to_verify(pub):
    print("Enter path to PDF file to verify:")
    path = input("Path: ")
    if os.path.isfile(path) and ".pdf" in path:
        print("Trying to verify PDF...")
        pdf = PDF_Verifier(pub, path)
        result = pdf.validate_signature()
        print(result)
    else:
        print("\nFile does not exist or is not suppoted!")

def app():
    print("Welcome to PDF signer! \n\n")
    pub = None,
    priv = None
    try:
        pub, priv = get_RSA()
    except Exception as e:
        return

    if pub != 1 and priv != 1:
        control = ""
        while control != "exit":
            print("Allowed commands: sign, verify, exit")
            control = input("Enter command: ")
            control = control.lower()

            match control:
                case "sign":
                    get_PDF_to_sign(priv)
                case "verify":
                    get_PDF_to_verify(pub)
                case "exit":
                    break
                case _:
                    print("Unknown command!")
   

if __name__ == "__main__":
   app()