import RPi.GPIO as GPIO
from time import sleep

class Buzzer:
    
    def __init__(self, pin_gpio, BCM_ACTIVE=True):
        self.PIN = pin_gpio
        if BCM_ACTIVE == True:
            GPIO.setmode(GPIO.BCM)
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


#-------------- Test ----------------------------
#print('BUZZER SYSTEM RUNNING...')
#GPIO.setmode(GPIO.BCM)
#buzzer = Buzzer(27)
#buzzer.alarm()
#buzzer.set_status('HIGH')
#sleep(5)
#buzzer.set_status('LOW')
#print(buzzer.get_status())
#sleep(2)
#buzzer.set_status()
#sleep(3)
#print(buzzer.get_status())
#GPIO.cleanup()
#print("\033[31mSystem Finished!\033[m")
