from unittest import TestCase
from app.DES.des import DES


class TestDES(TestCase):
    KEY = '12345678'

    def test_encrypt_decrypt(self):
        text = 'Hi there, bitchezz!'

        encrypted = DES.encrypt(text, self.KEY)
        self.assertNotEqual(text, encrypted)

        decrypted = DES.decrypt(encrypted, self.KEY)
        self.assertEqual(text, decrypted)

        print('--- --- --- --- --- --- ---')
        print('Original text: ' + text)
        print('encrypted: {}'.format(encrypted))
        print('decrypted: {}'.format(decrypted))
