import RPi.gpio as GPIO
from time import sleep

class LED:
    def __init__(self, pin_gpio):
        self.PIN = pin_gpio
        GPIO.setup(self.PIN, GPIO.OUT)
        GPIO.output(self.PIN, GPIO.HIGH)

    def set_status(self, status='HIGH'):
        status = status.upper()
        if status == 'HIGH':
            GPIO.output(self.PIN, GPIO.HIGH)
        else:
            GPIO.output(self.PIN, GPIO.LOW)
    
    def get_status(self):
        return GPIO.input(self.PIN)


    def blink(self, n, interval=1):
        for x in range(n):
            GPIO.output(self.PIN, GPIO.HIGH)
            sleep(interval)
            GPIO.output(self.PIN, GPIO.LOW)
            sleep(interval)