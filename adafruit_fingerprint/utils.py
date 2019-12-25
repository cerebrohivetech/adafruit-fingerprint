"""Uitility functions used by core interface

This module contains functions that are unnecessary to go in main core
classes and perform specific functions

Functions
_________
hexbyte_2integer_normalizer(first_int_byte, second_int_btye)
    Function to normalize integer bytes to a single byte

"""


def hexbyte_2integer_normalizer(first_int_byte, second_int_btye):
    """Function to normalize integer bytes to a single byte

    Transform two integer bytes to their hex byte values and normalize
    their values to a single integer

    Parameters
    __________
    first_int_byte, second_int_byte : int
        integer values to normalize (0 to 255)

    Returns
    _______
    integer: int
        Single normalized integer
    """

    first_hex = f'{hex(first_int_byte)}'.lstrip('0x')
    second_hex = f'{hex(second_int_btye)}'.lstrip('0x')
    first_hex = first_hex if len(f'{first_hex}') == 2 else f'0{first_hex}'
    second_hex = second_hex if len(f'{second_hex}') == 2 else f'0{second_hex}'
    hex_string = f'{first_hex}{second_hex}'
    integer = int(hex_string, 16)
    return integer
