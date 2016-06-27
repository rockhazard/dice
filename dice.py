#!/usr/bin/env python3

"""
* dice roller with full statistics output
* ability score roller with modifier calculator for D&D
* proficiency bonus calculator for D&D
* advantage/disadvantage roller for D&D
* averages are rounded up to the nearest whole number, reflecting hp rules
"""

__author__ = 'rockhazard'

import sys
import random
import math
import argparse
import textwrap


def roll_args(arg):
    # allow user to enter normal roll notation (e.g. 2d6+5)
    # returns a list of int-convertible strings for roll().
    roll_args_format_check(arg)
    num = type(1)
    raw = arg.split("d")
    if len(raw[1].split('-')) == 2:
        neg_bonus = raw[1].split('-')
        neg_bonus[1] = '-' + neg_bonus[1]
        neg_bonus.insert(0, raw[0])
        if len(neg_bonus) < 3:
            neg_bonus.insert(2,0)
        return  neg_bonus
    elif len(raw[1].split('+')) == 2:
        pos_bonus = raw[1].split('+')
        pos_bonus.insert(0, raw[0])
        if len(pos_bonus) < 3:
            pos_bonus.insert(2,0)
        return pos_bonus
    else:
        if len(raw) == 2:
            raw.append(0)
        return raw
    roll_args_int_check(dice_args)


def roll_args_format_check(arg):
    if 'd' not in arg:
        sys.exit('Roll notation must include "d", as in "1d20".')


def roll_args_int_check(arg):
    for die in arg:
        try:
            int(die)
        except ValueError:
            sys.exit('USAGE ERROR: Invalid input.')


def roll(dice=1, sides=20, bonus=0, stat='total'):
    """
    dice roller
    * default returns the resulting total of a 1d20 roll
    * use stat='key' to return a specific statistic, such as 'average'
    * example: roll(2, 6, stat='average') returns the average roll of 2d6
    * use stat='all' to return a dictionary of all stats
    """

    # pre-roll stats
    if dice < 1:
        dice = 1
        print('Number of dice must be greater than 0: setting dice to 1!')
    if sides < 2:
        sides = 2
        print('Number of sides must be greater than 1: setting sides to 2!')
    if bonus != 0:
        throw = '{}d{} + ({})'.format(dice, sides, bonus)
    else:
        throw = '{}d{}'.format(dice, sides)
    average = math.ceil((sides / 2 + 0.5) * dice) + bonus
    minimum = dice * 1 + bonus
    maximum = dice * sides + bonus

    # roll
    rolls = []
    count = dice
    while count > 0:
        rolls.append(random.randrange(1, sides + 1))
        count -= 1

    # post-roll stats
    rsort = sorted(rolls)
    total = sum(rolls) + bonus
    half = math.floor(total / 2)
    double = total * 2

    # stats dictionary
    stats = dict(average=average, total=total, dice=dice, sides=sides,
                 min=minimum, max=maximum, half=half, double=double,
                 sorted=rsort, roll=throw)

    # return all roll's stats or the stat specified.
    if stat == 'all':
        return stats
    else:
        for i in stats:
            if stat == i:
                return stats[i]


def ability_score():
    # ability score: roll 4d6, subtract 1 die, then calculate score and modifier
    rolls = sorted([roll(1, 6) for i in range(0, 4)])
    del rolls[0]
    score = sum(rolls)
    mod = math.floor(round((score - 10) / 2, 2))
    result = dict(score=score, mod=mod)
    return result


def attack(ver=True):
    # attack roll
    attack = roll()
    if ver:
        print('### ATTACK! ###')
        print(attack, '\n')
    else:
        return attack


def advantage(verb=True):
    # advantage: roll 2d20 then drop the lowest
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
    # disadvantage: roll 2d20 then drop the highest
    rolls = sorted([roll(), roll()])
    if verb:
        print('### Disadvantage ###')
        print(rolls)
        del rolls[1]
        print(rolls[0], '\n')
    else:
        del rolls[1]
        return rolls[0]


def profBonus(level=1):
    # calculate proficiency based on level tiers
    if level in range(1, 21):
        if level in (1, 2, 3, 4):
            prof = 2
        elif level in (5, 6, 7, 8):
            prof = 3
        elif level in (9, 10, 11, 12):
            prof = 4
        elif level in (13, 14, 15, 16):
            prof = 5
        elif level in (17, 18, 19, 20):
            prof = 6
    else:
        sys.exit('Your level must be between 1 and 20!')
    print('Your proficiency bonus at level {} is {}.\n'.format(level, prof))


def percentile():
    print('### Percentile ###')
    print('{}%\n'.format(roll(1, 100)))


def ability():
    # create then print six ability scores and their modifiers
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


def stats(dice=1, sides=20, bonus=0):
    # A dice roll that prints a complete stat table.
    eg = roll(dice, sides, bonus, stat='all')
    print(textwrap.dedent("""\
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
        """.format(eg['roll'], eg['sorted'], eg['total'], eg['average'],
                   eg['min'], eg['max'], eg['dice'], eg['sides'], eg['half'],
                   eg['double'])))

    # Message for a critical or an automatic failure.
    if dice == 1 and sides == 20:
        if eg['sorted'][0] == 20:
            print('Great success!\n')
        elif eg['sorted'][0] == 1:
            print('Pathetic!\n')


def damage():
    # print out sample damage dice and their averages
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
    parser = argparse.ArgumentParser(prog=sys.argv[0][2:],
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description=textwrap.dedent("""\
        %(prog)s is a dice roller customized for D&D 5th Edition. Execution
        without any options will roll a d20 and return a result with statistics.
        """), epilog=textwrap.dedent("""\
        %(prog)s was developed by rockhazard and licensed under GPL3.0.
        There are no warranties expressed or implied.
        """))
    parser.add_argument('--version', help='print version info then exit',
                        version='%(prog)s 1.0a "Mystra", GPL3.0 (c) 2016, by rockhazard',
                        action='version')
    parser.add_argument('-r', '--roll', help="""Roll a die or set of dice and retrieve result. Use normal dice notation
    such that "2d6+5" means 2 six-sided dice plus 5.""", metavar='XdY+/-Z')
    parser.add_argument('-s', '--stats', help="""Roll a die or set of dice and retrieve all statistics. Use normal dice
    notation such that "2d6+5" means 2 six-sided dice plus 5.""",
                        metavar='XdY+/-Z')
    parser.add_argument('-a', '--advantage', help='Roll advantage.  This rolls 2d20 and removes the lowest die.',
                        action='store_true')
    parser.add_argument('-d', '--disadvantage', help='Roll disadvantage.  This rolls 2d20 and removes the highest die.',
                        action='store_true')
    parser.add_argument('-p', '--proficiency', help='Display your proficiency bonus by entering your LEVEL from 1 to 20.',
                        nargs=1, metavar=('LEVEL'))
    parser.add_argument('--ability', help='Roll a set of ability scores with modifiers.',
                        action='store_true')
    parser.add_argument('--demo', help='Demonstrate program features.',
                        action='store_true')
    args = parser.parse_args()

    if args.roll:
        ra = roll_args(args.roll)
        print(roll(int(ra[0]), int(ra[1]), int(ra[2])))
    if args.stats:
        ra = roll_args(args.stats)
        stats(int(ra[0]), int(ra[1]), int(ra[2]))
    if args.advantage:
        advantage()
    if args.disadvantage:
        disadvantage()
    if args.ability:
        ability()
    if args.proficiency:
        profBonus(int(args.proficiency[0]))
    if args.demo:
        ability()
        profBonus(5)
        advantage()
        disadvantage()
        attack()
        percentile()
        damage()
        stats(20, 6)
    if len(sys.argv) == 1:
        # if no arguments, roll a d20 with stats
        stats()


if __name__ == '__main__':
    # execute main method with cli args as input then exit
    sys.exit(main(sys.argv[1:]))
