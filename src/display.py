from RPLCD import i2c
from time import sleep
import src.environment as environment

# constants to initialise the LCD
lcdmode = 'i2c'
cols = 20
rows = 4
charmap = 'A00'
i2c_expander = 'PCF8574'

address = 0x27 
port = 1

welcomeMessageShow = False
# Initialise the LCD
lcd = i2c.CharLCD(i2c_expander, address, port=port, charmap=charmap,
                  cols=cols, rows=rows)

def displayMessage(message):
    global welcomeMessageShow
    if message != "":
        welcomeMessageShow = True
        lcd.close(clear=True)
        lcd.write_string(message)
        sleep(3)
        welcomeMessageShow = False

def displayStats():
    while True:
        if welcomeMessageShow == False:
            lcd.close(clear=True)
            occupants = ', '.join(environment.occupants)
            lcd.write_string("Occupants in room")
            lcd.crlf()
            lcd.write_string(occupants if len(environment.occupants) > 0 else "Room is empty")
            sleep(3)

        if welcomeMessageShow == False:
            lcd.close(clear=True)
            lcd.write_string("Room Temp: "+ str(environment.roomConditions["temperature"]) + " F")
            lcd.crlf()
            lcd.write_string("Pref. Temp: "+ str(environment.settings["temperatureInF"]) + " F")
            lcd.crlf()
            lcd.write_string("Heater Status: " + environment.heaterStatus)
            lcd.crlf()
            lcd.write_string("Cooler Status: " + environment.coolerStatus)
            lcd.crlf()
            sleep(3)

        if welcomeMessageShow == False:
            lcd.close(clear=True)
            lcd.write_string("Room Humidity: "+ str(environment.roomConditions["humidity"]) + "%")
            lcd.crlf()
            lcd.write_string("Pref. Humidity: "+ str(environment.settings["humidity"])+" %")
            lcd.crlf()
            lcd.write_string("Humidifier: " + environment.humidifierStatus)
            lcd.crlf()
            sleep(3)

        if welcomeMessageShow == False:
            lcd.close(clear=True)
            lcd.write_string("Light Color: "+ environment.settings["lightColor"])
            lcd.crlf()
            lcd.write_string("Brightness: "+ str(environment.settings["lightBrightness"]))
            lcd.crlf()
            lcd.write_string("Fan Speed: "+ str(environment.settings["fanSpeed"]))
            lcd.crlf()
            sleep(3)
