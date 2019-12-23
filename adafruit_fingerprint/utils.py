def hexbyte_2integer_normalizer(first_2byte, second_2btye):
    first = f'{hex(first_2byte)}'.lstrip('0x')
    second = f'{hex(second_2btye)}'.lstrip('0x')
    first = first if len(f'{first}') == 2 else f'0{first}'
    second = second if len(f'{second}') == 2 else f'0{second}'
    hex_string = f'{first}{second}'
    integer = int(hex_string, 16)
    return integer