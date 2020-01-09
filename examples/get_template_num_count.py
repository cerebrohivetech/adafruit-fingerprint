# Standard library imports
import sys

# Third party imports
import serial

# Adafruit package imports
from adafruit_fingerprint import AdafruitFingerprint
from adafruit_fingerprint.responses import *


def main():
    # Attempt to connect to serial port
    try:
        port = '/dev/ttyUSB0'  # USB TTL converter port
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

    response = get_template_num_count(finger=finger)
    if response:
        _, template_num_count = response
        print(f'Total number of templates stored is #{template_num_count}')


def get_template_num_count(finger):
    response = -1

    response = finger.template_num()
    if isinstance(response, tuple) and len(response) == 2 and response[0] is FINGERPRINT_OK:
        return True, response[1]

    if response is FINGERPRINT_PACKETRECEIVER:
        print('Communication error')
    else:
        print('Unknown Error')

    return False


__all__ = ['get_template_num_count']


if __name__ == '__main__':
    main()
