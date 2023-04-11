import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import http.client
import json
import time

reader = SimpleMFRC522()
basketConn = http.client.HTTPSConnection("getpantry.cloud")
roomID = "1234"
APIKey = "95850410-ddee-42f6-8eba-483644fca996"

def getBasketValue(basketName):
    payload = ''
    headers = {
    'Content-Type': 'application/json'
    }
    basketConn.request("GET", "/apiv1/pantry/"+APIKey+"/basket/"+basketName, payload, headers)
    res = basketConn.getresponse()
    data = res.read()
    return json.loads(data)

def updateBasketValue(basketName, payload):
    headers = {
    'Content-Type': 'application/json'
    }
    basketConn.request("POST", "/apiv1/pantry/"+APIKey+"/basket/"+basketName, payload, headers)
    res = basketConn.getresponse()
    data = res.read()
    return data.decode("utf-8")

def readNameAndReturnUpdatedOccupants():
    _, name = reader.read()
    name = name.strip()
    room = getBasketValue("Room-"+roomID)
    occupants = room["occupants"]
    print("Previous occupants of the room ",occupants)
    if name in occupants:
        occupants.remove(name)
        print("Goodbye ",name, "!")
    else:
        occupants.append(name)
        print("Welcome to the room ",name, "!")
        occupants.sort()
    return occupants

def updateOccupantsInRoom(occupants):
    payload = json.dumps({
        "occupants": occupants
    })
    result = updateBasketValue("Room-"+roomID, payload)
    return result

def getPreferenceFromOccupants(occupants):
    occupantsString = ""
    if len(occupants) == 0:
        occupantsString = "Default"
    else:
        occupantsString = "-".join(occupants)
    preferences = getBasketValue("Preferences-"+occupantsString)
    print("Preferences changed to Preferences-"+occupantsString)
    return preferences

try:
    while True:
        print("Scanner ready to scan. You may scan now")
        occupants = readNameAndReturnUpdatedOccupants()
        print("Updated occupants of the room ",occupants)
        response = updateOccupantsInRoom(occupants)
        print(response)
        preferences = getPreferenceFromOccupants(occupants)
        print(preferences)
        print("Wait till prompted other wise to scan again")
        time.sleep(5)
except KeyboardInterrupt:
    GPIO.cleanup()
except Exception as err:
    print("Unexpected error occured: ",err)
    GPIO.cleanup()



    