"""Internal Exception classes used by package

These classes subclass the base Exception class

Classes
_______
MissingPortException(Exception)
SerialReadException(Exception)
UnknownConfirmationCodeException(Exception)

"""


class MissingPortException(Exception):
    """
    Exception raised when the port param is missing when instantiating
    the AdafruitFingerprin class
    """


class SerialReadException(Exception):
    """Exception raised when no data is read from the serial port"""


class UnknownConfirmationCodeException(Exception):
    """Exception raised when package content is an invalid response"""
