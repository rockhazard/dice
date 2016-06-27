#!/usr/bin/env python3
# dice tests


import unittest
# from hypothesis import given
# import hypothesis.strategies as st
import dice


class Test(unittest.TestCase):
    def setUp(self):
        # initial conditions: variables, open files, etc.
        # Dice Roll:
        self.average = dice.roll(stat='average')
        self.max = dice.roll(stat='max')
        self.min = dice.roll(stat='min')
        self.dice = dice.roll(stat='dice')
        self.sides = dice.roll(stat='sides')
        # Dice Argument Parsing:
        self.roll_args_neg = dice.roll_args('10d100-50')
        self.roll_args_pos = dice.roll_args('10d100+50')
        self.roll_args_2dice = dice.roll_args('2d4')
        self.roll_args_2dice_bonus = dice.roll_args('2d4+5')

    def tearDown(self):
        # cleanup operations: close/remove files, etc.
        pass

    # roll tests
    def test_roll_average(self):
        self.assertEqual(self.average, 11, 'Not equal')

    def test_roll_maximum(self):
        self.assertEqual(self.max, 20, 'Not equal')

    # @given(st.integers(min_value=0, max_value=1))
    def test_roll_minimum(self):
        self.assertEqual(self.min, 1, 'Not equal')

    def test_roll_dice(self):
        self.assertEqual(self.dice, 1, 'Not equal')

    def test_roll_sides(self):
        self.assertEqual(self.sides, 20, 'Not equal')

    # roll_args tests
    def test_roll_args_neg(self):
        self.assertEqual(self.roll_args_neg, ['10', '100', '-50'],
                         'Parse failure.')

    def test_roll_args_pos(self):
        self.assertEqual(self.roll_args_pos, ['10', '100', '50'],
                         'Parse failure.')

    def test_roll_args_2dice(self):
        self.assertEqual(self.roll_args_2dice, ['2', '4', 0],
                         'Parse failure.')

    def test_roll_args_2dice_bonus(self):
        self.assertEqual(self.roll_args_2dice_bonus, ['2', '4', '5'],
                         'Parse failure.')


"""
COMMON ASSERTS:
assert - base assert allowing you to write your own assertions
assertEqual(a, b) - check a and b are equal
assertNotEqual(a, b) - check a and b are not equal
assertIn(a, b) - check that a is in the item b
assertNotIn(a, b) - check that a is not in the item b
assertFalse(a) - check that the value of a is False
assertTrue(a) - check the value of a is True
assertIsInstance(a, TYPE) - check that a is of type "TYPE"
assertRaises(ERROR, a, args) - check that when a is called with 
    args that it raises ERROR
"""

if __name__ == "__main__":
    # call unittest module
    unittest.main()
