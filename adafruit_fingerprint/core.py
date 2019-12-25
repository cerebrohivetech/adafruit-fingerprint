'''
From struct packing and unpacking
H - 2 bytes
I - 4 bytes
B - 1 byte
'''

import sys
from time import sleep
from struct import unpack, pack


class Package:
    CHECKSUM_LENGTH = 2
    WAIT_TIME = 1

    def __init__(self, port):
        # Set default package header contents
        self.port = port
        self.header = 0xEF01
        self.address = 0xFFFFFFFF
        self.identifier = 0x01
        self.package_head = [self.header, self.address, self.identifier]

    def read(self):
        ''' Read acknowledge package from serial port '''
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
        ''' Write the command (or instruction) package '''
        # Get package_length
        package_length = [(len(data) + self.CHECKSUM_LENGTH)]

        # Create checksum
        checksum = [sum(self.package_head[-1:] + package_length + data)]

        package_format = '!HIBH' + 'B' * len(data) + 'H'
        package = self.package_head + package_length + data + checksum
        serial_data = pack(package_format, *package)
        self.port.write(serial_data)

    def read_template(self):
        ''' Read template from serial buffer '''
        if self.port.in_waiting > 0:
            serial_data = self.port.read(self.port.in_waiting)
            template = serial_data.hex()
            return template

    def write_template(self, data):
        ''' Write template to serial buffer '''
        template = bytes.fromhex(data)
        self.port.write(template)

    def __repr__(self):
        return f'Package Header: {self.package_head}'
