from gpiozero import LightSensor
import datetime
import time
import morse

ldr = 18
ldr = LightSensor(ldr)
brightness = 0.2

morse = []
length = []
length_str = ''
morse_str = ''

message_len = 0
length_received = False
is_started = False


def int2bytes(binary_input):
    return ''.join(chr(int(binary_input[i:i + 8], 2)) for i in range(0, len(binary_input), 8))


def message_length(integer):
    toint = int(integer, 2)
    return toint*8


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

# ================================================
while True:
    if ldr.value > brightness and is_started == False:
        start_1 = set_time_1()
        start_2 = set_time_2()
        is_started = True
    elif is_started:
        while True:
            dateSTR = datetime.datetime.now().strftime("%H:%M")
            if dateSTR == start_1 and length_received == False:
                time.sleep(0.2)
                for x in range(9):
                    if ldr.value > brightness and len(length) < 8:
                        length.append('1')
                        print('received 1')
                        time.sleep(0.5)
                    elif ldr.value < brightness and len(length) < 8:
                        length.append('0')
                        print('Received 0')
                        time.sleep(0.5)
                    elif len(length) == 8:
                        for ch in length:
                            length_str = length_str + ch
                            length_received = True
                            message_len = message_len + message_length(length_str)

            elif dateSTR == start_2:
                time.sleep(0.2)
				text = ""
                while True:
					if ldr.value > brightness and len(morse) < message_len:
						time.sleep(0.26)
						if ldr.value > brightness and len(morse) < message_len:
							text += "-"
							time.sleep(0.49)
						else:
							text += "."
							time.sleep(0.49)
					elif ldr.value < brightness and len(morse) < message_len:
						isOn = False
						time.sleep(0.26)
						if ldr.value < brightness and len(morse) < message_len:
							text += " "
							time.sleep(0.49)
						else:
							time.sleep(0.49)
					elif len(morse) == message_len:
						mc = MorseConverter()
						print mc.morseToText(text)
						exit()
