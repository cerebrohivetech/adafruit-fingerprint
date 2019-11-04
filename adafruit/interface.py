#!/usr/bin/python3

from adafruit.core import Package
from adafruit.exceptions import *
from adafruit.response import *


class AdafruitFingerprint:
    def __init__(self, port=None):
        if port is None:
            raise NullPortException('No port passed for serial communication')
        self.port = port
        self.package = Package(port=port)

    # verify module's handshaking password
    def vfy_pwd(self):
        data = [0x13, 0x0, 0x0, 0x0, 0x0]
        self.package.write(data=data)
        serial_data = self.package.read()
        if len(serial_data):
            package_content = serial_data[4]
            if package_content == FINGERPRINT_PASSWORD_OK:
                return FINGERPRINT_PASSWORD_OK
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            elif package_content == FINGERPRINT_WRONG_PASSWORD:
                return FINGERPRINT_WRONG_PASSWORD
            else:
                raise UnknownConfirmationCodeException('Unknown confirmation code')
        raise SerialReadException('No data read from serial port')


    # detect finger and store the detected finger image in ImageBuffer
    def gen_img(self):
        data = [0x01]
        self.package.write(data=data)
        serial_data = self.package.read()
        if len(serial_data):
            package_content = serial_data[4]
            if package_content == FINGERPRINT_OK:
                return FINGERPRINT_OK
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            elif package_content == FINGERPRINT_NOFINGER:
                return FINGERPRINT_NOFINGER
            elif package_content == FINGERPRINT_IMAGEFAIL:
                return FINGERPRINT_IMAGEFAIL
            else:
                raise UnknownConfirmationCodeException('Unknown confirmation code')
        raise SerialReadException('No data read from serial port')
        

    # generate character file from the original image in ImageBuffer
    # and store the file in CharBuff1(id:1) and CharBuff2(id:2)
    def img_2tz(self, buffer):
        data = [0x02, buffer]
        self.package.write(data=data)
        serial_data = self.package.read()
        if len(serial_data):
            package_content = serial_data[4]
            if package_content == FINGERPRINT_OK:
                return FINGERPRINT_OK
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            elif package_content == FINGERPRINT_IMAGEMESS:
                return FINGERPRINT_IMAGEMESS
            elif package_content == FINGERPRINT_FEATUREFAIL:
                return FINGERPRINT_FEATUREFAIL
            elif package_content == FINGERPRINT_INVALIDIMAGE:
                return FINGERPRINT_INVALIDIMAGE
            else:
                raise UnknownConfirmationCodeException('Unknown confirmation code')
        raise SerialReadException('No data read from serial port')

    # combine informartion stored in charBuffer1 and CharBuffer2 and
    # generate a template to be stored back in both CharBuffer1 and CharBuffer2
    def reg_model(self):
        data = [0x05]
        self.package.write(data=data, show=False)
        serial_data = self.package.read(show=False)
        if len(serial_data):
            package_content = serial_data[4]
            if package_content == FINGERPRINT_OK:
                return FINGERPRINT_OK
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            elif package_content == FINGERPRINT_ENROLLMISMATCH:
                return FINGERPRINT_ENROLLMISMATCH
            else:
                raise UnknownConfirmationCodeException('Unknown confirmation code')
        raise SerialReadException('No data read from serial port')

    def up_char(self, buffer):
        data = [0x08, buffer]
        self.package.write(data=data, show=False)

        serial_data = self.package.read(show=False)
        if len(serial_data):
            package_content = serial_data[4]
            if package_content == FINGERPRINT_OK:
                template = self.package.read_template()
                return FINGERPRINT_OK, template
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            elif package_content == FINGERPRINT_TEMPLATEUPLOADFAIL:
                return FINGERPRINT_TEMPLATEUPLOADFAIL
            else:
                raise UnknownConfirmationCodeException('Unknown confirmation code')
        raise SerialReadException('No data read from serial port')
