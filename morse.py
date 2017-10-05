from gpiozero import LightSensor
import datetime
import time
import RPi.GPIO as GPIO

class MorseConverter(object):
	def __init__ (self):
		self.lettertocode = {
			"A": ".-",
			"B": "-...",
			"C": "-.-.",
			"D": "-..",
			"E": ".",
			"F": "..-.",
			"G": "--.",
			"H": "....",
			"I": "..",
			"J": ".---",
			"K": "-.-",
			"L": ".-..",
			"M": "--",
			"N": "-.",
			"O": "---",
			"P": ".--.",
			"Q": "--.-",
			"R": ".-.",
			"S": "...",
			"T": "-",
			"U": "..-",
			"V": "...-",
			"W": ".--",
			"X": "-..-",
			"Y": "-.--",
			"Z": "--..",
			"1": ".----",
			"2": "..---",
			"3": "...--",
			"4": "....-",
			"5": ".....",
			"6": "-....",
			"7": "--...",
			"8": "---..",
			"9": "----.",
			"0": "-----",
			" ": "   "
		}
		
		self.codetoletter = {v: k for k, v in self.lettertocode.items()}
		
		self.chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
				 "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
				 "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7",
				 "8", "9", "0", " "]

		self.letter = ""
		self.morseCode = ""
		self.laserPin = 0
		self.ldrPin = 0
		self.brightness = 0.0
		self.ldr = None
		self.started = False
		self.dotTime = 0.0
		self.hyphenTime = 0.0
		self.spaceTime = 0.0

	def textToMorse(self, text):
		self.letter = text.upper()
		self.morseCode = ""

		if self.letter not in self.chars:
			print ("Error: Not a valid character")
			exit()

		self.morseCode += self.lettertocode[self.letter]
		
		return self.morseCode
		
	def morseToText(self, text):
		self.letter = ""
		self.morseCode = text
		
		self.letter += self.codetoletter[self.morseCode]
		
		return self.letter
		

	# SENDER
	# Takes the TXT given to it and find then length and turns it it into binary
	def lengthToBinary(self, message):
		message = len(message)
		length = '{0:08b}'.format(message)
		length = str(length)
		print('length of message: ', message)
		return length

	def setup_laser(self, pin):
		self.laserPin = pin

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.laserPin, GPIO.OUT)
		GPIO.output(self.laserPin, 0)

	def send_length(self, binary_length, multiplier):
		print ("Sending length")

		for ch in binary_length:
			if ch == '1':
				print ('1')
				GPIO.output(self.laserPin, 1)
				time.sleep(0.5 * multiplier)
				GPIO.output(self.laserPin, 0)
			elif ch == '0':
				print ('0')
				time.sleep(0.5 * multiplier)
			else:
				continue

		GPIO.output(self.laserPin, 0)

	def send_message(self, morse, multiplier):
		print ("Sending morse: " + morse)

		if morse == "   ":
			print ("Space")
			time.sleep(0.75 * multiplier)
			GPIO.output(self.laserPin, 1)
			time.sleep(0.5 * multiplier)
			GPIO.output(self.laserPin, 0)
		else:
			for ch in morse:
				if ch == ".":
					print (".")
					GPIO.output(self.laserPin, 1)
					time.sleep(0.25 * multiplier)
					GPIO.output(self.laserPin, 0)
					time.sleep(0.5 * multiplier)
				elif ch == "-":
					print ("-")
					GPIO.output(self.laserPin, 1)
					time.sleep(0.75 * multiplier)
					GPIO.output(self.laserPin, 0)
					time.sleep(0.5 * multiplier)

	def send(self, char, multiplier=1):
		morse_txt = self.textToMorse(char)
		morse_length = self.lengthToBinary(morse_txt)
		print (morse_txt)

		print ("The message will be sent in 3 seconds")
		time.sleep(3)

		GPIO.output(self.laserPin, 1)
		time.sleep(5)
		GPIO.output(self.laserPin, 0)

		self.send_length(morse_length, multiplier)
		time.sleep(1 * multiplier)
		self.send_message(morse_txt, multiplier)
		time.sleep(1 * multiplier)

	# RECEIVER
	# convert binary to length
	def message_length(integer):
		toint = int(integer, 2)
		return toint*8
		
	def setup_ldr(self, pin):
		self.ldrPin = pin
		self.ldr = LightSensor(self.ldrPin)
		
	def get_char(self, brightness=0.5, multiplier=1):
		self.dotTime = datetime.timedelta(seconds=int(0.3 * multiplier), microseconds=(1000000 * float("0." + str(str((0.3 * multiplier) - int(0.3 * multiplier))[2:]))))
		self.hyphenTime = datetime.timedelta(seconds=int(0.8 * multiplier), microseconds=(1000000 * float("0." + str(str((0.8 * multiplier) - int(0.8 * multiplier))[2:]))))
		self.spaceTime = self.hyphenTime
		self.brightness = brightness
		
		while not (self.ldr.value > self.brightness):
			if self.ldr.value > self.brightness and not self.started:
				self.started = True
			elif self.ldr.value > self.brightness and self.started:
				continue
			elif self.ldr.value < self.brightness and not self.started:
				continue
				
		receiveBin = ""
		while len(receiveBin) != 8:
			if self.ldr.value > self.brightness:
				receiveBin += "1"
				time.sleep(0.5 * multiplier)
			elif self.ldr.value < self.brightness:
				receiveBin += "0"
				time.sleep(0.5 * multiplier)
		print (receiveBin)
		receiveLen = self.message_length(receiveBin)
		print (receiveLen)
		
		time.sleep(1 * multiplier)
		
		receiveMorse = ""
		while len(receiveMorse) != receiveLen:
			time1 = datetime.datetime.now()
			if self.ldr.value > self.brightness:
				while True:
					if self.ldr.value < self.brightness:
						time2 = datetime.datetime.now()
						if (time2 - time1) < self.dotTime:
							receiveMorse += "."
							break
						elif (time2 - time1) < self.hyphenTime:
							receiveMorse += "-"
							break
			elif self.ldr.value < self.brightness:
				while True:
					if self.ldr.value > self.brightness:
						time2 = datetime.datetime.now()
						if (time2 - time1) < self.spaceTime:
							receiveMorse += "   "
							break
			time.sleep(0.5 * multiplier)
		print ("The letter is: " + self.morseToText(receiveMorse))
		time.sleep(1 * multiplier) 
