"""Core module for serial communication of module data package format

This module implements methods to read and write packets in the data
package format. When communicating, the transferring and receiving of
command/data/result are all wrapped in data package format. The packets
take the shape of package to be sent and received as specified by the
adafruit fingerprint module.

Classes
________
Package
    Contain methods for serial read and write of module package

"""


from time import sleep
from struct import unpack, pack


class Package:
    """Implemets data package format for adafruit fingerprint module

    Contain methods to read and write module package data format to and
    from the serial buffer. Before every read and write, the package
    (packet to be read or written) has to be deconstructed and
    constructed respectively before the read/write operation, to be
    able to pick out the "package content" which is important to the
    AdafruitFingerprint class.

    Attributes
    __________
    port : serial.Serial
        Instance of the Serial class from the serial module. The serial
        port passed down to allow serial communication
        (Default is None)
    header : int
        Pakcage data header value (Default is 0xEF01)
    address : int
        Package data address value (Default is 0xFFFFFFFF)
    identifier : int
        Package data identifier value. Values can be 01H, 02H or 07H
    package_head : list
        a list containing package `header`, `address` and `identifier`


    Methods
    _______
    read()
        read package (packet) from the serial buffer
    write(data)
        write package (data packet) from the serail buffer
    read_template()
        read fingerprint template from the serial buffer
    write_template(data)
        write fingerprint template to the serial buffer
    """

    CHECKSUM_LENGTH = 2
    WAIT_TIME = 1

    def __init__(self, port):
        """Initialize package with serial port for serial communication

        Set default package header values

        Attributes
        __________
        header : int
            Pakcage data header value (Default is 0xEF01)
        address : int
            Package data address value (Default is 0xFFFFFFFF)
        identifier : int
            Package data identifier value. (Default is 0x01)
        package_head : list
            a list containing package `header`, `address` and `identifier`
        """

        self.port = port
        self.header = 0xEF01
        self.address = 0xFFFFFFFF
        self.identifier = 0x01
        self.package_head = [self.header, self.address, self.identifier]

    def read(self):
        """read package data (packet) from the serial buffer

        Returns
        _______
        package
            A list of integers. Unpacked via a specified format from a
            string of hex bytes
        """

        sleep(self.WAIT_TIME)
        package = []

        # Perform partial read to get package length i.e content length
        if self.port.in_waiting >= 9:
            serial_data = self.port.read(9)

            # Unpack bytes in big endian format for easy formatting
            package.extend(unpack('!HIBH', serial_data))
            package_length = package[-1]

            # Wait to read rest of package
            sleep(self.WAIT_TIME)
            if self.port.in_waiting >= package_length:
                serial_data = self.port.read(package_length)
                content_format = '!' + 'B' * \
                    (package_length - self.CHECKSUM_LENGTH) + 'H'
                package.extend(unpack(content_format, serial_data))
        return package

    def write(self, data):
        """write package data (data packet) from the serail buffer"""

        # Get package_length
        package_length = [(len(data) + self.CHECKSUM_LENGTH)]

        # Create checksum
        checksum = [sum(self.package_head[-1:] + package_length + data)]

        package_format = '!HIBH' + 'B' * len(data) + 'H'
        package = self.package_head + package_length + data + checksum
        serial_data = pack(package_format, *package)
        self.port.write(serial_data)

    def read_template(self):
        """Read fiingerprint template from serial buffer

        Returns
        _______
        template : string
            if fingerprint template is read successfully
        None
            if no fingerprint template is read from serial buffer
        """

        if self.port.in_waiting > 0:
            serial_data = self.port.read(self.port.in_waiting)
            template = serial_data.hex()
            return template
        return None

    def write_template(self, data):
        """Write fingerprint template to serial buffer"""

        template = bytes.fromhex(data)
        self.port.write(template)

    def __repr__(self):
        return f'Package Header: {self.package_head}'
