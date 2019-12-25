# Adafruti package imports
from adafruit_fingerprint.core import Package
from adafruit_fingerprint.exceptions import *
from adafruit_fingerprint.responses import *
from adafruit_fingerprint.utils import hexbyte_2integer_normalizer


class AdafruitFingerprint:
    def __init__(self, port=None):
        if port is None:
            raise MissingPortException(
                'No port passed for serial communication')
        self.port = port
        self.package = Package(port=port)

    def vfy_pwd(self):
        '''
        Verify module's handshaking password
        '''
        data = [0x13, 0x0, 0x0, 0x0, 0x0]
        self.package.write(data=data)
        serial_data = self.package.read()
        if len(serial_data) > 0:
            package_content = serial_data[4]
            if package_content == FINGERPRINT_PASSWORD_OK:
                return FINGERPRINT_PASSWORD_OK
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            elif package_content == FINGERPRINT_WRONG_PASSWORD:
                return FINGERPRINT_WRONG_PASSWORD
            else:
                raise UnknownConfirmationCodeException(
                    'Unknown confirmation code')
        raise SerialReadException('No data read from serial port')

    def gen_img(self):
        '''
        Detecting finger and store the detected finger image in ImageBuffer
        While returning successfull confirmation code; If there is no finger,
        Returned confirmation code would be “can’t detect finger”
        '''
        data = [0x01]
        self.package.write(data=data)
        serial_data = self.package.read()
        if len(serial_data) > 0:
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
                raise UnknownConfirmationCodeException(
                    'Unknown confirmation code')
        raise SerialReadException('No data read from serial port')

    def img_2Tz(self, buffer):
        '''
        To generate character file from the original finger image in
        ImageBuffer and store the file in CharBuffer1 or CharBuffer2
        '''
        data = [0x02, buffer]
        self.package.write(data=data)
        serial_data = self.package.read()
        if len(serial_data) > 0:
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
                raise UnknownConfirmationCodeException(
                    'Unknown confirmation code')
        raise SerialReadException('No data read from serial port')

    def reg_model(self):
        '''
        To combine information of character files from CharBuffer1 and
        CharBuffer2 and generate a template which is stroed back in both
        CharBuffer1 and CharBuffer2
        '''
        data = [0x05]
        self.package.write(data=data)
        serial_data = self.package.read()
        if len(serial_data) > 0:
            package_content = serial_data[4]
            if package_content == FINGERPRINT_OK:
                return FINGERPRINT_OK
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            elif package_content == FINGERPRINT_ENROLLMISMATCH:
                return FINGERPRINT_ENROLLMISMATCH
            else:
                raise UnknownConfirmationCodeException(
                    'Unknown confirmation code')
        raise SerialReadException('No data read from serial port')

    def up_char(self, buffer):
        '''
        To upload the character file or template of CharBuffer1/CharBuffer2
        to upper computer
        '''
        data = [0x08, buffer]
        self.package.write(data=data)

        serial_data = self.package.read()
        if len(serial_data) > 0:
            package_content = serial_data[4]
            if package_content == FINGERPRINT_OK:
                template = self.package.read_template()
                return FINGERPRINT_OK, template
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            elif package_content == FINGERPRINT_TEMPLATEUPLOADFAIL:
                return FINGERPRINT_TEMPLATEUPLOADFAIL
            else:
                raise UnknownConfirmationCodeException(
                    'Unknown confirmation code')
        raise SerialReadException('No data read from serial port')

    def down_char(self, buffer, template):
        '''
        To download character file or template from upper computer to the
        Specified buffer of Module
        '''
        data = [0x09, buffer]
        self.package.write(data=data)

        serial_data = self.package.read()
        if len(serial_data) > 0:
            package_content = serial_data[4]
            if package_content == FINGERPRINT_OK:
                self.package.write_template(data=template)
                return FINGERPRINT_OK
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            elif package_content == FINGERPRINT_TEMPLATEDOWNLOADFAIL:
                return FINGERPRINT_TEMPLATEDOWNLOADFAIL
            else:
                raise UnknownConfirmationCodeException(
                    'Unknown confirmation code')
        raise SerialReadException('No data read from serial port')

    def store(self, buffer, page_id):
        '''
        To store the template of specified buffer (Buffer1/Buffer2) at the designated
        Location (page) of Flash library
        '''
        data = [0x06, buffer, 0x00, page_id]
        self.package.write(data=data)

        serial_data = self.package.read()
        if len(serial_data) > 0:
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
                raise UnknownConfirmationCodeException(
                    'Unknown confirmation code')
        raise SerialReadException('No data read from serial port')

    def search(self, buffer, page_start, page_num):
        '''
        To search the whole finger library for the template that matches the
        One in CharBuffer1 or CharBuffer2. When found, page_id will be returned
        '''
        data = [0x04, buffer, 0x00, page_start, 0x00, page_num]
        self.package.write(data=data)

        serial_data = self.package.read()
        if len(serial_data) > 0:
            package_content = serial_data[4]
            if package_content == FINGERPRINT_OK:
                page_id = hexbyte_2integer_normalizer(
                    serial_data[5], serial_data[6])
                confidence_score = hexbyte_2integer_normalizer(
                    serial_data[7], serial_data[8])
                return FINGERPRINT_OK, page_id, confidence_score
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            elif package_content == FINGERPRINT_NOTFOUND:
                return FINGERPRINT_NOTFOUND
            else:
                raise UnknownConfirmationCodeException(
                    'Unknown confirmation code')
        raise SerialReadException('No data read from serial port')
