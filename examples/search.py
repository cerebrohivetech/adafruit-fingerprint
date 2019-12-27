# Standard library imports
import sys
from time import sleep

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

    print('\nWaiting for valid finger!\n')
    while True:
        response = search(finger=finger, page_id=1, page_num=255)
        if response:
            id, confidence = response
            print(f'Found ID #{id}', end='')
            print(f' with confidence of {confidence}\n')
        sleep(0.1)  # Don't run at full speed


def search(finger, page_id, page_num):
    # Buffer constants
    CHAR_BUFF_1 = 0x01
    CHAR_BUFF_2 = 0x02

    # Read finger the first time
    response = -1
    while response is not FINGERPRINT_OK:
        response = finger.gen_img()
        if response is FINGERPRINT_OK:
            print('Image taken')
            sys.stdout.flush()
        elif response is FINGERPRINT_NOFINGER:
            print('waiting...')
            sys.stdout.flush()
        elif response is FINGERPRINT_PACKETRECEIVER:
            print('Communication error')
            return False
        elif response is FINGERPRINT_IMAGEFAIL:
            print('Imaging Error')
            return False
        else:
            print('Unknown Error')
            return False

    response = finger.img_2Tz(buffer=CHAR_BUFF_1)
    if response is FINGERPRINT_OK:
        print('Image Converted')
        sys.stdout.flush()
    elif response is FINGERPRINT_IMAGEMESS:
        print('Image too messy')
        return False
    elif response is FINGERPRINT_PACKETRECEIVER:
        print('Communication error')
        return False
    elif response is FINGERPRINT_FEATUREFAIL:
        print('Could not find fingerprint features')
        return False
    elif response is FINGERPRINT_INVALIDIMAGE:
        print('Could not find fingerprint features')
        return False
    else:
        print('Unknown Error')
        return False

    response = finger.search(
        buffer=CHAR_BUFF_1, page_start=page_id, page_num=page_num)
    if isinstance(response, tuple) and len(response) == 3 and response[0] is FINGERPRINT_OK:
        print('Found a print match!\n')
        return response[1], response[2]
    if response is FINGERPRINT_PACKETRECEIVER:
        print('Communication error\n')
        return False
    if response is FINGERPRINT_NOTFOUND:
        print('Did not find a match\n')
        return False


# Expose only search from module
__all__ = ['search']


if __name__ == '__main__':
    main()
