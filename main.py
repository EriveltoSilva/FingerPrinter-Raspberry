import RPi.GPIO as GPIO
from time import sleep

from components.LED import LED
from components.Buzzer import Buzzer
from components.Biometric import Biometric

MY_LED = 17
MY_BUZZER = 27


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = LED(MY_LED)
buzzer = Buzzer(MY_BUZZER)
finger = Biometric()
