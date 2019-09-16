#!/usr/bin/python3

import sys
import serial
from time import sleep

from adafruit.interface import AdafruitFingerprint
from adafruit.response import FINGERPRINT_PASSWORD_OK
from enroll import enroll_fingerprint


def main ():
    # attempt to connect to serial port
    try:
        port = '/dev/ttyUSB0' # USB TTL converter port
        baud_rate = '57600'
        serial_port = serial.Serial(port, baud_rate)
    except Exception as e:
        print(e)
        sys.exit()

    print('Program started...')

    # initialize sensor library with serial port connection
    finger = AdafruitFingerprint(port=serial_port)

    resp = finger.vfy_pwd()
    if resp is not FINGERPRINT_PASSWORD_OK:
        print(f'Verification error. Did not find fingerprint sensor :(')
        sys.exit()
    print('Found Fingerprint Sensor!\n')

    show_options()
    option = int(input('Enter option: '))
    print()
    while True:
        if option == 1:
            enroll_fingerprint(finger=finger)
        elif option == 2:
            print('Unavailable for now')
            pass
        elif option == 3:
            print('Unavailable for now')
            pass
        else:
            print('Please select a valid option')
            option = int(input('Enter option: '))
            print()
            continue
        show_options()
        option = int(input('Enter option: '))
        print()


def show_options():
    print('\nEnter 1 to register')
    print('Enter 2 for lecture')
    print('Enter 3 for exam')


if __name__ == '__main__':
    main()
