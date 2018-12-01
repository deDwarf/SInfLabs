import random
from typing import Dict

import utils


def generate_private_key(params: Dict):
    """Choose a secret private key x by some random method, where 0 < x < q"""
    return random.randint(1, params['q'] - 1)


def generate_public_key(params: Dict, private_key: int):
    """Calculate the public key [y = g^x mod p]"""
    return utils.square_and_multiply(base=params['g'], exponent=private_key, modulus=params['p'])

