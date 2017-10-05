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
		
		self.codetoletter = {v: k for k, v in self.lettertocode.iteritems()}
		
		self.chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K",
				 "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
				 "W", "X", "Y", "Z", "1", "2", "3", "4", "5", "6", "7",
				 "8", "9", "0", " "]
		
	def textToMorse(self, text):
		self.text = text.upper()
		self.morse = ""
		
		for ch in self.text:
			if ch not in self.chars:
				self.text = self.text.replace(ch, "")
		
		for ch in self.text:
			if ch == " ":
				continue
			else:
				self.morse += self.lettertocode[ch]
			self.morse += " "
		
		return self.morse.replace("   ", "|")
		
	def morseToText(self, text):
		self.letters = ""
		self.text = text
		self.text = self.text.split("   ")
		
		for item in self.text:
			item = str(item)
			item = item.split(" ")
			for letter in item:
				self.letters += self.codetoletter[letter]
			self.letters += " "
		
		return self.letters
		

class Sender(object):
	# Takes the TXT given to it and find then length and turns it it into binary
	def lengthToBinary(message):
		message = len(message)
		length = '{0:08b}'.format(message)
		length = str(length)
		print('length of message: ', message)
		return length
		
	# Get the time when the length will be sent
	def sendLengthTime():
		now = datetime.datetime.now()
		start1 = now + datetime.timedelta(minutes=1)
		start1 = start1.strftime("%H:%M")
		print(now)
		print('Start1: ', start1)
		return start1
	
	# Get the time when the message will be sent
	def sendMessageTime():
		now = datetime.datetime.now()
		start2 = now + datetime.timedelta(minutes=2)
		start2 = start2.strftime("%H:%M")
		print('Start2: ', start2)
		return start2
		
	# Get the current time
	def currentTime():
		return datetime.datetime.now().strftime("%H:%M")
		

class Receiver(object):
	# convert binary to length
	def message_length(integer):
		toint = int(integer, 2)
		return toint*8
	
	# Get the time when the length will be sent
	def receiveLengthTime():
		now = datetime.datetime.now()
		start1 = now + datetime.timedelta(minutes=1)
		start1 = start1.strftime("%H:%M")
		print(now)
		print('Start1: ', start1)
		return start1
	
	# Get the time when the message will be sent
	def receiveMessageTime():
		now = datetime.datetime.now()
		start2 = now + datetime.timedelta(minutes=2)
		start2 = start2.strftime("%H:%M")
		print('Start2: ', start2)
		return start2
		
	# Get the current time
	def currentTime():
		return datetime.datetime.now().strftime("%H:%M")
		
