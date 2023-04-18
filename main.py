import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from handler import makeAPIRequest
from lighting import setLight
from dht11 import checkTemperatureAndHumidity
import threading
import environment
from display import displayStats, displayMessage

reader = SimpleMFRC522()
roomID = "1234"

def getRoomInfo():
    return makeAPIRequest("GET", "/rooms/" + roomID + "/settings")

def updateUserScan(user):
    return makeAPIRequest("PUT", "/rooms/" + roomID + "/users/" + user + "/scan")

def scanUserAndReturnRoomInfo():
    _, user = reader.read()
    user = user.strip()
    return user


def printRoomInfo():
    print("The occupants of this room are: ", environment.occupants)
    print("The current settings of this room are: ", environment.settings)


def setToPreferences(roomInfo):
    environment.occupants = roomInfo["occupants"]
    environment.settings = roomInfo["settings"]
    setLight()
    checkTemperatureAndHumidity()


def weatherCheck():
    while True:
        time.sleep(60*15)
        checkTemperatureAndHumidity()


weatherCheckThread = threading.Thread(target=weatherCheck, daemon=True)
displayThread = threading.Thread(target=displayStats, daemon=True)

try:
    roomInfo = getRoomInfo()
    if roomInfo != {}:
        setToPreferences(roomInfo)
        printRoomInfo()
        weatherCheckThread.start()
        displayThread.start()
        while True:
            print("Scanner ready to scan. You may scan now")
            user = scanUserAndReturnRoomInfo()
            roomInfo = updateUserScan(user)
            if roomInfo != {}:
                if user in environment.occupants:
                    displayMessage("Goodbye "+user + "!")
                else:
                    displayMessage("Welcome to the room "+user + "!")
                setToPreferences(roomInfo)
                printRoomInfo()
            print("Wait till prompted other wise to scan again")
            time.sleep(3)
    
except KeyboardInterrupt:
    GPIO.cleanup()
except Exception as err:
    print("Unexpected error occured: ", err)
    GPIO.cleanup()
