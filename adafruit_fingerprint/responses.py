"""Implements fingerprint module confirmation codes as constants

Defined for the methods of the AdafruitFingerprint class. This
module defines the confirmation codes for interfaces of the
adafruit fingerprint module. Codes are defined as integer constants.

Objects
_______
_BASE: int
    base to use for conversion of hex response contants

FINGERPRINT_OK : int
    multi-method response: Success for all operations (Value is 00H)

FINGERPRINT_PACKETRECEIVER : int
    multi-method response: Error when receiving package (Value is 01H)

FINGERPRINT_PASSWORD_OK : int
    vry_pwd response: Correct password (Value is 00H)

FINGERPRINT_WRONG_PASSWORD : int
    vry_pwd response: Wrong Password (Value is 13H)

FINGERPRINT_NOFINGER : int
    gen_img response: Can't detect finger (Value is 02H)

FINGERPRINT_IMAGEFAIL : int
    gen_img response: fail to collect finger (Value is 03H)

FINGERPRINT_IMAGEMESS : int
    img_2Tz response: fail to generate character file due to the
    over-disorderly fingerprint image (Value is 06H)

FINGERPRINT_FEATUREFAIL : int
    img_2Tz response: fail to generate character file due to lackness
    of character point or over-smallness of fingerprint image
    (Value is 07H)

FINGERPRINT_INVALIDIMAGE : int
    img_2Tz response: fail to generate the image for the lackness of
    valid primary image (Value is 15H)

FINGERPRINT_ENROLLMISMATCH : int
    reg_model: fail to combine the character files. That’s, the
    character files don’t belong to one finger (Value is 0aH)

FINGERPRINT_TEMPLATEUPLOADFAIL : int
    up_char response: error when uploading template (Value is 0dH)

FINGERPRINT_TEMPLATEDOWNLOADFAIL : int
    up_char response: error when downloading template (Value is 0eH)

FINGERPRINT_BADLOCATION : int
    store response: addressing PageID is beyond the finger library
    (Value is 0bH)

FINGERPRINT_FLASHER : int
    store response: error when writing to flash library (Value is 18H)

FINGERPRINT_NOTFOUND : int
    search response: No matching print in the library (both the PageID
    and matching score are 0) (Value is 09H)
    
"""


# Base to use for conversion of hex constants
_BASE = 16

# General responses
FINGERPRINT_OK = int('0x00', _BASE)
FINGERPRINT_PACKETRECEIVER = int('0x01', _BASE)

# Responses for vfy_pwd
FINGERPRINT_PASSWORD_OK = FINGERPRINT_OK
FINGERPRINT_WRONG_PASSWORD = int('0x13', _BASE)

# Responses for gen_img
FINGERPRINT_NOFINGER = int('0x02', _BASE)
FINGERPRINT_IMAGEFAIL = int('0x03', _BASE)

# Responses for img_2Tz
FINGERPRINT_IMAGEMESS = int('0x06', _BASE)
FINGERPRINT_FEATUREFAIL = int('0x07', _BASE)
FINGERPRINT_INVALIDIMAGE = int('0x15', _BASE)

# Responses for reg_model
FINGERPRINT_ENROLLMISMATCH = int('0x0a', _BASE)

# Responses for up_char
FINGERPRINT_TEMPLATEUPLOADFAIL = int('0x0d', _BASE)

# Responses for down_char
FINGERPRINT_TEMPLATEDOWNLOADFAIL = int('0x0e', _BASE)

# Responses for store
FINGERPRINT_BADLOCATION = int('0x0b', _BASE)
FINGERPRINT_FLASHER = int('0x18', _BASE)

# Responses for search
FINGERPRINT_NOTFOUND = int('0x09', _BASE)
