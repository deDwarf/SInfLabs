from unittest import TestCase
from app.DES.bit_utils import *

from bitarray import bitarray


class TestTransform(TestCase):
    good_bits = bitarray('00101010')
    more_bits = bitarray('0010101000')
    less_bits = bitarray('00101')

    PERM_RULES = [3, 5, 7, 1, 6, 8, 2, 4]
    PERM_EXPECTED = '11100000'

    EXT_RULES = [3, 5, 7, 1, 6, 8, 2, 4, 3, 5, 7]
    EXT_EXPECTED = '11100000111'

    REDUCE_RULES = [3, 5, 6, 8]
    REDUCE_EXPECTED = '1100'

    MALFORMED_RULES = [3, 5, 7, 1, 6, 8, 2, 10]

    def test_positive(self):
        tmp = transform(self.good_bits, self.PERM_RULES).to01()
        self.assertEqual(tmp, self.PERM_EXPECTED)

        tmp = transform(self.good_bits, self.EXT_RULES, resize_allowed=True).to01()
        self.assertEqual(tmp, self.EXT_EXPECTED)

        tmp = transform(self.good_bits, self.REDUCE_RULES, resize_allowed=True).to01()
        self.assertEqual(tmp, self.REDUCE_EXPECTED)

    def test_resize(self):
        exception = None
        try:
            transform(self.more_bits, self.PERM_RULES).to01()
        except ValueError as e:
            exception = e
        self.assertIsNotNone(exception)

        exception = None
        try:
            transform(self.less_bits, self.PERM_RULES).to01()
        except ValueError as e:
            exception = e
        self.assertIsNotNone(exception)

        exception = None
        try:
            transform(self.good_bits, self.MALFORMED_RULES).to01()
        except ValueError as e:
            exception = e
        self.assertIsNotNone(exception)


class TestShifts(TestCase):
    bits = bitarray('0001101001')

    def test_left_circular(self):
        self.assertEqual('0011010010', circular_left_shift(self.bits, 1).to01())
        self.assertEqual('0110100100', circular_left_shift(self.bits, 2).to01())
        self.assertEqual('1101001000', circular_left_shift(self.bits, 3).to01())
        self.assertEqual('0001101001', circular_left_shift(self.bits, 10).to01())
        self.assertEqual('0011010010', circular_left_shift(self.bits, 11).to01())

    def test_right_circular(self):
        self.assertEqual('1000110100', circular_right_shift(self.bits, 1).to01())
        self.assertEqual('0100011010', circular_right_shift(self.bits, 2).to01())
        self.assertEqual('0010001101', circular_right_shift(self.bits, 3).to01())
        self.assertEqual('0001101001', circular_right_shift(self.bits, 10).to01())
        self.assertEqual('1000110100', circular_right_shift(self.bits, 11).to01())


class TestPadding(TestCase):
    def test_add_padding(self):
        value = bitarray('11000011' * 5)
        result = pad_to_64bits_multiple(value)
        self.assertEqual('11000011' * 5 + '00000011' * 3, result.to01())

    def test_remove_padding(self):
        value = bitarray('11000011' * 5 + '00000011' * 3)
        result = remove_64_multiple_bits_padding(value)
        self.assertEqual('11000011' * 5, result.to01())

        value = bitarray('11000011' * 5 + '00000111' * 3)
        result = remove_64_multiple_bits_padding(value)
        self.assertEqual('11000011' * 5 + '00000111' * 3, result.to01())
