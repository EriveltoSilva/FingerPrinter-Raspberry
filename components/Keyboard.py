import RPi.GPIO as GPIO
from time import sleep


class Keyboard:
	def __init__(self, lines=[5,6,13,19], columns=[26,16,20], GPIO_AUTO_CONFIG=True):
		if GPIO_AUTO_CONFIG == True:
			GPIO.setwarnings(False)
			GPIO.setmode(GPIO.BCM)

		self.LINE1 = lines[0]
		self.LINE2 = lines[1]
		self.LINE3 = lines[2]
		self.LINE4 = lines[3]
		
		self.COLUMN1 = columns[0]
		self.COLUMN2 = columns[1]
		self.COLUMN3 = columns[2]


		GPIO.setup(self.LINE1, GPIO.OUT)
		GPIO.setup(self.LINE2, GPIO.OUT)
		GPIO.setup(self.LINE3, GPIO.OUT)
		GPIO.setup(self.LINE4, GPIO.OUT)

		GPIO.setup(self.COLUMN1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.COLUMN2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.COLUMN3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		
		#GPIO.add_event_detect(self.COLUMN1, GPIO.FALLING, callback=self.key_pressed, bouncetime=100)

		
	def wait_key_pressed(self):
		while True:				
			GPIO.output(self.LINE1, GPIO.LOW)
			if GPIO.input(self.COLUMN1) == 0:
				while GPIO.input(self.COLUMN1)==0:
					pass
				return '1'
			elif GPIO.input(self.COLUMN2) == 0:
				while GPIO.input(self.COLUMN2)==0:
					pass
				return '2'
			elif GPIO.input(self.COLUMN3) == 0:
				while GPIO.input(self.COLUMN3)==0:
					pass
				return '3'
			GPIO.output(self.LINE1, GPIO.HIGH)
			
			
			GPIO.output(self.LINE2, GPIO.LOW)
			if GPIO.input(self.COLUMN1) == 0:
				while GPIO.input(self.COLUMN1)==0:
					pass
				return '4'
			elif GPIO.input(self.COLUMN2) == 0:
				while GPIO.input(self.COLUMN2)==0:
					pass
				return '5'
			elif GPIO.input(self.COLUMN3) == 0:
				while GPIO.input(self.COLUMN3)==0:
					pass
				return '6'
			GPIO.output(self.LINE2, GPIO.HIGH)
				 
				 
			GPIO.output(self.LINE3, GPIO.LOW)
			if GPIO.input(self.COLUMN1) == 0:
				while GPIO.input(self.COLUMN1)==0:
					pass
				return '7'
			elif GPIO.input(self.COLUMN2) == 0:
				while GPIO.input(self.COLUMN2)==0:
					pass
				return '8'
			elif GPIO.input(self.COLUMN3) == 0:
				while GPIO.input(self.COLUMN3)==0:
					pass
				return '9'
			GPIO.output(self.LINE3, GPIO.HIGH)
				 
			
			GPIO.output(self.LINE4, GPIO.LOW)
			if GPIO.input(self.COLUMN1) == 0:
				while GPIO.input(self.COLUMN1)==0:
					pass
				return '*'
			elif GPIO.input(self.COLUMN2) == 0:
				while GPIO.input(self.COLUMN2)==0:
					pass
				return '0'
			elif GPIO.input(self.COLUMN3) == 0:
				while GPIO.input(self.COLUMN3)==0:
					pass
				return '#'
			GPIO.output(self.LINE4, GPIO.HIGH)
			
		return ''
			 

	      
		
	def key_pressed(self):
		GPIO.output(self.LINE1, GPIO.LOW)
		if GPIO.input(self.COLUMN1) == 0:
			while GPIO.input(self.COLUMN1)==0:
				pass
			return '1'
		elif GPIO.input(self.COLUMN2) == 0:
			while GPIO.input(self.COLUMN2)==0:
				pass
			return '2'
		elif GPIO.input(self.COLUMN3) == 0:
			while GPIO.input(self.COLUMN3)==0:
				pass
			return '3'
		GPIO.output(self.LINE1, GPIO.HIGH)
		
		
		GPIO.output(self.LINE2, GPIO.LOW)
		if GPIO.input(self.COLUMN1) == 0:
			while GPIO.input(self.COLUMN1)==0:
				pass
			return '4'
		elif GPIO.input(self.COLUMN2) == 0:
			while GPIO.input(self.COLUMN2)==0:
				pass
			return '5'
		elif GPIO.input(self.COLUMN3) == 0:
			while GPIO.input(self.COLUMN3)==0:
				pass
			return '6'
		GPIO.output(self.LINE2, GPIO.HIGH)
			 
			 
		GPIO.output(self.LINE3, GPIO.LOW)
		if GPIO.input(self.COLUMN1) == 0:
			while GPIO.input(self.COLUMN1)==0:
				pass
			return '7'
		elif GPIO.input(self.COLUMN2) == 0:
			while GPIO.input(self.COLUMN2)==0:
				pass
			return '8'
		elif GPIO.input(self.COLUMN3) == 0:
			while GPIO.input(self.COLUMN3)==0:
				pass
			return '9'
		GPIO.output(self.LINE3, GPIO.HIGH)
			 
		
		GPIO.output(self.LINE4, GPIO.LOW)
		if GPIO.input(self.COLUMN1) == 0:
			while GPIO.input(self.COLUMN1)==0:
				pass
			return '*'
		elif GPIO.input(self.COLUMN2) == 0:
			while GPIO.input(self.COLUMN2)==0:
				pass
			return '0'
		elif GPIO.input(self.COLUMN3) == 0:
			while GPIO.input(self.COLUMN3)==0:
				pass
			return '#'
		GPIO.output(self.LINE4, GPIO.HIGH)
		
		return ''
		 
		 
if __name__ == '__main__':	
	from LED import LED	
	try:
		print('System running...')
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		led = LED(17, False)
		keyboard = Keyboard([5,6,13,19],[26,16,20], False)
		while True:
			led.set_status('HIGH')
			sleep(1)
			led.set_status('LOW')
			sleep(0.5)
			##key = keyboard.key_pressed()
			##if key !='':
				##print(key)
			#sleep(0.1)

	except KeyboardInterrupt:
		print('\033[31m\nSystem Stopped!\033[m')
		GPIO.cleanup()
