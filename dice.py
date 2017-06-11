#!/usr/bin/env python3

"""
dice.py is a dice roller with optional statistical output (averages rounded up).
The program accepts standard dice notation (such as 2d6+4 or d20).
"""


import sys
import re
import argparse
from random import randint
from math import floor
from math import ceil
from textwrap import dedent

__author__ = 'rockhazard'


def roll_args(arg):
    """Splits standard dice notation input into a list of integers for roll()"""
    dice_pattern = re.compile(
        r'^(?P<num>\d*)[d|D](?P<sides>\d+)(?P<mod>[\+|\-]\d*)*$', re.I)
    if dice_pattern.match(arg):
        strHand = list(dice_pattern.match(arg).groups())
        # handle single die notation, minimum sides, and no mod
        if not strHand[0]:
            strHand[0] = 1
        if int(strHand[1]) < 2:
            strHand[1] = 2
            print('ERROR: input fewer than 2 sides; converting to minimum.')
        if not strHand[2]:
            strHand[2] = 0
        # convert input to integers
        intHand = [int(num) for num in strHand]
        return intHand
    else:
        sys.exit('ERROR: entry must be in standard dice notation, e.g. 1d6+1')


def roll(dice=1, sides=20, bonus=0, stat='total'):
    """
    stat can be used to return a dictionary of statistics with 'all', or one
    of these values: 'all', 'total', 'roll', 'average', 'max', 'min', 'dice', 
    'sides', 'sorted', 'half', and 'double'
    """

    # bonus formatting
    if bonus != 0:
        throw = '{}d{} + ({})'.format(dice, sides, bonus)
    else:
        throw = '{}d{}'.format(dice, sides)

    # pre-roll stats
    average = ceil((sides / 2 + 0.5) * dice) + bonus
    minimum = dice * 1 + bonus
    maximum = dice * sides + bonus

    # roll
    rolls = []
    for die in range(dice):
        rolls.append(randint(1, sides))

    # post-roll stats
    rsort = sorted(rolls)
    total = sum(rolls) + bonus
    half = floor(total / 2)
    double = total * 2

    # stats dictionary
    stats = dict(average=average, total=total, dice=dice, sides=sides,
                 min=minimum, max=maximum, half=half, double=double,
                 sorted=rsort, roll=throw)

    # return all roll's stats or specified stat.
    if stat == 'all':
        return stats
    else:
        return stats[stat]


def stats_roll(dice=1, sides=20, bonus=0):
    """A dice roll that prints stats."""
    example = roll(dice, sides, bonus, stat='all')
    print(dedent("""\
        ### Roll Statistics For: {} ###
        Roll: ....... {}
        Total: ...... {}
        Average: .... {}
        Minimum: .... {}
        Maximum: .... {}
        Dice: ....... {}
        Sides/Die: .. {}
        Half ........ {}
        Double ...... {}
        """.format(example['roll'], example['sorted'], example['total'],
                   example['average'], example['min'], example['max'],
                   example['dice'], example['sides'], example['half'],
                   example['double'])))

    # Message for a critical or an automatic failure.
    if dice == 1 and sides == 20:
        if example['sorted'][0] == 20:
            print('Great success!\n')
        elif example['sorted'][0] == 1:
            print('Pathetic!\n')


def main(argv):
    # parse commandline arguments
    parser = argparse.ArgumentParser(prog='dice.py',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=dedent("""\
        %(prog)s is a dice roller customized for role playin ggames. Execution
        without any options will roll a d20 and return a result with statistics.
        """), epilog=dedent("""\
        %(prog)s was developed by rockhazard and licensed under GPL3.0.
        There are no warranties expressed or implied.
        """))
    parser.add_argument('--version', help='print version info then exit',
                        version=dedent("""\
                        %(prog)s 1.0a "Mystra"
                        GPL3.0 (c) 2016, by rockhazard"""), action='version')
    parser.add_argument('-r', '--roll', help="""Roll a die or set of dice and
    retrieve a result.  Use normal dice notation, where X > 0, Y > 1, and Z is
    optional but can be any integer.""", metavar='XdY+/-Z')
    parser.add_argument('-s', '--stats', help="""Roll a die or set of dice and
    retrieve a result  with statistics. Use normal dice notation, where X > 0,
    Y > 1, and Z is optional but can be  any integer.""", metavar='XdY+/-Z')
    args = parser.parse_args()

    try:  # options that require user input.
        if args.roll:
            ra = roll_args(args.roll)
            print(roll(ra[0], ra[1], ra[2]))
        elif args.stats:
            ra = roll_args(args.stats)
            stats_roll(ra[0], ra[1], ra[2])
    except ValueError:
        sys.exit('ERROR: invalid input.')
    if len(sys.argv) == 1:
        # if no arguments, roll a d20 with stats_roll
        stats_roll()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
