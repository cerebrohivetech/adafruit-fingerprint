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
        print('Please type in the ID # (from 1 to 127) you want to save this finger as...')
        id = read_number()
        print(f'Enrolling id #{id}\n')
        while not enroll_to_flash_library(finger, id):
            break

def read_number():
    num = 0
    while num < 1 or num > 127:
        try:
            num = int(input())
        except ValueError:
            print('Please provide an integer')
        else:
            if num < 1 or num > 127:
                print('Please provide an integer in the above range')

    return num


def enroll_to_flash_library(finger, id):
    CHAR_BUFF_1 = 0x01
    CHAR_BUFF_2 = 0x02
    
    print('Waiting for a valid finger to enroll\n')
    sys.stdout.flush()

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
            sys.stdout.flush()
        elif response is FINGERPRINT_IMAGEFAIL:
            print('Imaging Error')
            sys.stdout.flush()
        else:
            print('Unknown Error')
            sys.stdout.flush()
    
    response = finger.img_2Tz(buffer=CHAR_BUFF_1)
    if response is FINGERPRINT_OK:
        print('Image Converted')
        sys.stdout.flush()
    elif response is FINGERPRINT_IMAGEMESS:
        print('Image too messy')
        return response
    elif response is FINGERPRINT_PACKETRECEIVER:
        print('Communication error')
        return response
    elif response is FINGERPRINT_FEATUREFAIL:
        print('Could not find fingerprint features')
        return response
    elif response is FINGERPRINT_INVALIDIMAGE:
        print('Could not find fingerprint features')
        return response
    else:
        print('Unknown Error')
        return response

    # Ensure finger has been removed
    print('Remove finger')
    sleep(1)
    response = -1
    while (response is not FINGERPRINT_NOFINGER):
        response = finger.gen_img()

    print('\nPlace same finger again')
    sys.stdout.flush()

    # Read finger the second time
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
            sys.stdout.flush()
        elif response is FINGERPRINT_IMAGEFAIL:
            print('Imaging Error')
            sys.stdout.flush()
        else:
            print('Unknown Error')
            sys.stdout.flush()
    
    response = finger.img_2Tz(buffer=CHAR_BUFF_2)
    if response is FINGERPRINT_OK:
        print('Image Converted')
        sys.stdout.flush()
    elif response is FINGERPRINT_IMAGEMESS:
        print('Image too messy')
        return response
    elif response is FINGERPRINT_PACKETRECEIVER:
        print('Communication error')
        return response
    elif response is FINGERPRINT_FEATUREFAIL:
        print('Could not find fingerprint features')
        return response
    elif response is FINGERPRINT_INVALIDIMAGE:
        print('Could not find fingerprint features')
        return response
    else:
        print('Unknown Error')
        return response

    print('Remove finger')
    print('\nChecking both prints...\n')
    sys.stdout.flush()

    # Register model
    response = finger.reg_model()
    if response is FINGERPRINT_OK:
        print('Prints matched')
        sys.stdout.flush()
    elif response is FINGERPRINT_PACKETRECEIVER:
        print('Communication error')
        return response
    elif response is FINGERPRINT_ENROLLMISMATCH:
        print('Prints did not match')
        return response
    else:
        print('Unknown Error')
        return response

    response = finger.store(buffer=CHAR_BUFF_2, pageID=id)
    if response is FINGERPRINT_OK:
        print(f'Print stored in id #{id} of flash library\n')
        sys.stdout.flush()
        return response
    if response is FINGERPRINT_PACKETRECEIVER:
        print('Communication error')
        sys.stdout.flush()
        return response
    if response is FINGERPRINT_BADLOCATION:
        print('Could not store in that location')
        sys.stdout.flush()
        return response
    if response is FINGERPRINT_FLASHER:
        print('Error writing to flash')
        sys.stdout.flush()
        return response


# Expose only enroll function from module
__all__ = ['enroll_to_flash_library']


if __name__ == '__main__':
    main()
