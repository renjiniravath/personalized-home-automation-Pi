import Adafruit_DHT
import RPi.GPIO as GPIO
import src.environment as environment

heaterPin = 37
coolerPin = 38
humidifierPin = 40

GPIO.setup(heaterPin, GPIO.OUT)
GPIO.setup(coolerPin, GPIO.OUT)
GPIO.setup(humidifierPin, GPIO.OUT)

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4

def checkTemperatureAndHumidity():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None or temperature is not None:
        temperatureInF = (temperature*9/5) + 32.0
        print("Current Temperature: ", temperatureInF)
        print("Current Humidity: ", humidity)
        environment.roomConditions["temperature"] = temperatureInF
        environment.roomConditions["humidity"] = humidity
        controlTemperature(float(environment.settings["temperatureInF"] - temperatureInF))
        setHumidifier("ON" if humidity < environment.settings["humidity"] else "OFF")
    else:
        print("Sensor failure")


def controlTemperature(value):
    if value>0:
        print("heater on")
        environment.heaterStatus = "ON"
        environment.coolerStatus = "OFF"
        GPIO.output(heaterPin, GPIO.HIGH)
        GPIO.output(coolerPin, GPIO.LOW)
    else:
        print("cooler on")
        environment.heaterStatus = "OFF"
        environment.coolerStatus = "ON"
        GPIO.output(heaterPin, GPIO.LOW)
        GPIO.output(coolerPin, GPIO.HIGH)
    
def setHumidifier(value):
    if value == "ON":
        print("humidifier on")
        environment.humidifierStatus = "ON"
        GPIO.output(humidifierPin, GPIO.HIGH)
    else:
        environment.humidifierStatus = "OFF"
        GPIO.output(humidifierPin, GPIO.LOW)
