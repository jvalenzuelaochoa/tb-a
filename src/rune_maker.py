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
                    help='Spell type')

parser.add_argument('--food',
                    choices=list(FOOD_TIMERS.keys()),
                    default='d_ham',
                    help='Food type')

parser.add_argument('--voc',
                    choices=list(VOC_REGEN.keys()),
                    default='mage',
                    help='Vocation')

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

RUNE_DURATION = MANA_PER_SPELL[spell] / VOC_REGEN[voc]
FOOD_DURATION = FOOD_TIMERS[food]

# Startup time
time.sleep(5)

def key_event(key):
    keyboard.press(key)
    time.sleep(.5)
    keyboard.release(key)


runer_struct = [('spell', RUNE_HOTKEY, RUNE_DURATION),('food', FOOD_HOTKEY, FOOD_DURATION)]

counters = [0] * len(runer_struct)

while(True):
    for i, c in enumerate(counters):
        if c <= 0:
            key_event(runer_struct[i][1])
            # Add variable deadtime to avoid exact patterns
            counters[i] = runer_struct[i][2] + randint(0, 15)
        # Extra white space to clear carries from larger numbers
        print(f"{runer_struct[i][0]} counter {counters[i]}      ")
        counters[i] -= 1
        
    sys.stdout.write("\033[F") # Cursor up one line
    sys.stdout.write("\033[F") # Cursor up one line
    time.sleep(1)

