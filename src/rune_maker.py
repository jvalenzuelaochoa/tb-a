import time
import sys
import argparse
from random import randint
from pynput.keyboard import Key, Controller


keyboard = Controller()


# TODO: validate dictionaries
VOC_REGEN = {'mage' : 2, 'paladin' : 4/3}
MANA_PER_SPELL = {'ava' : 530, 'sd': 945, 'f_bomb' : 600, 'e_wall': 1000, 'w_growth' : 600, 'spear': 350, 'holy': 300}
FOOD_TIMERS = {'d_ham' : 720, 'b_mushroom': 264}

parser = argparse.ArgumentParser(description='Rune maker')

parser.add_argument('--spell',
                    choices=list(MANA_PER_SPELL.keys()),
                    default='ava',
                    help='Spell type {ava}')

parser.add_argument('--food',
                    choices=list(FOOD_TIMERS.keys()),
                    default='d_ham',
                    help='Food type {d_ham}')

parser.add_argument('--voc',
                    choices=list(VOC_REGEN.keys()),
                    default='mage',
                    help='Vocation {mage}')

parser.add_argument('--sb', dest='sb', action='store_true',
                    help='Specify this flag when using soft boots')


parser.add_argument('--sb_timer',  type=int, default=-1,
                    help='Specify time left on soft boots {minutes}')

args = parser.parse_args()

# TODO: argparse variables
# PARAMETERS
spell = args.spell
food = args.food
voc  = args.voc

print("Running Automationd for:")
print(f"{voc} using \'{spell}\' eating {food}")

RUNE_HOTKEY = Key.f2
FOOD_HOTKEY = Key.f1

#TODO: Change assignment to function
mana_regen = VOC_REGEN[voc] if not args.sb else VOC_REGEN[voc]+4

RUNE_DURATION = MANA_PER_SPELL[spell] / mana_regen
FOOD_DURATION = FOOD_TIMERS[food]

# Startup time
time.sleep(5)

def key_event(key):
    keyboard.press(key)
    time.sleep(.5)
    keyboard.release(key)

runer_struct = {'spell' : {'action' : RUNE_HOTKEY, 'duration' : RUNE_DURATION, 'jitter' : 5},
                'food' :  {'action' : FOOD_HOTKEY, 'duration' : FOOD_DURATION, 'jitter' : 14}}

counters = [0] * len(runer_struct.keys())
sb_timekeep = 0

while(True):
    for i, k in enumerate(runer_struct.keys()):
        if counters[i] <= 0:
            key_event(runer_struct[k]['action'])
            # Add variable deadtime to avoid exact patterns
            counters[i] = runer_struct[k]['duration'] + randint(0, runer_struct[k]['jitter'])
        # Extra white space to clear carries from larger numbers
        print("%s counter %.2f     " % (k, counters[i]))
        counters[i] -= 1

    sys.stdout.write("\033[F") # Cursor up one line
    sys.stdout.write("\033[F") # Cursor up one line
    time.sleep(1)
    if args.sb:
        sb_timekeep += 1
        #TODO: Change assignment to function
        if (args.sb_timer and (sb_timekeep >= args.sb_timer*60)):
            runer_struct['spell']['duration'] = MANA_PER_SPELL[spell] / VOC_REGEN[voc]

