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
		
		return self.morse
		
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
		
