from bitarray import bitarray
import typing as t


def transform(bits: bitarray, transformation_rules: t.List, resize_allowed: bool = False) -> bitarray:
    if max(*transformation_rules) > len(bits):
        raise ValueError('Malformed rules')
    if len(transformation_rules) != len(bits) and not resize_allowed:
        raise ValueError('Rules does not conform with given bits (lengths are different)')

    permuted_bits = bitarray()
    for i, rule in enumerate(transformation_rules):
        permuted_bits.append(bits[rule-1])
    return permuted_bits


def extend(bits: bitarray, extension_rules: t.List):
    return transform(bits, extension_rules, resize_allowed=True)


def circular_left_shift(bits: bitarray, positions) -> bitarray:
    if positions < 0:
        raise ValueError('Positions should be positive value')
    positions %= len(bits)
    if positions == 0:
        return bits

    new_bits = bits[positions:] + bits[:positions]
    return new_bits


def circular_right_shift(bits: bitarray, positions) -> bitarray:
    if positions < 0:
        raise ValueError('Positions should be positive value')
    positions %= len(bits)
    if positions == 0:
        return bits

    new_bits = bits[-positions:] + bits[:-positions]
    return new_bits


# --------------------------------------------------------------------
def bitarr_to_hex(bits: bitarray) -> str:
    return hex(int(bits.to01(), 2))[2:].upper().zfill(int(len(bits)/4))


def hex_to_bitarr(hexstring: str) -> str:
    return ''.join([bin(int(c, 16))[2:].zfill(4) for c in hexstring])


def bitarr_to_1byte_unicode(bits: bitarray) -> str:
    res = ''
    for i in range(0, len(bits), 8):
        res += chr(int(bits[i:i+8].to01(), 2))
    return res


def byte_unicode_to_bin(text: str) -> bitarray:
    res = bitarray()
    for c in text:
        res += bitarray(bin(ord(c))[2:].zfill(8))
    return res


def pad_to_64bits_multiple(bits: bitarray) -> bitarray:
    # https://tools.ietf.org/html/rfc5652#section-6.3
    # limited implementation: padding up to 64 bits multiple
    if len(bits) % 8 != 0:
        raise ValueError("Received bit sequence that is not multiple to 8 (one byte)")
    if len(bits) % 64 == 0:
        return bits
    else:
        rest = int((64 - len(bits) % 64) / 8)
        addition = bin(rest)[2:].zfill(8) * rest  # n byte, n times ('10' '10')
        return bitarray.copy(bits) + bitarray(addition)


def remove_64_multiple_bits_padding(bits: bitarray):
    last_byte = bits[-8:].to01()
    times = int(last_byte, 2)
    if times == 0:
        return bits
    elif bits.to01().endswith(last_byte * times):
        return bits[:-8*times]
    else:
        return bits