import time
import datetime
import RPi.GPIO as GPIO
import morse

laser = 2
GPIO.setmode(GPIO.BCM)
GPIO.setup(laser, GPIO.OUT)
GPIO.output(laser, 0)

length_sent = False


# Takes in a CMD txt input
def user_input():
    text = input("What message would you like to send? : ")
    return text

# Takes the TXT given to it and find then length and turns it it into binary
def message_length_to_binary(message):
    message = len(message)
    length = '{0:08b}'.format(message)
    length = str(length)
    print('length of message: ', message)
    return length


# Warns the user to stay back from the laser
def warn():
    print("The message will be sent in three seconds, stand back")
    time.sleep(3)


# send a indicator signal to the receiver
def indicate():
    GPIO.output(laser, 1)
    time.sleep(5)
    GPIO.output(laser, 0)


# Function to send length of the message
def send_length(binary_length):
    print('sending length')
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
    GPIO.output(laser, 0)


# Function to send binary message
def send_message(morse):
    print('Sending binary:', morse)
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
    GPIO.output(laser, 0)


def set_time_1():
    now = datetime.datetime.now()
    start1 = now + datetime.timedelta(minutes=1)
    start1 = start1.strftime("%H:%M")
    print(now)
    print('Start1: ', start1)
    return start1


def set_time_2():
    now = datetime.datetime.now()
    start2 = now + datetime.timedelta(minutes=2)
    start2 = start2.strftime("%H:%M")
    print('Start2: ', start2)
    return start2

# ==========================================================
GPIO.output(laser, 0)

message_send = user_input()
morse_converter = morse.MorseConverter()
morse_txt = morse_converter.textToMorse(message_send).replace("   ", "|")
morse_txt_length = message_length_to_binary(message_send).replace("   ", "|")
print ('Message in morse code: ', morse_txt)

start_1 = set_time_1()
start_2 = set_time_2()

warn()
indicate()

while True:
    dateSTR = datetime.datetime.now().strftime("%H:%M")
    if dateSTR == start_1 and length_sent == False:
        send_length(morse_txt_length)
        length_sent = True
    if dateSTR == start_2:
        send_message(morse_txt)
        exit()
