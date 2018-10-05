from unittest import TestCase
from app.DES.des import algorithm
from app.DES.des_key.des_key import *
from app.DES.bit_utils import bitarr_to_hex


class TestAlgorithm(TestCase):
    def test_algorithm(self):
        key_encrypt = DESKey(Mode.ENCRYPT_MODE, 'AABB09182736CCDD', KeyType.BASE16_INTEGER)
        key_decrypt = DESKey(Mode.DECRYPT_MODE, 'AABB09182736CCDD', KeyType.BASE16_INTEGER)
        text_hex = '123456ABCD132536'
        text_bitarr = bitarray(hex_to_bitarr(text_hex))

        encrypted = bitarr_to_hex(algorithm(text_bitarr, key_encrypt))
        decrypted = bitarr_to_hex(algorithm(bitarray(hex_to_bitarr(encrypted)), key_decrypt))

        print()
        print('Original:  ' + text_hex)
        print('Encrypted: ' + encrypted)
        print('Decrypted: ' + decrypted)
        self.assertEqual(text_hex, decrypted)

