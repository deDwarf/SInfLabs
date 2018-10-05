from unittest import TestCase

from app.RSA.rsa_key import RSAKeyGenerator


class TestRSAKey(TestCase):
    def test_get_key(self):
        key = RSAKeyGenerator.get_key(61, 53, 17)
        self.assertEqual(key.get_public_key(), (3233, 17))
        self.assertEqual(key.get_private_key(), (3233, 2753))

