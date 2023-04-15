import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

def writeValue(name):
    reader.write(name)
    print("Write successful")

def readValue():
    _, name = reader.read()
    print("Card owner name: ",name)

try:
    while True:
        print("Scan ID to read")
        readValue()
        value = input("Do you want to change the card owners's name? Enter Y to change: ")
        if value == "Y":
            name = input("Enter the updated name: ")
            writeValue(name)
            readValue()
        else:
            print("Thank you!")
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()
except Exception as err:
    print("Unexpected error occured: ",err)
    GPIO.cleanup()
