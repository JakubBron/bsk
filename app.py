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
            p.set_pin(pin)
            print("Device detected! \n")
            print("Private key: \n" + p.get_RSA_private_key())
            print("Public key: \n", p.get_RSA_public_key())
        else:
            print("RSA keys do not exist!")
    except Exception as e:
        print(e)


app()