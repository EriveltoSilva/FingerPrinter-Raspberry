import RPi.GPIO as GPIO
from time import sleep

class Buzzer:
    
    def __init__(self, pin_gpio):
        self.PIN = pin_gpio
        GPIO.setup(self.PIN, GPIO.OUT)
        GPIO.output(self.PIN, GPIO.HIGH)
        sleep(1.5)
        GPIO.output(self.PIN, GPIO.LOW)

    def set_status(self, status='HIGH'):
        status = status.upper()
        if status == 'HIGH':
            GPIO.output(self.PIN, GPIO.HIGH)
        else:
            GPIO.output(self.PIN, GPIO.LOW)
    
    def get_status(self):
        return GPIO.input(self.PIN)


    def bip(self, interval=0.5):
            GPIO.output(self.PIN, GPIO.HIGH)
            sleep(interval)
            GPIO.output(self.PIN, GPIO.LOW)

    def alarm(self, interval=2):
            self.bip(interval)
