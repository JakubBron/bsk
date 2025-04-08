from pendrive import Pendrive
from config import DEFAULT_PIN

def app():
    print("Welcome to PDF signer! \n\n")

    try:
        print("Checking if any RSA keys are saved...")
        p = Pendrive(DEFAULT_PIN)
        if p.check_if_RSA_keys_exist():
            print("RSA keys exist!")
            print("Enter password to get private key")
            pin = int(input("Enter pin: "))
            p = Pendrive(pin)
            print("Trying to obtain keys... \n")

            RSA_public_key = p.get_RSA_public_key()
            RSA_private_key = p.get_RSA_private_key()
            if "UNABLE TO READ" in RSA_private_key:
                print("Error, password is incorrect!")
                print("Ending programme.")
                return
            else:
                print("Public key (stored somewhere else)\n" + RSA_public_key)
                print("Private key: \n" + RSA_private_key)
        else:
            print("RSA keys do not exist!")
            print("Use pendrive_app.py to create new RSA.")
    except Exception as e:
        print(e)


app()