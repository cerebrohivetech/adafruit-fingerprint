"""AdafruitFingerprint core API

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
    """

    def __init__(self, port=None):
        """Initialize class with serial port object

        This sets up the `AdafruitFingerprint` class with the serial
        `port` object to be used for serial communication. The `port`
        object is passed down during initialization of the `Package`
        class from the `core` module (which composes this class) where
        it is actually used. The implementation of the type of serial
        object `port` must be is not strict. This is why it is left up
        to the user to select the type of serial object to be used, as
        can be seen in the examples section.

        In development, the ``pyserial`` package is used. So the
        constraints are that the serial port object must implement two
        (2) methods (a ``read`` and a ``write``); which reads and writes
        from the serial in and out-buffer of the specified port string
        used when creating the serial connection, and a property
        ``in_waiting``; which checks the in-buffer for waiting (buffered)
        incoming data, as specified in the pyserial docs. We advise you
        simply go with the pyserial package for 100% compatibility. We
        refused to be strict on this, by abstracting away the serial
        connection entirely from the user (to the core module perhaps),
        this is so as to have similiarities with the actual adafruit
        fingerprint library implemented in arduino which accepts a
        serial port connection (a hardware or software serial).

        Parameters
        __________
        port : serial.Serial
            Instance of the Serial class from the serial module. The serial
            port passed to allow serial communication (Default is None)

        Attributes
        __________
        package : core.Package
            Instance of the `Package` class from the local `core` module
            that describes the complete format for communicating with the
            adafruit fingerprint module over serial communication. The
            format describes and composes, and receives and sends the
            complete read and raw write packets
        """

        if port is None:
            raise MissingPortException(
                'No port passed for serial communication')
        self.package = Package(port=port)

    def vfy_pwd(self):
        """Verify module's handshaking password

        Raises
        ______
        UnknownConfirmationCodeException
            if no valid confirmation code is received from module
        SerialReadException
            if no serial data can be read from buffer (from module)

        Returns
        _______
        int
            Confirmation code (A response object)

        Note
        ____
        This has to be the first method to be called on any created
        instance of this class. It also serves as a checker for proper
        hardware connections as it first tries to establish
        communication with the connected module
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
        """Try detecting finger and store the detected finger image in
        ImageBuffer while returning successful confirmation code; If
        there is no finger, returned confirmation code would be “can’t
        detect finger”.

        Raises
        ______
        UnknownConfirmationCodeException
            if no valid confirmation code is received from module
        SerialReadException
            if no serial data can be read from buffer (from module)

        Returns
        _______
        int
            Confirmation code (A response object)
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
        ImageBuffer and store the file in CharBuffer1 or CharBuffer2.

        Parameters
        __________
        buffer : int
            one of two module CharBuffers used for template storage

        Raises
        ______
        UnknownConfirmationCodeException
            if no valid confirmation code is received from module
        SerialReadException
            if no serial data can be read from buffer (from module)

        Returns
        _______
        int
            Confirmation code (A response object)
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
        both CharBuffer1 and CharBuffer2.

        Raises
        ______
        UnknownConfirmationCodeException
            if no valid confirmation code is received from module
        SerialReadException
            if no serial data can be read from buffer (from module)

        Returns
        _______
        int
            Confirmation code (A response object)
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
        or CharBuffer2 to upper computer.

        Parameters
        __________
        buffer : int
            one of two module CharBuffers used for template storage

        Raises
        ______
        UnknownConfirmationCodeException
            if no valid confirmation code is received from module
        SerialReadException
            if no serial data can be read from buffer (from module)

        Returns
        _______
        tuple
            On success. Confirmation code (A response object)
            and fingerprint template `template`
        int
            On failure. Confirmation code (A response object)
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
        to the Specified buffer of Module.

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
            if no serial data can be read from buffer (from module)

        Returns
        _______
        int
            Confirmation code (A response object)
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
        at the designated Location (page) of Flash library.

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
            if no serial data can be read from buffer (from module)

        Returns
        _______
        int
            Confirmation code (A response object)
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
        When found, page_id will be returned.

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
            if no serial data can be read from buffer (from module)

        Returns
        _______
        tuple
            On success. Confirmation code (A response object),
            `page_id` where template was fonud, and the confidence score
        int
            On failure. Confirmation code (A response object)
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

    def delete_char(self, page_id, num=1):
        """To delete a segment (n) of templates of Flash library started
        from the specified location (or Page_id).

        Parameters
        __________
        page_id : int
            location in module flash library to start delete from
        num : int
            number of templates to be deleted from module flash library
            (Default is 1)

        Raises
        ______
        UnknownConfirmationCodeException
            if no valid confirmation code is received from module
        SerialReadException
            if no serial data can be read from buffer (from module)

        Returns
        _______
        int
            Confirmation code (A response object)
        """

        data = [0x0c, 0x00, page_id, 0x00, num]
        self.package.write(data=data)

        serial_data = self.package.read()
        if len(serial_data) > 0:
            package_content = serial_data[4]
            if package_content == FINGERPRINT_OK:
                return FINGERPRINT_OK
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            elif package_content == FINGERPRINT_TEMPLATEDELETEFAIL:
                return FINGERPRINT_TEMPLATEDELETEFAIL
            elif package_content == FINGERPRINT_BADLOCATION:
                return FINGERPRINT_BADLOCATION
            elif package_content == FINGERPRINT_FLASHER:
                return FINGERPRINT_FLASHER
            else:
                raise UnknownConfirmationCodeException(
                    'Unknown confirmation code')
        raise SerialReadException('No data read from serial port')

    def empty(self):
        """To delete all the templates in the Flash library

        Raises
        ______
        UnknownConfirmationCodeException
            if no valid confirmation code is received from module
        SerialReadException
            if no serial data can be read from buffer (from module)

        Returns
        _______
        int
            Confirmation code (A response object)
        """

        data = [0x0d]
        self.package.write(data=data)

        serial_data = self.package.read()
        if len(serial_data) > 0:
            package_content = serial_data[4]
            if package_content == FINGERPRINT_OK:
                return FINGERPRINT_OK
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            elif package_content == FINGERPRINT_TEMPLATECLEARALLFAIL:
                return FINGERPRINT_TEMPLATECLEARALLFAIL
            else:
                raise UnknownConfirmationCodeException(
                    'Unknown confirmation code')
        raise SerialReadException('No data read from serial port')

    def template_num(self):
        """To read the current valid template number of the Module

        Raises
        ______
        UnknownConfirmationCodeException
            if no valid confirmation code is received from module
        SerialReadException
            if no serial data can be read from buffer (from module)

        Returns
        _______
        Returns
        _______
        tuple
            On success. Confirmation code (A response object),
            template number count in flash library
        int
            On failure. Confirmation code (A response object)
        """

        data = [0x1d]
        self.package.write(data=data)

        serial_data = self.package.read()
        if len(serial_data) > 0:
            package_content = serial_data[4]
            if package_content == FINGERPRINT_OK:
                template_num = hexbyte_2integer_normalizer(
                    serial_data[5], serial_data[6])
                return FINGERPRINT_OK, template_num
            elif package_content == FINGERPRINT_PACKETRECEIVER:
                return FINGERPRINT_PACKETRECEIVER
            else:
                raise UnknownConfirmationCodeException(
                    'Unknown confirmation code')
        raise SerialReadException('No data read from serial port')
