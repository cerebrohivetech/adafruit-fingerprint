"""AdafruitFingerprint core interface

Classes
_______
class AdafruitFingerprint
    Implements the core interface of the fingerprint module as methods

"""


# Adafruit imports
from adafruit_fingerprint.core import Package
from adafruit_fingerprint.exceptions import *
from adafruit_fingerprint.responses import *
from adafruit_fingerprint.utils import hexbyte_2integer_normalizer


# pylint: disable=no-else-return


class AdafruitFingerprint:
    """Interface class for adafruit fingerprint module

    This class implements the methods for interacting with the
    adafruit fingerprint module as is in the official datasheet

    Attributes
    __________
    port : serial.Serial
        Instance of the Serial class from the serial module. The serial
        port passed to allow serial communication (Default is None)
    pacakage : core.Package
        Instance of the Package class from the local core module that
        describes the complete format for communicating with the
        adafruit fingerprint module. The format describes/composes and
        receives the complete read and raw write packets

    Methods
    _______
    vfy_pwd()
        Verify module's handshaking password
    gen_img()
        Detect finger and store the image in ImageBuffer
    img_2Tz(buffer)
        Generate character file from the original finger image
    reg_model()
        Combine information of character files and generate a template
    up_char(buffer)
        To upload the character file or template to upper computer
    down_char(buffer, template)
        To download character file or template from upper computer
    store(buffer, page_id)
        To store the template of specified buffer to flash library
    search(buffer, page_start, page_num)
        To search the whole finger library for a matching template that
    """

    def __init__(self, port=None):
        if port is None:
            raise MissingPortException(
                'No port passed for serial communication')
        self.port = port
        self.package = Package(port=port)

    def vfy_pwd(self):
        """Verify module's handshaking password

        Raises
        ______
        UnknownConfirmationCodeException
            if no valid confirmation code is received from module
        SerialReadException
            if no serial data can be read from module

        Returns
        _______
        integer
            confirmation code response constant
        """

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
        """Detecting finger and store the detected finger image in
        ImageBuffer while returning successful confirmation code; If
        there is no finger, returned confirmation code would be “can’t
        detect finger”

        Raises
        ______
        UnknownConfirmationCodeException
            if no valid confirmation code is received from module
        SerialReadException
            if no serial data can be read from module

        Returns
        _______
        integer
            A confirmation code response constant
        """

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

    # pylint: disable=invalid-name
    def img_2Tz(self, buffer):
        """To generate character file from the original finger image in
        ImageBuffer and store the file in CharBuffer1 or CharBuffer2

        Parameters
        __________
        buffer : int
            one of two module CharBuffers used for template storage

        Raises
        ______
        UnknownConfirmationCodeException
            if no valid confirmation code is received from module
        SerialReadException
            if no serial data can be read from module

        Returns
        _______
        integer
            A confirmation code response constant
        """

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
        """To combine information of character files from CharBuffer1
        and CharBuffer2 and generate a template which is stroed back in
        both CharBuffer1 and CharBuffer2

        Raises
        ______
        UnknownConfirmationCodeException
            if no valid confirmation code is received from module
        SerialReadException
            if no serial data can be read from module

        Returns
        _______
        integer
            A confirmation code response constant
        """

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
        """To upload the character file or template of CharBuffer1
        or CharBuffer2 to upper computer

        Parameters
        __________
        buffer : int
            one of two module CharBuffers used for template storage

        Raises
        ______
        UnknownConfirmationCodeException
            if no valid confirmation code is received from module
        SerialReadException
            if no serial data can be read from module

        Returns
        _______
        tuple
            Confirmation code response constant `FINGERPRINT_OK`
            And fingerprint template `template`
        """

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
        """To download character file or template from upper computer
        to the Specified buffer of Module

        Parameters
        __________
        buffer : int
            one of two module CharBuffers used for template storage
        template : str
            previously generated template passed down from upper computer

        Raises
        ______
        UnknownConfirmationCodeException
            if no valid confirmation code is received from module
        SerialReadException
            if no serial data can be read from module

        Returns
        _______
        integer
            A confirmation code response constant
        """

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
        """To store the template of specified buffer (Buffer1/Buffer2)
        at the designated Location (page) of Flash library

        Parameters
        __________
        buffer : int
            one of two module CharBuffers used for template storage
        page_id : int
            designated location in module flash library (0 - 255)

        Raises
        ______
        UnknownConfirmationCodeException
            if no valid confirmation code is received from module
        SerialReadException
            if no serial data can be read from module

        Returns
        _______
        integer
            A confirmation code response constant
        """
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

    def search(self, buffer, page_start=0, page_num=255):
        """To search the whole finger library or a protion of it for
        the template that matches the One in CharBuffer1 or CharBuffer2
        When found, page_id will be returned

        Parameters
        __________
        buffer : int
            one of two module CharBuffers used for template storage
        page_start : int, optional
            location in module flash library to start search from
            (Default is 0)
        page_num : int, optional
            location in module flash library to end search
            (Default is 255)

        Raises
        ______
        UnknownConfirmationCodeException
            if no valid confirmation code is received from module
        SerialReadException
            if no serial data can be read from module

        Returns
        _______
        integer
            A confirmation code response constant
        """

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
