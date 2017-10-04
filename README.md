# MorseOverLaser
Sending messages between Raspberry Pis using lasers and morse code.

## Documentation
* setup(pin) - sets up the laser that is connected to the GPIO pin number specified in the parameter (BCM format)
* send(char, time=1) - converts the character specified in the parameter into morse code and then flashes the laser in morse code, the time parameter adjusts how long it takes to send a message, the higher the value the longer it takes but this makes it more accurate
