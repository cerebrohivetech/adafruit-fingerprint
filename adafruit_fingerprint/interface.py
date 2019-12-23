#!/usr/bin/python3

from adafruit.core import Package
from adafruit.exceptions import *
from adafruit.response import *
from adafruit.utils import hexbyte_2integer_normalizer


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


    # to upload the character file or template of CharBuffer1/CharBuffer2 to upper computer
    def up_char(self, buffer):
        data = [0x08, buffer]
        self.package.write(data=data, show=True)

        serial_data = self.package.read(show=True)
        if len(serial_data):
            package_content = serial_data[4]
            if package_content == FINGERPRINT_OK:
                template = self.package.read_template(show=True)
                return FINGERPRINT_OK, template
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            elif package_content == FINGERPRINT_TEMPLATEUPLOADFAIL:
                return FINGERPRINT_TEMPLATEUPLOADFAIL
            else:
                raise UnknownConfirmationCodeException('Unknown confirmation code')
        raise SerialReadException('No data read from serial port')

    # to download character file or template from upper computer to the specified
    # buffer of Module
    def down_char(self, buffer, template):
        data = [0x09, buffer]
        self.package.write(data=data, show=True)

        serial_data = self.package.read(show=True)
        if len(serial_data):
            package_content = serial_data[4]
            if package_content == FINGERPRINT_OK:
                self.package.write_template(data=template, show=True)
                return FINGERPRINT_OK
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            elif package_content == FINGERPRINT_TEMPLATEDOWNLOADFAIL:
                return FINGERPRINT_TEMPLATEDOWNLOADFAIL
            else:
                raise UnknownConfirmationCodeException('Unknown confirmation code')
        raise SerialReadException('No data read from serial port')

    # to store the template of specified buffer (Buffer1/Buffer2) at the designated
    # location of Flash library
    def store(self, buffer, page):
        data = [0x06, buffer, 0x00, page]
        self.package.write(data=data, show=True)

        serial_data = self.package.read(show=True)
        if len(serial_data):
            package_content = serial_data[4]
            if package_content == FINGERPRINT_OK:
                return FINGERPRINT_OK
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            elif package_content == FINGERPRINT_BADLOCATION:
                return FINGERPRINT_BADLOCATION
            elif package_content == FINGERPRINT_FLASHER:
                return FINGERPRINT_FLASHER
            else:
                raise UnknownConfirmationCodeException('Unknown confirmation code')
        raise SerialReadException('No data read from serial port')

    # to search the whole finger library for the template that matches the one in
    # CharBuffer1 or CharBuffer2. When found, PageID will be returned
    def search(self, buffer, page_start, page_num):
        data = [0x04, buffer, 0x00, page_start, 0x00, page_num]
        self.package.write(data=data, show=True)

        serial_data = self.package.read(show=True)
        if len(serial_data):
            package_content = serial_data[4]
            if package_content == FINGERPRINT_OK:
                page = hexbyte_2integer_normalizer(serial_data[5], serial_data[6])
                confidence_score = hexbyte_2integer_normalizer(serial_data[7], serial_data[8])
                return FINGERPRINT_OK, page, confidence_score
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            elif package_content == FINGERPRINT_NOTFOUND:
                return FINGERPRINT_NOTFOUND
            else:
                raise UnknownConfirmationCodeException('Unknown confirmation code')
        raise SerialReadException('No data read from serial port')
