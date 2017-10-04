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
		self.pin = 0

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

	def setup(self, pin):
		self.pin = pin

		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pin, GPIO.OUT)
		GPIO.output(self.pin, 0)

		GPIO.output(self.pin, 1)
		input("Press enter when the laser is aligned and you have got the brightness")
		GPIO.output(self.pin, 0)

	def send_length(self, binary_length, multiplier):
		print ("Sending length")

		for ch in binary_length:
			if ch == '1':
				print ('1')
				GPIO.output(self.pin, 1)
				time.sleep(0.5 * multiplier)
				GPIO.output(self.pin, 0)
			elif ch == '0':
				print ('0')
				time.sleep(0.5 * multiplier)
			else:
				continue

		GPIO.output(self.pin, 0)

	def send_message(self, morse, multiplier):
		print ("Sending morse: " + morse)

		if morse == "   ":
			print ("Space")
			time.sleep(0.75 * multiplier)
			GPIO.output(self.pin, 1)
			time.sleep(0.5 * multiplier)
			GPIO.output(self.pin, 0)
		else:
			for ch in morse:
				if ch == ".":
					print (".")
					GPIO.output(self.pin, 1)
					time.sleep(0.25 * multiplier)
					GPIO.output(self.pin, 0)
					time.sleep(0.5 * multiplier)
				elif ch == "-":
					print ("-")
					GPIO.output(self.pin, 1)
					time.sleep(0.75 * multiplier)
					GPIO.output(self.pin, 0)
					time.sleep(0.5 * multiplier)

	def send(self, char, multiplier=1):
		morse_txt = self.textToMorse(char)
		morse_length = self.lengthToBinary(morse_txt)
		print (morse_txt)

		print ("The message will be sent in 3 seconds")
		time.sleep(3)

		GPIO.output(self.pin, 1)
		time.sleep(5)
		GPIO.output(self.pin, 0)

		self.send_length(morse_length, multiplier)
		self.send_message(morse_txt, multiplier)

	# RECEIVER
	# convert binary to length
	def message_length(integer):
		toint = int(integer, 2)
		return toint*8
