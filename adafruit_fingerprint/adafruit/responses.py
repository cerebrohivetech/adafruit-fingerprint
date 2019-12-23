# Reponse constants
_base = 16

# General responses
FINGERPRINT_OK = int('0x00', _base)
FINGERPRINT_PACKETRECEIVER = int('0x01', _base)

# Responses for vfy_pwd
FINGERPRINT_PASSWORD_OK = FINGERPRINT_OK
FINGERPRINT_WRONG_PASSWORD = int('0x13', _base)

# Responses for gen_img
FINGERPRINT_NOFINGER = int('0x02', _base)
FINGERPRINT_IMAGEFAIL = int('0x03', _base)


# Responses for img_2Tz
FINGERPRINT_IMAGEMESS = int('0x06', _base)
FINGERPRINT_FEATUREFAIL = int('0x07', _base)
FINGERPRINT_INVALIDIMAGE = int('0x15', _base)

# Responses for reg_model
FINGERPRINT_ENROLLMISMATCH = int('0x0a', _base)

# Responses for up_char
FINGERPRINT_TEMPLATEUPLOADFAIL = int('0x0d', _base)

# Responses for down_char
FINGERPRINT_TEMPLATEDOWNLOADFAIL = int('0x0e', _base)

# Responses for store
FINGERPRINT_BADLOCATION = int('0x0b', _base)
FINGERPRINT_FLASHER = int('0x18', _base)

# Responses for search
FINGERPRINT_NOTFOUND = int('0x09', _base)
