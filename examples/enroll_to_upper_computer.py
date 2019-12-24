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
        template = enroll_to_upper_computer(finger=finger)
        if template:
            print(f'Template:: {template}')
        else:
            print('Failed to return template')


def enroll_to_upper_computer(finger):
    # Buffer constants
    _CHAR_BUFF_1 = 0x01
    _CHAR_BUFF_2 = 0x02

    '''
    Enrolls fingerprint, but returns template to upper computer instead
    Of flash library
    '''
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
    
    response = finger.img_2Tz(buffer=_CHAR_BUFF_1)
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
    
    response = finger.img_2Tz(buffer=_CHAR_BUFF_2)
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
        return False
    elif response is FINGERPRINT_ENROLLMISMATCH:
        print('Prints did not match')
        return False
    else:
        print('Unknown Error')
        return False

    # Return template to upper computer
    response = finger.up_char(buffer=_CHAR_BUFF_2)
    if isinstance(response, tuple) and len(response) == 2 and response[0] is FINGERPRINT_OK:
        print('Template created successfully!')
        print('Enrollment done!\n')
        sys.stdout.flush()
        return response[1]
    if response is FINGERPRINT_PACKETRECEIVER:
        print('Communication error')
        return False
    if response is FINGERPRINT_TEMPLATEUPLOADFAIL:
        print('Template upload error')
        return False


# Expose only enroll function from module
__all__ = ['enroll_to_upper_computer']


if __name__ == '__main__':
    main()
