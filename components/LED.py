import RPi.GPIO as GPIO
from time import sleep

class LED:
    def __init__(self, pin_gpio, GPIO_AUTO_CONFIG=True):
        if GPIO_AUTO_CONFIG == True:
            GPIO.setmode(GPIO.BCM)
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



#-------------- Test ----------------------------
if __name__ == '__main__':    
    print('LED SYSTEM RUNNING...')
    led = LED(17)
    led.blink(50, 0.1)
    led.set_status('HIGH')
    sleep(5)
    led.set_status('LOW')
    print(led.get_status())
    sleep(2)
    led.set_status()
    sleep(3)
    print(led.get_status())
    GPIO.cleanup()
    print("\033[31mSystem Finished!\033[m")
