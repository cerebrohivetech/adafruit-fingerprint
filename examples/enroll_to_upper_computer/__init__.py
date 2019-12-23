# Standard library imports
import sys


# Third party imports
import serial


# Adafruit package imports
from adafruit_fingerprint import AdafruitFingerprint
from adafruit_fingerprint.responses import *


# Enroll package imports
from examples.enroll_to_upper_computer.enroll import enroll_to_upper_computer


# Attempt to connect to serial port
try:
    port = '/dev/ttyUSB0' # USB TTL converter port
    baud_rate = '57600'
    serial_port = serial.Serial(port, baud_rate)
except Exception as e:
    print(e)
    sys.exit()

# Initialize sensor library with serial port connection
finger = AdafruitFingerprint(port=serial_port)

response = finger.vfy_pwd()
if response is not FINGERPRINT_PASSWORD_OK:
    print('Did not find fingerprint sensor :(')
    sys.exit()
print('Found Fingerprint Sensor!\n')

while True:
    print('\nReady to enroll a fingerprint!\n')
    template = enroll_to_upper_computer(finger)
    if template:
        print(f'Template:: {template}')
    else:
        print('Failed to return template')
