import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
from src.handler import makeAPIRequest
from src.lighting import setLight
from src.dht11 import checkTemperatureAndHumidity
import threading
import src.environment as environment
from src.display import displayStats, displayMessage
from src.fan import changeMotorSpeed
from src.scanIndicator import *
from src.subscriber import mqttSetup

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
    changeMotorSpeed()

def changeSubscription():
    environment.mqttClient.unsubscribe('#')
    if(len(environment.occupants) > 0):
        environment.mqttClient.subscribe('preferences/'+'-'.join(environment.occupants))

def weatherCheck():
    while True:
        time.sleep(60*15)
        checkTemperatureAndHumidity()

def refreshPreferences(client, userdata, message):
    print("Message received from broker. Topic: ", message.topic, " Content: ", message.payload)
    roomInfo = getRoomInfo()
    setToPreferences(roomInfo)
    printRoomInfo()


weatherCheckThread = threading.Thread(target=weatherCheck, daemon=True)
displayThread = threading.Thread(target=displayStats, daemon=True)
mqttSubscriberThread = threading.Thread(target=mqttSetup, daemon=True)

try:
    roomInfo = getRoomInfo()
    mqttSubscriberThread.start()
    if roomInfo != {}:
        environment.mqttClient.on_message = refreshPreferences
        setToPreferences(roomInfo)
        changeSubscription()
        printRoomInfo()
        weatherCheckThread.start()
        displayThread.start()
        while True:
            print("Scanner ready to scan. You may scan now")
            scanAwait()
            user = scanUserAndReturnRoomInfo()
            roomInfo = updateUserScan(user)
            if roomInfo != {}:
                scanSuccess()
                if user in environment.occupants:
                    displayMessage("Goodbye "+user + "!")
                else:
                    displayMessage("Welcome to the room "+user + "!")
                setToPreferences(roomInfo)
                changeSubscription()
                printRoomInfo()
            else:
                scanFail()
            print("Wait till prompted other wise to scan again")
            time.sleep(2.5)
    
except KeyboardInterrupt:
    GPIO.cleanup()
except Exception as err:
    print("Unexpected error occured: ", err)
    GPIO.cleanup()
