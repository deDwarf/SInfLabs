from app.DES import constants, des_key as dk
from bitarray import bitarray
import typing as t
import app.DES.bit_utils as bu
from app.DES.des_key import DESKey, Mode, KeyType


def reduce(bits: bitarray) -> bitarray:
    """
    Takes 48bit vector and reduces it`s length to 32 following the algorithm described for S-boxes.
    Algorithm in short:
    # split vector to 8 6bit vectors
    # for each such vector:
        - choose necessary S-Box: the one that is appropriate to current vector index (0 for 0, 1 for 1..);
        - calculate S-Box matrix indexes (i, j);
        - take the s-box value using indexes received in prev step and convert this decimal value to 4-bit vector;
    # concatenate received 4-bit vectors to get the final 32bit bit sequence

    :param bits: 48bit vector as bitarray object
    :return: 32bit bitarray
    """
    def get_s_box_indexes(vector_6bits: bitarray) -> t.Tuple:
        # determine row number(i): 1 and 6th bits -> convert to decimal
        i = int(vector_6bits[0:1].to01() + vector_6bits[5:6].to01(), 2)
        # determine col number(j): 2-5th bits, inclusively -> convert to decimal
        j = int(vector_6bits[1:5].to01(), 2)
        return i, j

    if len(bits) != 48:
        raise ValueError('Accepting 48bit blocks only')

    reduced_bits = bitarray()
    for v_index in range(int(48/6)):
        vector_6bits = bits[6*v_index:6*v_index + 6]
        indexes = get_s_box_indexes(vector_6bits)
        int_vector = constants.S_BOXES[v_index][indexes[0]][indexes[1]]
        vector_4bits = bitarray('{0:b}'.format(int_vector).zfill(4))
        reduced_bits += vector_4bits

    return reduced_bits


def fRK(vector_32bits: bitarray, round_: int, key: dk.DESKey) -> bitarray:
    # step1: extend to 48
    vector = bu.extend(vector_32bits, constants.EXTENSION_P_BOX)
    # step2: xor with key
    vector = key.get_round_key(round_) ^ vector
    # step3: reduce to 32 (s-boxes)
    vector = reduce(vector)
    # step4: final P box
    vector = bu.transform(vector, constants.FRK_FINAL_P_BOX)

    return vector


def algorithm(bits: bitarray, key: dk.DESKey) -> bitarray:
    """
    Does the DES for a single 64bit block

    :param bits: bitarray object representing 64bit vector. Vectors of length different from 64 are rejected
    :param key: crypto key as DESKey object
    :return: encrypted bits as bitarray object
    """
    if len(bits) != 64:
        raise ValueError('bitarray should be 64 bits length')

    bits = bu.transform(bits, constants.STARTING_PERMUTATION)
    ROUNDS = 16

    left32 = bits[:32]
    right32 = bits[32:]
    for i in range(ROUNDS):
        ri = fRK(right32, i+1, key)
        new_l = right32
        new_r = left32 ^ ri
        left32 = new_l
        right32 = new_r

        # debug
        # print('Round {}: left:{}   right:{}'.format(i+1, bu.bin_to_hex(left32), bu.bin_to_hex(right32)))

    bits = right32 + left32
    # print('After joining: {}'.format(bu.bin_to_hex(bits)))
    bits = bu.transform(bits, constants.FINAL_PERMUTATION)
    return bits


class DES:
    @staticmethod
    def encrypt(text: str, key: str) -> str:
        print('[E]Original message text: ' + text)
        key = DESKey(Mode.ENCRYPT_MODE, key, KeyType.STRING)
        result = bitarray()
        bits = bitarray()
        bits.frombytes(text.encode())
        print('[E]Original text hex:  {}, len = {}'.format(bu.bitarr_to_hex(bits), len(bits)))
        bits = bu.pad_to_64bits_multiple(bits)
        print('[E]Padded bits hex:    {}, len = {}'.format(bu.bitarr_to_hex(bits), len(bits)))
        for i in range(64, len(bits)+1, 64):
            encrypted = algorithm(bits[i-64:i], key)
            # encrypted = bu.bin_to_text(encrypted)
            result += encrypted
        print('[E]Encrypted msg hex:  ' + bu.bitarr_to_hex(result))
        print('[E]Encrypted msg text: ' + bu.bitarr_to_1byte_unicode(result))
        print('-----')
        return bu.bitarr_to_1byte_unicode(result)

    @staticmethod
    def decrypt(text: str, key: str) -> str:
        print('[D]Encrypted msg text: ' + text)
        key = DESKey(Mode.DECRYPT_MODE, key, KeyType.STRING)
        result_bits = bitarray()
        bits = bu.byte_unicode_to_bin(text)
        print('[D]Encrypted msg hex:  ' + bu.bitarr_to_hex(bits))

        for i in range(64, len(bits)+1, 64):
            decrypted_bits = algorithm(bits[i - 64:i], key)
            result_bits += decrypted_bits

        print('[D]Decrypted msg hex:  ' + bu.bitarr_to_hex(result_bits))
        result_bits = bu.remove_64_multiple_bits_padding(result_bits)
        print('[D]Decrypted msg:      ' + result_bits.tostring())
        return result_bits.tostring()
