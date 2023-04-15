import RPi.GPIO as GPIO

redPin = 11
greenPin = 13
bluePin = 15

brightness = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)

pwmRed = GPIO.PWM(redPin, 50)
pwmGreen = GPIO.PWM(greenPin, 50)
pwmBlue = GPIO.PWM(bluePin, 50)

pwmRed.start(0)
pwmGreen.start(0)
pwmBlue.start(0)


def blink(pin):
    pin.ChangeDutyCycle(brightness)

def turnOff(pin):
	pin.ChangeDutyCycle(0)
        
def redOn():
	blink(pwmRed)
	
def greenOn():
	blink(pwmGreen)

def blueOn():
	blink(pwmBlue)
	
def yellowOn():
	blink(pwmRed)
	blink(pwmGreen)

def cyanOn():
	blink(pwmGreen)
	blink(pwmBlue)

def magentaOn():
	blink(pwmRed)
	blink(pwmBlue)

def whiteOn():
	blink(pwmRed)
	blink(pwmGreen)
	blink(pwmBlue)
	
def lightsOff():
	turnOff(pwmRed)
	turnOff(pwmGreen)
	turnOff(pwmBlue)

def changeLight(lightColor, lightBrightness):
	global brightness
	brightness = lightBrightness
	lightsOff()
	if lightColor == "Red":
		redOn()
	elif lightColor == "Green":
		greenOn()
	elif lightColor == "Blue":
		blueOn()
	elif lightColor == "Yellow":
		yellowOn()
	elif lightColor == "Cyan":
		cyanOn()
	elif lightColor == "Magenta":
		magentaOn()
	elif lightColor == "White":
		whiteOn()
		