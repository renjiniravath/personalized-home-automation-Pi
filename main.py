import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from handler import makeAPIRequest
from lighting import changeLight

reader = SimpleMFRC522()
roomID = "1234"
roomInfo = {}

def getRoomInfo():
    return makeAPIRequest("GET", "/rooms/" + roomID + "/settings")

def updateUserScan(user):
    return makeAPIRequest("PUT", "/rooms/" + roomID + "/users/"+ user +"/scan")

def scanUserAndReturnRoomInfo():
    _, user = reader.read()
    user = user.strip()
    if user in roomInfo["occupants"]:
        print("Goodbye ",user, "!")
    else:
        print("Welcome to the room ",user, "!")
    return user

def printRoomInfo():
    print("The occupants of this room are: ", roomInfo["occupants"])
    print("The current settings of this room are: ", roomInfo["settings"])

def setToPreferences():
    changeLight(roomInfo["settings"]["lightColor"], roomInfo["settings"]["lightBrightness"])

try:
    roomInfo = getRoomInfo()
    setToPreferences()
    printRoomInfo()
    while True:
        print("Scanner ready to scan. You may scan now")
        user = scanUserAndReturnRoomInfo()
        roomInfo = updateUserScan(user)
        printRoomInfo()
        setToPreferences()
        print("Wait till prompted other wise to scan again")
        time.sleep(2)
except KeyboardInterrupt:
    GPIO.cleanup()
except Exception as err:
    print("Unexpected error occured: ",err)
    GPIO.cleanup()



    