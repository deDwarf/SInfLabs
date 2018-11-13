import time
from unittest import TestCase

from app.RSA.rsa import RSA
from app.RSA.rsa_key import RSAKeyGenerator


class TestRSA(TestCase):
    def test_encrypt(self):
        # key = RSAKeyGenerator.get_key(61, 53, 17)
        key = RSAKeyGenerator.generate_key()
        print("Generated key: public{}, private{}".format(key.get_public_key(), key.get_private_key()))
        text = "{lalala"
        print("Original text: '{}'".format(text))
        encrypted = RSA.encrypt(text, key)
        print("Encrypted: " + encrypted)

        decrypted = RSA.decrypt(encrypted, key)
        print("Decrypted: " + decrypted)

        # damn async print
        time.sleep(0.5)

