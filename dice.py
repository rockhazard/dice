#!/usr/bin/env python3

"""
* dice roller with full statistics output
* ability score roller with modifier calculator for D&D
* proficiency bonus calculator for D&D
* advantage/disadvantage roller for D&D
* averages are rounded up to the nearest whole number, reflecting hp rules
"""


import sys
import random
import math
import argparse
import re
from textwrap import dedent
from pathlib import Path


__author__ = 'rockhazard'


def roll_args(arg):
    """Splits standard dice notation input into a list of integers for roll()"""
    dice_pattern = re.compile(
        r'^(?P<num>\d*)[d|D](?P<sides>[2-9]|\d{2,})(?P<mod>[\+|\-]\d*)*$', re.I)
    if dice_pattern.match(arg):
        strHand = list(dice_pattern.match(arg).groups())
        # handle single die notation and no mod
        if not strHand[0]:
            strHand[0] = 1
        elif int(strHand[0]) < 1:
            strHand[0] = 1
        if not strHand[2]:
            strHand[2] = 0
        # convert input to integers
        intHand = [int(num) for num in strHand]
        return intHand
    else:
        sys.exit('Error: entry must be in standard dice notation, e.g. 1d6+1')

def roll(dice=1, sides=20, bonus=0, stat='total'):
    """
    stat can be used to return a dictionary of statistics with 'all', or one
    at a time.  Possible values: 'all', 'total', 'roll', 'average', 'max',
    'min', 'dice', 'sides', 'sorted', 'half', and 'double'
    """

    # bonus formatting
    if bonus != 0:
        throw = '{}d{} + ({})'.format(dice, sides, bonus)
    else:
        throw = '{}d{}'.format(dice, sides)

    # pre-roll stats
    average = math.ceil((sides / 2 + 0.5) * dice) + bonus
    minimum = dice * 1 + bonus
    maximum = dice * sides + bonus

    # roll
    rolls = []
    for die in range(dice):
        rolls.append(random.randint(1, sides))

    # post-roll stats
    rsort = sorted(rolls)
    total = sum(rolls) + bonus
    half = math.floor(total / 2)
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


def ability_score():
    """roll 4d6, subtract lowest die, then calculate score and modifier"""
    rolls = sorted([roll(1, 6) for i in range(0, 4)])
    del rolls[0]
    score = sum(rolls)
    mod = math.floor(round((score - 10) / 2, 2))
    result = dict(score=score, mod=mod)
    return result


def attack(verb=True):
    """d20 attack roll"""
    default_attack = roll()
    if verb:
        print('### ATTACK! ###')
        print(default_attack, '\n')
    else:
        return default_attack


def advantage(verb=True):
    """roll 2d20 then drop the lowest"""
    rolls = sorted([roll(), roll()])
    if verb:
        print('### Advantage ###')
        print(rolls)
        del rolls[0]
        print(rolls[0], '\n')
    else:
        del rolls[0]
        return rolls[0]


def disadvantage(verb=True):
    """roll 2d20 then drop the highest"""
    rolls = sorted([roll(), roll()])
    if verb:
        print('### Disadvantage ###')
        print(rolls)
        del rolls[1]
        print(rolls[0], '\n')
    else:
        del rolls[1]
        return rolls[0]


def prof_bonus(level=1):
    """calculate proficiency bonus (prof) based on level tiers"""
    # proficiency equals tier's index in prof_tiers plus 2.
    level = int(level)
    if level > 20:
        sys.exit('USAGE ERROR: Level must be between 1 and 20.')
    prof_tiers = [1, 5, 9, 13, 17, 21]
    prof = 2
    for tier in prof_tiers:
        tier_level_range = range(tier, prof_tiers[prof_tiers.index(tier) + 1])
        if level in tier_level_range:
            prof = prof_tiers.index(tier) + 2
            break
    print('Your proficiency bonus at level {} is {}.\n'.format(level, prof))


def percentile():
    print('### Percentile ###')
    print('{}%\n'.format(roll(1, 100)))


def ability():
    """create then print six ability scores and their modifiers"""
    score_1 = ability_score()
    score_2 = ability_score()
    score_3 = ability_score()
    score_4 = ability_score()
    score_5 = ability_score()
    score_6 = ability_score()

    print('### Ability Scores ###')
    print('roll: {} modifier: {}'.format(score_1['score'], score_1['mod']))
    print('roll: {} modifier: {}'.format(score_2['score'], score_2['mod']))
    print('roll: {} modifier: {}'.format(score_3['score'], score_3['mod']))
    print('roll: {} modifier: {}'.format(score_4['score'], score_4['mod']))
    print('roll: {} modifier: {}'.format(score_5['score'], score_5['mod']))
    print('roll: {} modifier: {}\n'.format(score_6['score'], score_6['mod']))


def stats_roll(dice=1, sides=20, bonus=0):
    """A dice roll that can print a complete dictionary of stats."""
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


def damage():
    """damage dice and their averages"""
    damage1 = roll(1, 4, stat='all')
    damage2 = roll(1, 6, stat='all')
    damage3 = roll(2, 6, stat='all')
    damage4 = roll(1, 8, stat='all')
    damage5 = roll(1, 10, stat='all')
    damage6 = roll(1, 12, stat='all')

    print('### Damage ###')
    print('{}  (average {}): {}'.format(damage1['roll'], damage1['average'],
                                        damage1['total']))
    print('{}  (average {}): {}'.format(damage2['roll'], damage2['average'],
                                        damage2['total']))
    print('{}  (average {}): {}'.format(damage3['roll'], damage3['average'],
                                        damage3['total']))
    print('{}  (average {}): {}'.format(damage4['roll'], damage4['average'],
                                        damage4['total']))
    print('{} (average {}): {}'.format(damage5['roll'], damage5['average'],
                                       damage5['total']))
    print('{} (average {}): {}'.format(damage6['roll'], damage6['average'],
                                       damage6['total']))
    print()


def main(argv):
    # parse commandline arguments
    parser = argparse.ArgumentParser(prog=str(Path(sys.argv[0]).name),
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=dedent("""\
        %(prog)s is a dice roller customized for D&D 5th Edition. Execution
        without any options will roll a d20 and return a result with statistics.
        """), epilog=dedent("""\
        %(prog)s was developed by rockhazard and licensed under GPL3.0.
        There are no warranties expressed or implied.
        """))
    parser.add_argument('--version', help='print version info then exit',
                        version="""%(prog)s 1.0a "Mystra", GPL3.0 (c) 2016, by rockhazard""",
                        action='version')
    parser.add_argument('-r', '--roll', help="""Roll a die or set of dice and
    retrieve a result.  Use normal dice notation, where X > 0, Y > 1, and Z is
    optional but can be any integer.""", metavar='XdY+/-Z')
    parser.add_argument('-s', '--stats', help="""Roll a die or set of dice and
    retrieve a result  with statistics. Use normal dice notation, where X > 0,
    Y > 1, and Z is optional but can be  any integer.""", metavar='XdY+/-Z')
    parser.add_argument('-a', '--advantage', help="""Roll advantage. This rolls
    2d20 and removes the lowest die.""", action='store_true')
    parser.add_argument('-d', '--disadvantage', help="""Roll disadvantage.
    This rolls 2d20 and removes the highest die.""", action='store_true')
    parser.add_argument('-p', '--proficiency', help="""Display your proficiency
    bonus by entering your LEVEL from 1 to 20.""", nargs=1, metavar=('LEVEL'))
    parser.add_argument('--ability', help="""Roll a set of ability scores with
    modifiers.""", action='store_true')
    parser.add_argument('-%', '--percentile', help="""Roll percentile.""",
                        action='store_true')
    parser.add_argument('--demo', help="""Demonstrate program features.""",
                        action='store_true')
    args = parser.parse_args()

    try:  # options that require user input.
        if args.roll:
            ra = roll_args(args.roll)
            print(roll(ra[0], ra[1], ra[2]))
        elif args.stats:
            ra = roll_args(args.stats)
            stats_roll(ra[0], ra[1], ra[2])
        elif args.proficiency:
            prof_bonus(args.proficiency[0])
    except ValueError:
        sys.exit('Error: invalid input.')

    if args.advantage:
        advantage()
    elif args.disadvantage:
        disadvantage()
    elif args.percentile:
        percentile()
    elif args.ability:
        ability()
    elif args.demo:
        ability()
        prof_bonus(5)
        advantage()
        disadvantage()
        attack()
        percentile()
        damage()
        stats_roll(20, 6)
    elif len(sys.argv) == 1:
        # if no arguments, roll a d20 with stats_roll
        stats_roll()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
