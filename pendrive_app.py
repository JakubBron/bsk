from pendrive import Pendrive
from config import *

def pendrive_app():
    print("Welcome to create pendrive app! \n\n")

    try:
        print("Checking if any RSA keys are saved...")
        p = Pendrive(DEFAULT_PIN)
        if p.check_if_RSA_keys_exist():
            print("RSA keys already exist!")
            print("Public key: \n" + p.get_RSA_public_key())
            print("Private key encrypted: \n" + p.get_RSA_private_key_encrypted())
        else:
            print("RSA keys do not exist! \n")
            print("Creating RSA keys...")
            pin = int(input("Enter pin: "))
            p.set_pin(pin)
            print("Creating keys... Please wait.")
            result = p.save_RSA_keys()
            print(result)

    except Exception as e:
        print(e)
    
if __name__ == "__main__":
    pendrive_app()