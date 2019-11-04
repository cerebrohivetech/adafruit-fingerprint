
base = 16

# general response on failure to read any serial data
FINGERPRINT_PACKETRECEIVER = int('0x01', base)

# vfy_pwd responses
FINGERPRINT_PASSWORD_OK = int('0x00', base)
FINGERPRINT_WRONG_PASSWORD = int('0x13', base)

# gen_img responses
FINGERPRINT_OK = int('0x00', base)
FINGERPRINT_NOFINGER = int('0x02', base)
FINGERPRINT_IMAGEFAIL = int('0x03', base)

# img_2Tz responses
FINGERPRINT_OK = int('0x00', base)
FINGERPRINT_IMAGEMESS = int('0x06', base)
FINGERPRINT_FEATUREFAIL = int('0x07', base)
FINGERPRINT_INVALIDIMAGE = int('0x15', base)

# reg_model responses
FINGERPRINT_ENROLLMISMATCH = int('0x0a', base)

# up_char response
FINGERPRINT_TEMPLATEUPLOADFAIL = int('0x0d', base)
