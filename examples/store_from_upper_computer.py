# Standard library imports
import sys
from time import sleep

# Third party imports
import serial

# Adafruit package imports
from adafruit_fingerprint import AdafruitFingerprint
from adafruit_fingerprint.responses import *

# Example module imports
from examples.enroll_to_upper_computer import enroll_to_upper_computer


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

    while True:
        print('\nReady to enroll a fingerprint!\n')
        template = enroll_to_upper_computer(finger)
        if template:
            print(f'Template:: {template}')
            print(
                '\nPlease type in the ID # (from 1 to 255) you want to save this finger as...')
            id = read_number()
            print(f'Storing template to flash library, with id #{id}\n')
            if store_from_upper_computer(finger=finger, template=template, page_id=id):
                print('Finished storing\n')
        else:
            print('Failed to return template')


def read_number():
    num = 0
    while num < 1 or num > 255:
        try:
            num = int(input())
        except ValueError:
            print('Please provide an integer')
        else:
            if num < 1 or num > 255:
                print('Please provide an integer in the above range')

    return num


def store_from_upper_computer(finger, template, page_id):
    # Buffer constants
    CHAR_BUFF_1 = 0x01
    CHAR_BUFF_2 = 0x02

    response = finger.down_char(buffer=CHAR_BUFF_1, template=template)
    if response is FINGERPRINT_OK:
        print('Template downloaded successfully!')
        sys.stdout.flush()
    if response is FINGERPRINT_PACKETRECEIVER:
        print('Communication error')
        return False
    if response is FINGERPRINT_TEMPLATEDOWNLOADFAIL:
        print('Template download error')
        return False

    response = finger.store(buffer=CHAR_BUFF_1, page_id=page_id)
    if response is FINGERPRINT_OK:
        print('Template stored successfully!')
        sys.stdout.flush()
        return page_id
    if response is FINGERPRINT_PACKETRECEIVER:
        print('Communication error')
        return False
    if response is FINGERPRINT_BADLOCATION:
        print('Could not store in that location')
        return False
    if response is FINGERPRINT_FLASHER:
        print('Error writing to flash')
        return False


# Expose only store function from module
__all__ = ['store_from_upper_computer']


if __name__ == '__main__':
    main()
