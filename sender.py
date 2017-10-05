import time
import datetime
import RPi.GPIO as GPIO
import morse

# setup the GPIO for the laser and turn the laser off
laser = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(laser, GPIO.OUT)
GPIO.output(laser, 0)

# Function to send length of the message
def send_length(binary_length):
    print('sending length')
    
    # for each number in the length...
		# check if its a one or a zero
		# if its a one then...
			# turn on the laser to indicate its a one
		# if its a zero then...
			# turn the laser off to indicate its a zero
		# if its neither then...
			# skip it
			
    for ch in binary_length:
        if ch == '1':
            print('1')
            GPIO.output(laser, 1)
            time.sleep(0.5)
            GPIO.output(laser, 0)
        elif ch == '0':
            print('0')
            time.sleep(0.5)
        else:
            continue
    
    # turn the laser off when finished
    GPIO.output(laser, 0)


# Function to send binary message
def send_message(morse):
    print('Sending binary:', morse)
    
    # for each character in the morse code...
		# check the symbol
		# if its a dot then...
			# turn the laser on for 0.25 seconds (one unit in morse)
		# if its a space between letters then...
			# turn the laser off for 0.25 seconds (one unit in morse)
		# if its a dash then...
			# turn the laser on for 0.75 seconds (three units in morse)
		# if its a space between words then...
			# turn the laser off for 0.75 seconds (three units in morse)
	
	# after each character has been sent, do the opposite for 0.5 seconds
		# for example
		# .. is on for 0.25 seconds, off for 0.5 seconds, on for 0.25 seconds and then off for 0.5 seconds
		# this is used to indicate how long the laser has been on/off for
		
    for ch in morse:
        if ch == '.':
            print('.')
            GPIO.output(laser, 1)
            time.sleep(0.25)
            GPIO.output(laser, 0)
            time.sleep(0.5)
        elif ch == ' ':
            print('Break between letters')
            time.sleep(0.25)
            GPIO.output(laser, 1)
            time.sleep(0.5)
            GPIO.output(laser, 0)
        elif ch == '-':
			print ('-')
			GPIO.output(laser, 1)
			time.sleep(0.75)
			GPIO.output(laser, 0)
			time.sleep(0.5)
		elif ch == '|':
			print ('Break between words')
			time.sleep(0.75)
			GPIO.output(laser, 1)
			time.sleep(0.5)
			GPIO.output(laser, 0)
        else:
            continue
    
    # once its finished, turn the laser off
    GPIO.output(laser, 0)

# ==========================================================
GPIO.output(laser, 0)

# get the message to send
message_send = input("What message would you like to send? ")
# convert the text to morse code
morse_txt = morse.MorseConverter().textToMorse(message_send)
# convert the length to binary
morse_txt_length = morse.Sender.lengthToBinary(message_send)

print ('Message in morse code: ', morse_txt)

# set the times to start sending 
lengthTime = morse.Sender.sendLengthTime()
messageTime = morse.Sender.sendMessageTime()

print("The message will be sent in three seconds, stand back")
time.sleep(3)

# turn the laser on for five seconds to warm it up
GPIO.output(laser, 1)
time.sleep(5)
GPIO.output(laser, 0)

while True:
	# constantly get the current time
    dateSTR = morse.Sender.currentTime()
    
    # if the current time is the time to send the length then...
		# send the length
    if dateSTR == lengthTime:
        send_length(morse_txt_length)
    
    # if the current time is the time to send the message then...
		# send the message
		# exit the program
    if dateSTR == messageTime:
        send_message(morse_txt)
        exit()
