import sys, binascii
from time import sleep
from struct import unpack, pack

# H - 2 bytes
# I - 4 bytes
# B - 1 byte


class Package:
    CHECKSUM_LENGTH = 2

    def __init__(self, port):
        # default package header contents
        self.port = port
        self.header = 0xEF01
        self.address = 0xFFFFFFFF
        self.identifier = 0x01
        self.package_head = [self.header, self.address, self.identifier]

    # read acknowledge package from serial port
    def read(self, show=None):
        sleep(1) # wait a second
        package = []

        # perform partial read to get package length i.e content length
        if self.port.in_waiting >= 9:
            serial_data = self.port.read(9)
            package.extend(unpack('!HIBH', serial_data))
            package_length = package[-1]

            # wait a second and read the rest of the package
            sleep(1)
            if self.port.in_waiting >= package_length:
                serial_data = self.port.read(package_length)
                content_format = '!' + 'B' * (package_length - self.CHECKSUM_LENGTH) + 'H'
                package.extend(unpack(content_format, serial_data))
        if show: print(f'read: {package}')
        if show: print(f'read: {pack("!HIBH"+content_format.lstrip("!"), *package)}')
        return package


    # write the command package
    def write(self, data, show=None):
        # get package_length
        package_length =  [(len(data) + self.CHECKSUM_LENGTH)]

        # create checksum
        checksum = [sum(self.package_head[-1:] + package_length + data)]

        package_format = '!HIBH' + 'B' * len(data) + 'H'
        package = self.package_head + package_length + data + checksum
        serial_data = pack(package_format, *package)
        if show: print(f'write: {package}')
        if show: print(f'write: {serial_data}')
        self.port.write(serial_data)

    def read_template(self):
        sleep(1)
        if self.port.in_waiting > 0:
            serial_data = self.port.read(self.port.in_waiting)
            t = binascii.hexlify(serial_data)
            # print(serial_data)
            # print(t)
            return t.decode()
            # sys.exit('Ended here')
