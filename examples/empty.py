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

    if empty(finger=finger):
        print(f'Flash library database emptied. All templates cleared.')


def empty(finger):
    response = -1

    response = finger.empty()
    if response is FINGERPRINT_OK:
        print('Now Database is empty :)')
        sys.stdout.flush()
        return True

    if response is FINGERPRINT_PACKETRECEIVER:
        print('Communication error')
    elif response is FINGERPRINT_TEMPLATECLEARALLFAIL:
        print('Could not empty database')
    else:
        print('Unknown Error')

    return False


__all__ = ['empty']


if __name__ == '__main__':
    main()
