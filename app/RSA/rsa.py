from typing import Tuple
import math
from app.RSA.rsa_key import Key


def _square_and_multiply(base, exponent, modulus):
    exponent = '{0:b}'.format(exponent)
    z = 1
    l = len(exponent)

    for i in range(0, l):
        z = (math.pow(z, 2)) % modulus
        if exponent[i] == "1":
            z = (z * base) % modulus

    return int(z)


class RSA:
    verbose = False

    @classmethod
    def encrypt(cls, text: str, key: Key) -> str:
        key = key.get_public_key()
        return cls.__do_rsa(text, key, 'encrypt')

    @classmethod
    def decrypt(cls, text: str, key: Key) -> str:
        key = key.get_private_key()
        return cls.__do_rsa(text, key, 'decrypt')

    @classmethod
    def __do_rsa(cls, text, key: Tuple[int, int], action: str):
        result_str = ""

        for c in text:
            result_int = _square_and_multiply(ord(c), key[1], key[0])
            if cls.verbose:
                print("{}: {} -> {}".format(action, c, result_int))
            result_str += chr(result_int)

        return result_str

