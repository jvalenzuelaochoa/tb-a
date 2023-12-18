from pynput.keyboard import Key, Controller
import time

class KeyCombination:

    def __init__(self, keyboard, modifier, key) -> None:
        self.keyboard = keyboard
        self.modifier = modifier
        self.key = key

    def press(self):
        if self.modifier != '':
            self.keyboard.press(self.modifier)
            time.sleep(.1)
            self.keyboard.press(self.key)
            time.sleep(.3)
            self.keyboard.release(self.key)
            time.sleep(.1)
            self.keyboard.release(self.modifier)
        else:
            self.keyboard.press(self.key)
            time.sleep(.3)
            self.keyboard.release(self.key)