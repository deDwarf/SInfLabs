import random
from collections import Counter
from typing import Dict

import utils
import hashlib

from app.DSA.utils import inverse


N = 1024
L = 160


class DSA:

    @classmethod
    def sign(cls, message: str, params: Dict, x_key: int) -> Dict:
        cls.__validate_params_dict(params)

        # Step 1. Generate random per-message key K
        k, k_ = cls.__generate_k(**params)
        # Step 2. Calculate (g^k mod p) mod q
        r = utils.square_and_multiply(base=params['g'], exponent=k, modulus=params['p']) % params['q']
        if r == 0:
            cls.sign(message, params, x_key)
        # Step 3. z = Hash( M ).
        z = cls.__message_sha1_hash(message.encode("utf-8"))
        z = int(z, 16)

        s = (k_ * (z + x_key * r)) % params['q']
        if s == 0:
            cls.sign(message, params, x_key)

        return {'r': r, 's': s}

    @classmethod
    def verify(cls, message: str, signature: Dict, params: Dict, y_key: int) -> bool:
        cls.__validate_params_dict(params)

        if not 0 < signature['r'] < params['q'] or not 0 < signature['s'] < params['q']:
            return False

        # Step 1. Calculate W
        w = inverse(signature['s'], params['q'])
        # Step 1.1. z = hash(Message)
        z = cls.__message_sha1_hash(message.encode("utf-8"))
        z = int(z, 16)
        # --
        u1 = (z * w) % params['q']
        u2 = (signature['r'] * w) % params['q']
        v = ((pow(params['g'], u1, params['p']) * pow(y_key, u2, params['p'])) % params['p']) % params['q']

        return v == signature['r']

    @classmethod
    def __message_sha1_hash(cls, message) -> str:
        """output len = 160 bits"""
        return hashlib.sha1(message).hexdigest()

    @classmethod
    def __generate_k(cls, p, q, g, try_count: int = 0):
        """
        `DSA Per-Message Secret Number` generator
        """
        c = random.getrandbits(N + 64)
        k = (c % (q - 1)) + 1
        try:
            k_ = inverse(k, q)
            return k, k_
        except ValueError:
            if try_count > 40:
                raise ValueError("Attempt limit exceeded: Inverse Error")
            return cls.__generate_k(p, q, g, try_count=try_count+1)

    @classmethod
    def __validate_params_dict(cls, params: Dict):
        if Counter(params.keys()) != Counter(['p', 'q', 'g']):
            raise ValueError("Wrong algorithm parameters dict. "
                             "Expected (p, q, g) keys, but got: ", [i for i in params])
