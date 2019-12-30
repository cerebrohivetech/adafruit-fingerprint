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

    while True:
        print('\nPlease type in the ID # (from 1 to 255) you want to delete...\n')
        id = read_number()
        print(f'Deleting ID #{id}\n')
        if delete(finger=finger, page_id=id, num=1):
            print(f'Fingerprint at ID #{id} has been successfully deleted.')


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


def delete(finger, page_id, num):
    response = -1

    response = finger.delete_char(page_id=page_id, num=num)
    if response is FINGERPRINT_OK:
        print('Deleted')
        sys.stdout.flush()
        return page_id
    elif response is FINGERPRINT_PACKETRECEIVER:
        print('Communication error')
    elif response is FINGERPRINT_TEMPLATEDELETEFAIL:
        print('Could not delete')
    elif response is FINGERPRINT_BADLOCATION:
        print('Could not delete in that location')
    elif response is FINGERPRINT_FLASHER:
        print('Error writing to flash')
    else:
        print('Unknown Error')

    return False


__all__ = ['delete']


if __name__ == '__main__':
    main()
