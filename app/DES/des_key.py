from bitarray import bitarray
from enum import Enum
from app.DES import constants
from app.DES.bit_utils import transform, circular_left_shift, hex_to_bitarr


class Mode(Enum):
    ENCRYPT_MODE = 0
    DECRYPT_MODE = 1


class KeyType(Enum):
    BASE16_INTEGER = 0
    STRING = 1


class DESKey:
    def __init__(self, mode, key, key_type: KeyType = KeyType.STRING):
        if mode not in (Mode.ENCRYPT_MODE, Mode.DECRYPT_MODE):
            raise ValueError("Unrecognized mode")

        if key_type == KeyType.BASE16_INTEGER:
            self.key = hex_to_bitarr(key)
        elif key_type == KeyType.STRING:
            self.key = ''.join([bin(ord(c))[2:].zfill(8) for c in key])
        else:
            raise ValueError("Unsupported keyType: {}. Supported types: STRING, BASE16_INTEGER")

        if len(self.key) != 64:
            raise ValueError("Expected 64bit length key, received {}".format(len(self.key)))

        self.mode = mode
        self.round_keys = self._generate_round_keys()

    def _generate_round_keys(self):
        res = []
        key_bits = bitarray(self.key)

        key_bits = transform(key_bits, constants.KEY_REDUCE_TO_56_P_BOX, resize_allowed=True)
        ci = key_bits[:28]
        di = key_bits[28:]
        for i in range(16):
            ci = circular_left_shift(ci, constants.SHIFT_BOX[i])
            di = circular_left_shift(di, constants.SHIFT_BOX[i])
            bits = ci + di
            round_key = transform(bits, constants.KEY_REDUCE_TO_48_P_BOX, resize_allowed=True)
            res.append(round_key)

        return res

    def get_round_key(self, round_num) -> bitarray:
        """
        Returns requested round`s key

        :param round_num: round num, from 1 to 16
        :return: round key
        """
        if round_num > 16 or round_num <= 0:
            raise ValueError('There can be only 16 rounds: 1 to 16')

        if self.mode == Mode.ENCRYPT_MODE:
            return self.round_keys[round_num - 1]
        elif self.mode == Mode.DECRYPT_MODE:
            return self.round_keys[- round_num]

