def inverse(z, a):
    """
    For algorithm description see "fips-186-3" specification document, appendix C.1

    :param z: The value to be inverted mod a (i.e., either k or s).
    :param a: The domain parameter and (prime) modulus (i.e., either q or n ).
    :return: The multiplicative inverse of z mod a , if it exists.
    :raise ValueError if multiplicative inverse does not exists
    """
    if not (0 < z < a and a > 0):
        raise ValueError("Inverse error")
    i = a
    j = z
    y2 = 0
    y1 = 1
    while j > 0:
        quotient = i//j
        remainder = i - j * quotient
        y = y2 - y1 * quotient
        i, j = j, remainder
        y2, y1 = y1, y
    if i == 1:
        return y2 % a
