import datetime
import time
import RPi.GPIO as GPIO

try:
	import explorerhat
except:
	print ("Explorer HAT not detected")
	exit()

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
			"0": "-----"
		}
		
		self.codetoletter = {v: k for k, v in self.lettertocode.items()}
		
		self.chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
				 "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
				 "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7",
				 "8", "9", "0"]

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
	def setup_laser(self, pin):
		self.laserPin = pin

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.laserPin, GPIO.OUT)
		GPIO.output(self.laserPin, 0)
		GPIO.output(self.laserPin, 1)

		input("Press enter when you have aligned the laser")
		GPIO.output(self.laserPin, 0)
		input("Press enter when the laser says its searching for the light")

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
					#GPIO.output(self.laserPin, 1)
					#time.sleep(0.25 * multiplier)
					#GPIO.output(self.laserPin, 0)
					#time.sleep(0.5 * multiplier)
					GPIO.output(self.laserPin, 1)
					time.sleep(5)
					GPIO.output(self.laserPin, 0)
					time.sleep(3)
				elif ch == "-":
					print ("-")
					#GPIO.output(self.laserPin, 1)
					#time.sleep(0.75 * multiplier)
					#GPIO.output(self.laserPin, 0)
					#time.sleep(0.5 * multiplier)
					GPIO.output(self.laserPin, 1)
					time.sleep(10)
					GPIO.output(self.laserPin, 0)
					time.sleep(3)
		
		GPIO.output(self.laserPin, 1)
		time.sleep(15)
		GPIO.output(self.laserPin, 0)

	def send(self, char, multiplier=1):
		morse_txt = self.textToMorse(char)
		print (morse_txt)

		print ("The message will be sent in 3 seconds")
		time.sleep(3)

		GPIO.output(self.laserPin, 1)
		time.sleep(5)
		GPIO.output(self.laserPin, 0)

		time.sleep(5)

		self.send_message(morse_txt, multiplier)
		GPIO.output(self.laserPin, 0)		
		time.sleep(1 * multiplier)

	# RECEIVER
	# convert binary to length
	def setup_ldr(self):
		answer = ""
		
		while answer != "n":
			answer = input("Would you like to check the brightness? (y/n) ")
			
			if answer == "y":
				print (explorerhat.analog.one.read())
			elif answer != "y" and answer != "n":
				continue
		
	def get_char(self, brightness=0.5, multiplier=1):
		self.dotTime = datetime.timedelta(seconds=int(0.3 * multiplier), microseconds=(1000000 * float("0." + str(str((0.3 * multiplier) - int(0.3 * multiplier))[2:]))))
		self.hyphenTime = datetime.timedelta(seconds=int(0.8 * multiplier), microseconds=(1000000 * float("0." + str(str((0.8 * multiplier) - int(0.8 * multiplier))[2:]))))
		self.spaceTime = self.hyphenTime
		self.endTime = datetime.timedelta(seconds=6)
		self.brightness = brightness
		
		while not (explorerhat.analog.one.read() > self.brightness and self.started):
			if explorerhat.analog.one.read() > self.brightness and not self.started:
				print ("I saw the light")
				self.started = True
			elif explorerhat.analog.one.read() > self.brightness and self.started:
				continue
			elif explorerhat.analog.one.read() < self.brightness and not self.started:
				print ("Searching for the light...")
				continue
		time.sleep(5)		
		
		receiveMorse = ""
		sending = True
		while sending:
			time1 = datetime.datetime.now()
			if explorerhat.analog.one.read() > self.brightness:
				while True:
					if explorerhat.analog.one.read() < self.brightness:
						time2 = datetime.datetime.now()
						if (time2 - time1) < datetime.timedelta(seconds=7):
							print (".")
							receiveMorse += "."
							break
						elif (time2 - time1) < datetime.timedelta(seconds=12):
							print ("-")
							receiveMorse += "-"
							break
						elif (time2 - time1) < datetime.timedelta(seconds=17):
							print ("END")
							sending = False
							break
			time.sleep(0.5 * multiplier) 
		print ("The letter is: " + self.morseToText(receiveMorse))
		time.sleep(1 * multiplier) 
