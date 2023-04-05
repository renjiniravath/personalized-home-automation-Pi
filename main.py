import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import http.client
import json

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
    if name in occupants:
        occupants.remove(name)
    else:
        occupants.append(name)
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
    return preferences

try:
    while True:
        occupants = readNameAndReturnUpdatedOccupants()
        print(occupants)
        response = updateOccupantsInRoom(occupants)
        print(response)
        preferences = getPreferenceFromOccupants(occupants)
        print(preferences)
except KeyboardInterrupt:
    GPIO.cleanup()
except:
    GPIO.cleanup()



    