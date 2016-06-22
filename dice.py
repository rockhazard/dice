#!/usr/bin/env python3

"""
* dice roller with full statistics output
* ability score roller with modifier calculator for D&D
* proficiency bonus calculator for D&D
* advantage/disadvantage roller for D&D
* averages are rounded up to the nearest whole number, reflecting hp rules
"""

__author__ = 'rockhazard'

import sys, random, math, argparse, textwrap


def roll(dice=1, sides=20, bonus=0, stat='total'):
    """
    dice roller
    * default returns the resulting total of a 1d20 roll
    * use stat='key' to return a specific statistic, such as 'average'
    * example: roll(2, 6, stat='average') returns the average roll of 2d6
    * use stat='all' to return a dictionary of all stats
    """

    # pre-roll stats
    if bonus != 0:
        throw = '{}d{} + ({})'.format(dice,sides,bonus)
    else:
        throw = '{}d{}'.format(dice,sides)
    average = math.ceil((sides / 2 + 0.5) * dice) + bonus
    min = dice * 1 + bonus
    max = dice * sides + bonus

    # roll
    rolls = []
    count = dice
    while count > 0:
        rolls.append(random.randrange(1, sides + 1))
        count = count - 1

    # post-roll stats
    rsort = sorted(rolls)
    total = sum(rolls) + bonus
    half = math.floor(total / 2)
    double = total * 2

    # stats dictionary
    stats = dict(average=average, total=total, dice=dice, sides=sides, min=min, 
        max=max, half=half, double=double, sorted=rsort, roll=throw)

    # return all roll's stats or the stat specified.
    if stat == 'all':
        return stats
    else:
        for i in stats:
            if stat == i:
                return stats[i]

def abscore():
    # ability score roller creates a table of ability scores w/ their modifiers.

    # roll 4d6 and sort results lowest to highest
    d6a = roll(1, 6)
    d6b = roll(1, 6)
    d6c = roll(1, 6)
    d6d = roll(1, 6)
    rolls = sorted([d6a, d6b, d6c, d6d])

    # remove lowest roll, get total score, and calculate modifier
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
        print(rolls[0],'\n')
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
        print(rolls[0],'\n')
    else:
        del rolls[1]
        return rolls[0]

def profbonus(level=1):
    # calculate proficiency based on level tiers
    if level in range(1,21):
        if level in (1,2,3,4):
            prof = 2
        elif level in (5,6,7,8):
            prof = 3
        elif level in (9,10,11,12):
            prof = 4
        elif level in (13,14,15,16):
            prof = 5
        elif level in (17,18,19,20):
            prof = 6
    else:
        sys.exit('Your level must be between 1 and 20!')
    print('Your proficiency bonus at level {} is {}.\n'.format(level,prof))

def percentile():
    print('### Percentile ###')
    print('{}%\n'.format(roll(1, 100)))

def ability():
    # create then print six ability scores and their modifiers
    Score1 = abscore()
    Score2 = abscore()
    Score3 = abscore()
    Score4 = abscore()
    Score5 = abscore()
    Score6 = abscore()

    print('### Ability Scores ###')
    print('roll: {} mod: {}'.format(Score1['score'],Score1['mod']))
    print('roll: {} mod: {}'.format(Score2['score'],Score2['mod']))
    print('roll: {} mod: {}'.format(Score3['score'],Score3['mod']))
    print('roll: {} mod: {}'.format(Score4['score'],Score4['mod']))
    print('roll: {} mod: {}'.format(Score5['score'],Score5['mod']))
    print('roll: {} mod: {}\n'.format(Score6['score'],Score6['mod']))

def stats(dice=1, sides=20, bonus=0):
    # A dice roll that prints a complete stat table.
    eg = roll(dice,sides,bonus,stat='all')
    print(textwrap.dedent("""\
        #### Roll Statistics For: {} ###
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
    damage1 = roll(1,4, stat='all')
    damage2 = roll(1,6, stat='all')
    damage3 = roll(2,6, stat='all')
    damage4 = roll(1,8, stat='all')
    damage5 = roll(1,10, stat='all')
    damage6 = roll(1,12, stat='all')

    print('### Damage ###')
    print('{} (average {}): {}'.format(damage1['roll'], damage1['average'],
        damage1['total']))
    print('{} (average {}): {}'.format(damage2['roll'], damage2['average'],
        damage2['total']))
    print('{} (average {}): {}'.format(damage3['roll'], damage3['average'],
        damage3['total']))
    print('{} (average {}): {}'.format(damage4['roll'], damage4['average'],
        damage4['total']))
    print('{} (average {}): {}'.format(damage5['roll'], damage5['average'],
        damage5['total']))
    print('{} (average {}): {}'.format(damage6['roll'], damage6['average'],
        damage6['total']))
    print()

def main(argv):
    # parse commandline arguments
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""\
        dice.py is a dice roller customized for D&D 5th Edition. Execution
        without any options will roll a d20 and return a result with statistics.
        """), epilog=textwrap.dedent("""\
        dice was developed by rockhazard and licensed under GPL3.0. 
        There are no warranties expressed or implied.
        """))
    parser.add_argument('--version', help='print version info then exit', 
    version=
    'dice 1.0a "Mystra", GPL3.0 (c) 2016, by rockhazard', action='version')
    parser.add_argument('-r', '--roll', help=
        """Roll a die or set of dice and retrieve result.  Use the form 'x x x'
        such that you can roll, say, 2d6 +5 with '2 6 5'.  The bonus must be 
        included, even if it is 0.""", 
        nargs=3, metavar=('DICE', 'SIDES','BONUS'))
    parser.add_argument('-s', '--stats', help=
        """Roll a die or set of dice and retrieve all statistics.  Use the form 
        'x x x' such that you can roll, say, 2d6+5 with '2 6 5'.  The bonus 
        must be included, even if it is 0.""", 
        nargs=3, metavar=('DICE', 'SIDES','BONUS'))
    parser.add_argument('-a', '--advantage', help=
        'Roll advantage.  This rolls 2d20 and removes the lowest die.', 
        action='store_true')
    parser.add_argument('-d', '--disadvantage', help=
        'Roll disadvantage.  This rolls 2d20 and removes the highest die.', 
        action='store_true')
    parser.add_argument('-p', '--proficiency', help=
        'Display your proficiency bonus by entering your LEVEL from 1 to 20.', 
        nargs=1, metavar=('LEVEL'))
    parser.add_argument('--ability', help=
        'Roll a set of ability scores with modifiers.', 
        action='store_true')
    parser.add_argument('--demo', help=
        'Demonstrate program features.', 
        action='store_true')
    args = parser.parse_args()

    if args.roll:
        print(roll(int(args.roll[0]), int(args.roll[1]), int(args.roll[2])))
    if args.stats:
        stats(int(args.stats[0]), int(args.stats[1]), int(args.stats[2]))
    if args.advantage:
        advantage()
    if args.disadvantage:
        disadvantage()
    if args.ability:
        ability()
    if args.proficiency:
        profbonus(int(args.proficiency[0]))
    if args.demo:
        ability()
        profbonus(5)
        advantage()
        disadvantage()
        attack()
        percentile()
        damage()
        stats(20,6)
    if len(sys.argv) == 1:
        # if no arguments, roll a d20 with stats
        stats()

if __name__ == '__main__':
    # execute main method with cli args as input then exit
    sys.exit(main(sys.argv[1:]))                                        