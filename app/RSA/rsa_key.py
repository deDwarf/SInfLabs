from typing import Tuple
from math import gcd


class Key:
    def __init__(self, n, e, d):
        """
        :param n: common part for public/private keys. p * q result
        :param e: part of public key
        :param d: part of private key
        """
        self.n = int(n)
        self.e = int(e)
        self.d = int(d)

    def get_private_key(self) -> Tuple[int, int]:
        return self.n, self.d

    def get_public_key(self) -> Tuple[int, int]:
        return self.n, self.e


class RSAKeyGenerator:

    @classmethod
    def get_key(cls, p: int, q: int, e: int) -> Key:
        n = p * q
        totient = (p - 1) * (q - 1)
        if e < 1 or e > totient or gcd(e, totient) != 1:
            raise ValueError("Invalid 'e' number: {}. [gcd(e, totient) && 1 < e < totient] condition is not satisfied")
        d = cls.__get_damn_d(totient, e)
        return Key(n, e, d)

    @classmethod
    def generate_key(cls) -> Key:
        raise NotImplementedError()

    @classmethod
    def __get_damn_d(cls, totient, e):
        # d = (1 + x * totient) / e
        d = 0.01
        i = 0
        while d - round(d) != 0:
            d = (1 + i * totient) / e
            i += 1

        return d
