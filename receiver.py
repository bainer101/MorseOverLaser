from gpiozero import LightSensor
import datetime
import time
import morse

# setup the ldr
ldr = 18
ldr = LightSensor(ldr)

# set the minimum brightness the room has to be to count it as the laser being on
brightness = 0.2

# setup two lists and two variables to hold the length and morse details
morse = []
morse_str = ''

length = []
length_str = ''	

# setup variables to define the length of the message, if the length has
# been received and if the message receiving has started
message_len = 0
length_received = False
is_started = False
    
# ================================================
while True:
	# if the laser is on and the transmission hasn't begun then...
		# define the times when to receive the length and receive the message
		# set the variable to true so the message receiving has started
    if ldr.value > brightness and is_started == False:
        lengthTime = morse.Receiver.receiveLengthTime()
        messageTime = morse.Receiver.receiveMessageTime()
        is_started = True
    # if the message receiving has started...
    elif is_started:
        while True:
			# constantly get the current time
            dateSTR = morse.Receiver.currentTime()
            # if its time to receive the length and the length hasn't been received yet then...
            if dateSTR == lengthTime and length_received == False:
                time.sleep(0.2)
                # repeat this 8 times (because there are 8 digits in binary)
                for x in range(9):
					# if the laser is on and there's not 8 digits yet then...
						# add a one to the length and wait 0.5 seconds
                    if ldr.value > brightness and len(length) < 8:
                        length.append('1')
                        print('received 1')
                        time.sleep(0.5)
                    # if the laser is off and there's not 8 digits yet then...
						# add a zero to the length and wait 0.5 seconds
                    elif ldr.value < brightness and len(length) < 8:
                        length.append('0')
                        print('Received 0')
                        time.sleep(0.5)
                    # if there are 8 digits then...
						# for each digit...
							# add the digit to the length_str variable
							# convert the binary string to a number
						# set the variable to True as the length as been received
                    elif len(length) == 8:
                        for ch in length:
                            length_str = length_str + ch
                            message_len = message_len + morse.Receiver.message_length(length_str)
                        length_received = True
			# else if its time to send the message
            elif dateSTR == messageTime:
				# wait 0.2 seconds and sent the text variable to a blank string
                time.sleep(0.2)
				text = ""
                while True:
					# if the laser and on and the message isn't finished then...
						# wait 0.26 seconds
						# if the laser is still on then its a dash
						# else its a dot
						# wait 0.49 seconds
					# else if the laser is off and the message isn't finished then...
						# wait 0.26 seconds
						# if its still off then its a space between words
						# else its a space between letters
						# wait 0.49 seconds
					# else if the message is finished then...
						# convert the morse to text, output it and then exit the program
					if ldr.value > brightness and len(morse) < message_len:
						time.sleep(0.26)
						if ldr.value > brightness and len(morse) < message_len:
							text += "-"
							time.sleep(0.49)
						else:
							text += "."
							time.sleep(0.49)
					elif ldr.value < brightness and len(morse) < message_len:
						time.sleep(0.26)
						if ldr.value < brightness and len(morse) < message_len:
							text += "   "
							time.sleep(0.49)
						else:
							text += " "
							time.sleep(0.49)
					elif len(morse) == message_len:
						print morse.MorseConverter.morseToText(text)
						exit()
