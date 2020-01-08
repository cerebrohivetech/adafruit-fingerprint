"""Implements fingerprint module confirmation codes as int constants

Defined for the methods of the AdafruitFingerprint class. This
module defines the confirmation codes for interfaces of the
adafruit fingerprint module. Codes are defined as integer constants.

`H` here simply means the values are hex values. E.g ``0bH`` means
``0x0b``, and the integer value is 11.
"""


# Base to use for conversion of hex constants
_BASE = 16
"""int: Private variable used to store numerical base for conversion of
hex response contants
"""

# General responses
FINGERPRINT_OK = int('0x00', _BASE)
"""int: Success for all operations (Value is 00H)"""

FINGERPRINT_PACKETRECEIVER = int('0x01', _BASE)
"""int: Error when receiving package (Value is 01H)"""


# Responses for vfy_pwd
FINGERPRINT_PASSWORD_OK = FINGERPRINT_OK
"""int: Correct password (Value is 00H)

A `vry_pwd` response
"""

FINGERPRINT_WRONG_PASSWORD = int('0x13', _BASE)
"""int: Wrong Password (Value is 13H)

A `vry_pwd` response
"""


# Responses for gen_img
FINGERPRINT_NOFINGER = int('0x02', _BASE)
"""int: Can't detect finger (Value is 02H)

A `gen_img` response
"""

FINGERPRINT_IMAGEFAIL = int('0x03', _BASE)
"""int: Fail to collect finger (Value is 03H)

A `gen_img` response
"""


# Responses for img_2Tz
FINGERPRINT_IMAGEMESS = int('0x06', _BASE)
"""int: Fail to generate character file due to the over-disorderly
fingerprint image (Value is 06H)

A `img_2Tz` response
"""

FINGERPRINT_FEATUREFAIL = int('0x07', _BASE)
"""int: Fail to generate character file due to lackness of character
point or over-smallness of fingerprint image (Value is 07H)

A `img_2Tz` response
"""

FINGERPRINT_INVALIDIMAGE = int('0x15', _BASE)
"""int: Fail to generate the image for the lackness of valid primary
image (Value is 15H)

A `img_2Tz` response
"""


# Responses for reg_model
FINGERPRINT_ENROLLMISMATCH = int('0x0a', _BASE)
"""int: Fail to combine the character files. That’s, the character
files don’t belong to one finger (Value is 0aH)

A `reg_model` response
"""

# Responses for up_char
FINGERPRINT_TEMPLATEUPLOADFAIL = int('0x0d', _BASE)
"""int: error when uploading template (Value is 0dH)

A `up_char` response
"""


# Responses for down_char
FINGERPRINT_TEMPLATEDOWNLOADFAIL = int('0x0e', _BASE)
"""int: error when downloading template (Value is 0eH)

A `down_char` response
"""


# Responses for store and delete_char
FINGERPRINT_BADLOCATION = int('0x0b', _BASE)
"""int: (Value is 0bH)

addressing PageID is beyond the finger library (store)

fail to delete template from a location (delete_char)

A `store` and `delete_char` response
"""

FINGERPRINT_FLASHER = int('0x18', _BASE)
"""int: (Value is 18H)

error when writing to flash library

A `store` and `delete_char` response
"""


# Responses for search
FINGERPRINT_NOTFOUND = int('0x09', _BASE)
"""int: No matching print in the library (both the PageID and matching
score are 0) (Value is 09H)

A `search` response
"""


# Responses for delete
FINGERPRINT_TEMPLATEDELETEFAIL = int('0x10', _BASE)
"""int: Fail to delete templates (Value is 10H)

A `delete_char` response
"""

# Responses for empty
FINGERPRINT_TEMPLATECLEARALLFAIL = int('0x11', _BASE)
"""int: Fail to clear finger library (Value is 11H)

A `empty` response
"""
