import RPi.GPIO as GPIO
import time

redPin = 26
greenPin = 32
bluePin = 29

GPIO.setmode(GPIO.BOARD)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)

pwmRed = GPIO.PWM(redPin, 50)
pwmGreen = GPIO.PWM(greenPin, 50)

pwmRed.start(0)
pwmGreen.start(0)

def scanAwait():
    indicatorOff()
    GPIO.output(bluePin,GPIO.HIGH)


def indicatorOff():
    pwmRed.ChangeDutyCycle(0)
    pwmGreen.ChangeDutyCycle(0)
    GPIO.output(bluePin,GPIO.LOW)

    
def scanSuccess():
    indicatorOff()
    pwmRed.ChangeDutyCycle(0)
    for i in range(4):
        pwmGreen.ChangeDutyCycle(100)
        time.sleep(0.3)
        pwmGreen.ChangeDutyCycle(0)
        time.sleep(0.3)

    

def scanFail():
    indicatorOff()
    pwmGreen.ChangeDutyCycle(0)
    for i in range(4):
        pwmRed.ChangeDutyCycle(100)
        time.sleep(0.3)
        pwmRed.ChangeDutyCycle(0)
        time.sleep(0.3)
        