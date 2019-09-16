import sys
from time import sleep


from adafruit.exceptions import *
from adafruit.response import *


CHAR_BUFF_1 = 0x01
CHAR_BUFF_2 = 0x02


def enroll_fingerprint(finger):
    print('\nPlace your finger')
    sys.stdout.flush()

    # read finger the first time
    resp = -1
    while resp is not FINGERPRINT_OK:
        resp = finger.gen_img()
        sleep(0.1)
        if resp is FINGERPRINT_OK:
            print('Image taken')
            sys.stdout.flush() 
        elif resp is FINGERPRINT_NOFINGER:
            print('waiting...')
            sys.stdout.flush()
        elif resp is FINGERPRINT_PACKETRECEIVER:
            print('Communication error')
            # sys.exit()
            return False
        elif resp is FINGERPRINT_IMAGEFAIL:
            print('Imaging Error')
            # sys.exit()
            return False
        else:
            print('Unknown Error')
            # sys.exit()
            return False
    
    resp = finger.img_2tz(buffer_id=CHAR_BUFF_1)
    if resp is FINGERPRINT_OK:
        print('Image Converted')
        sys.stdout.flush() 
    elif resp is FINGERPRINT_IMAGEMESS:
        print('Image too messy')
        # sys.exit()
        return False
    elif resp is FINGERPRINT_PACKETRECEIVER:
        print('Communication error')
        # sys.exit()
        return False
    elif resp is FINGERPRINT_FEATUREFAIL:
        print('Could not find fingerprint features')
        # sys.exit()
        return False
    elif resp is FINGERPRINT_INVALIDIMAGE:
        print('Could not find fingerprint features')
        # sys.exit()
        return False
    else:
        print('Unknown Error')
        # sys.exit()
        return False

    # Ensure finger has been removed
    print('Remove finger')
    sleep(2)
    resp = -1
    while (resp is not FINGERPRINT_NOFINGER):
        resp = finger.gen_img()

    print('\nPlace that same finger again')
    sys.stdout.flush()

    # read finger the second time
    resp = -1
    while resp is not FINGERPRINT_OK:
        resp = finger.gen_img()
        sleep(0.1)
        if resp is FINGERPRINT_OK:
            print('Image taken')
            sys.stdout.flush() 
        elif resp is FINGERPRINT_NOFINGER:
            print('waiting...')
            sys.stdout.flush()
        elif resp is FINGERPRINT_PACKETRECEIVER:
            print('Communication error')
            # sys.exit()
            return False
        elif resp is FINGERPRINT_IMAGEFAIL:
            print('Imaging Error')
            # sys.exit()
            return False
        else:
            print('Unknown Error')
            # sys.exit()
            return False
    
    resp = finger.img_2tz(buffer_id=CHAR_BUFF_2)
    sleep(0.1)
    if resp is FINGERPRINT_OK:
        print('Image Converted')
        sys.stdout.flush() 
    elif resp is FINGERPRINT_IMAGEMESS:
        print('Image too messy')
        # sys.exit()
        return False
    elif resp is FINGERPRINT_PACKETRECEIVER:
        print('Communication error')
        # sys.exit()
        return False
    elif resp is FINGERPRINT_FEATUREFAIL:
        print('Could not find fingerprint features')
        # sys.exit()
        return False
    elif resp is FINGERPRINT_INVALIDIMAGE:
        print('Could not find fingerprint features')
        # sys.exit()
        return False
    else:
        print('Unknown Error')
        # sys.exit()
        return False

    print('Remove finger')
    print('\nChecking both prints...\n')
    sys.stdout.flush()

    # Register model
    resp = finger.reg_model()
    sleep(0.1)
    if resp is FINGERPRINT_OK:
        print('Prints matched')
        sys.stdout.flush()
    if resp is FINGERPRINT_PACKETRECEIVER:
        print('Communication error')
        # sys.exit()
        return False
    if resp is FINGERPRINT_ENROLLMISMATCH:
        print('Prints did not match')
        # sys.exit()
        return False
    
    print('Enrollment done!\n')
    sys.stdout.flush()
