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
        if not cls.validate_e(e, totient):
            raise ValueError("Invalid 'e' number: {}. [gcd(e, totient) && 1 < e < totient] condition is not satisfied")
        d = cls.__get_damn_d(totient, e)
        return Key(n, e, d)

    @classmethod
    def generate_key(cls) -> Key:
        import primesieve as prime_gen
        import random
        import time

        random.seed(round(time.time()))
        q = prime_gen.n_primes(1, 10 ** 3 + random.randint(1, 100))[0]
        random.seed(round(time.time() - 1000))
        p = prime_gen.n_primes(1, 10 ** 3 - random.randint(1, 100))[0]
        totient = (p - 1) * (q - 1)
        random.seed(round(time.time()))
        e = prime_gen.n_primes(1, totient / 4)[0] + 1
        while not cls.validate_e(e, totient):
            e += 1

        return cls.get_key(p, q, e)

    @classmethod
    def validate_e(cls, e, totient):
        return 1 < e < totient and gcd(e, totient) == 1

    @classmethod
    def __get_damn_d(cls, totient, e):
        res = 0
        for d in range(3, totient, 1):
            if d * e % totient == 1:
                res = d
                break

        return res
