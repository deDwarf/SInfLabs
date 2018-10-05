from unittest import TestCase
from app.DES.des_key import des_key as dk
from app.DES.bit_utils import bitarr_to_hex

HEX_KEY = 'AABB09182736CCDD'
BINARY_KEY = '1010101010111011000010010001100000100111001101101100110011011101'
HEX_ROUND_KEYS = [
    '194CD072DE8C',
    '4568581ABCCE',
    '06EDA4ACF5B5',
    'DA2D032B6EE3',
    '69A629FEC913',
    'C1948E87475E',
    '708AD2DDB3C0',
    '34F822F0C66D',
    '84BB4473DCCC',
    '02765708B5BF',
    '6D5560AF7CA5',
    'C2C1E96A4BF3',
    '99C31397C91F',
    '251B8BC717D0',
    '3330C5D9A36D',
    '181C5D75C66D'
]


class TestDESKey(TestCase):
    def test_generated_keys(self):
        key_obj = dk.DESKey(dk.Mode.ENCRYPT_MODE, HEX_KEY, key_type=dk.KeyType.BASE16_INTEGER)
        self.assertEqual(key_obj.key, BINARY_KEY)

        for i, val in enumerate(key_obj.round_keys):
            print('Round {0:2d}: {1}'.format(i + 1, bitarr_to_hex(val)))
            print('Expected: {}'.format(HEX_ROUND_KEYS[i]))

        self.assertEqual([bitarr_to_hex(c) for c in key_obj.round_keys], HEX_ROUND_KEYS)

    def test_get_round_key(self):
        key_obj = dk.DESKey(dk.Mode.ENCRYPT_MODE, HEX_KEY, key_type=dk.KeyType.BASE16_INTEGER)

        self.assertEqual(key_obj.get_round_key(1), key_obj.round_keys[0])
        self.assertEqual(key_obj.get_round_key(16), key_obj.round_keys[15])
        self.assertEqual(key_obj.get_round_key(4), key_obj.round_keys[3])

        key_obj = dk.DESKey(dk.Mode.DECRYPT_MODE, HEX_KEY, key_type=dk.KeyType.BASE16_INTEGER)

        self.assertEqual(key_obj.get_round_key(1), key_obj.round_keys[15])
        self.assertEqual(key_obj.get_round_key(16), key_obj.round_keys[0])
        self.assertEqual(key_obj.get_round_key(4), key_obj.round_keys[12])
