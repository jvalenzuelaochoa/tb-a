import time
import sys
from random import randint
from pynput.keyboard import Key, Controller


keyboard = Controller()


# TODO: validate dictionaries
VOC_REGEN = {'mage' : 2, 'paladin' : 4/3}
MANA_PER_RUNE = {'ava' : 530, 'sd': 945, 'f_bomb' : 600, 'e_wall': 1000, 'w_growth' : 600}
FOOD_TIMERS = {'d_ham' : 720, 'b_mushroom': 264}


# TODO: argparse variables
# PARAMETERS
rune = 'ava'
food = 'b_mushroom'
voc  = 'mage'


RUNE_HOTKEY = Key.f2
FOOD_HOTKEY = Key.f1

RUNE_DURATION = MANA_PER_RUNE[rune] / VOC_REGEN[voc]
FOOD_DURATION = FOOD_TIMERS[food]

# Startup time
time.sleep(5)

def key_event(key):
    keyboard.press(key)
    time.sleep(.5)
    keyboard.release(key)


runer_struct = [('rune', RUNE_HOTKEY, RUNE_DURATION),('food', FOOD_HOTKEY, FOOD_DURATION)]

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

