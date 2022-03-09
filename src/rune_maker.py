import time
import sys
import argparse
from random import randint
from pynput.keyboard import Key, Controller
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *


keyboard = Controller()


# TODO: validate dictionaries
VOC_REGEN = {'Mage' : 2, 'Paladin' : 4/3, 'Knight': 2/3}
MANA_PER_SPELL = {'Avalanche/GFB' : 530, 'SD': 945, 'Fire Bomb' : 600, 'Energy Wall': 1000, 'Wild Growth' : 600, 'Enchented Spear': 350, 'Holy Missile': 300, 'Burst Arrow': 290}
FOOD_TIMERS = {'Dragon Ham' : 720, 'Brown Mushroom': 264, 'Ham': 360}
RING_TIMERS = {}



class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.sb  = False
        self.roh = False
        self.sb_timer = 0
        self.voc   = list(VOC_REGEN.keys())[0]
        self.food  = list(FOOD_TIMERS.keys())[0]
        self.spell = list(MANA_PER_SPELL.keys())[0]

        # setting title
        self.setWindowTitle("Night's Watch")

        # setting geometry
        self.setGeometry(100, 100, 600, 400)

        # calling method
        self.Vocations()

        # calling method
        self.Spell()

        # calling method
        self.Food()

        # showing all the widgets
        self.show()

    # method for widgets
    def Vocations(self):

        # creating a combo box widget
        self.voc_box = QComboBox(self)

        # setting geometry of combo box
        self.voc_box.setGeometry(50, 50, 150, 30)

        # making it editable
        self.voc_box.setEditable(True)

        # adding list of items to combo box
        self.voc_box.addItems(VOC_REGEN.keys())

        # adding action to combo box
        self.voc_box.activated.connect(self.update_voc)


        self.start_button = QPushButton('Start!', self)
        self.start_button.setToolTip('Start Counters')
        self.start_button.move(250,80)
        self.start_button.clicked.connect(self.start)


        self.start_button = QPushButton('STOP!', self)
        self.start_button.setToolTip('stop Counters')
        self.start_button.move(250,150)
        self.start_button.clicked.connect(self.on_click)

        b1 = QCheckBox("Soft Boots", self)
        b1.setChecked(False)
        b1.move(50,250)
        b1.resize(200,50)
        b1.stateChanged.connect(self.btnstate)

        b2 = QCheckBox("Ring of Healing", self)
        b2.setChecked(False)
        b2.move(300,250)
        b2.resize(200,50)
        b2.stateChanged.connect(self.roh_state)

        sb_i = QLineEdit('0', self)
        sb_i.setValidator(QIntValidator())
        sb_i.setMaxLength(3)
        sb_i.setAlignment(Qt.AlignRight)
        sb_i.setGeometry(100,300, 150, 40)
        sb_i.setFont(QFont("Arial", 12))
        sb_i.textChanged.connect(self.textchanged)

        sb_label = QLabel("Time Left", self)
        sb_label.setGeometry(50, 300, 120, 60)
        sb_label.setWordWrap(True)

        roh_i = QLineEdit('0', self)
        roh_i.setValidator(QIntValidator())
        roh_i.setMaxLength(3)
        roh_i.setAlignment(Qt.AlignRight)
        roh_i.setGeometry(350,300, 100, 40)
        roh_i.setFont(QFont("Arial", 12))
        roh_i.textChanged.connect(self.textchanged)

        roh_label = QLabel("Amount", self)
        roh_label.setGeometry(300, 300, 120, 60)
        roh_label.setWordWrap(True)

    def textchanged(self,text):
        self.sb_timer = int(text)

    def btnstate(self, state):
        self.sb = True if state == QtCore.Qt.Checked else False
        print(f'Updated sb [ {self.sb} ]')

    def roh_state(self, state):
        self.roh = True if state == QtCore.Qt.Checked else False
        print(f'Updated roh [ {self.roh} ]')

    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')

    # method for widgets
    def Spell(self):

        # creating a combo box widget
        self.spell_box = QComboBox(self)

        # setting geometry of combo box
        self.spell_box.setGeometry(50, 100, 150, 30)
        # making it editable
        self.spell_box.setEditable(True)

        # adding list of items to combo box
        self.spell_box.addItems(MANA_PER_SPELL.keys())

        # adding action to combo box
        self.spell_box.activated.connect(self.update_spell)

    # method for widgets
    def Food(self):

        # creating a combo box widget
        self.food_box = QComboBox(self)

        # setting geometry of combo box
        self.food_box.setGeometry(50, 150, 150, 30)
        # making it editable
        self.food_box.setEditable(True)

        # adding list of items to combo box
        self.food_box.addItems(FOOD_TIMERS.keys())

        # adding action to combo box
        self.food_box.activated.connect(self.update_food)

    def update_food(self):
        self.food = self.food_box.currentText()

    def update_spell(self):
        self.spell = self.food_box.currentText()

    def update_voc(self):
        self.voc = self.food_box.currentText()

    @pyqtSlot()
    def start(self):
        print("Running Automationd for:")
        print(f"{self.voc} using \'{self.spell}\' eating {self.food}")
        print(f"{'Using' if self.sb else 'not using'} soft boots")
        RUNE_HOTKEY = Key.f2
        FOOD_HOTKEY = Key.f1
        ROH_HOTKEY = Key.f3

        #TODO: Change assignment to function
        mana_regen = VOC_REGEN[self.voc] if not self.sb else VOC_REGEN[self.voc]+4

        RUNE_DURATION = MANA_PER_SPELL[self.spell] / mana_regen
        FOOD_DURATION = FOOD_TIMERS[self.food]

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
            if self.sb:
                print(f"{self.sb_timer*60-sb_timekeep} left on soft boots.")

            sys.stdout.write("\033[F") # Cursor up one line
            sys.stdout.write("\033[F") # Cursor up one line
            if self.sb:
                sb_timekeep += 1
                #TODO: Change assignment to function
                if (self.sb_timer and (sb_timekeep >= self.sb_timer*60)):
                    runer_struct['spell']['duration'] = MANA_PER_SPELL[self.spell] / VOC_REGEN[self.voc]
                sys.stdout.write("\033[F") # Cursor up one line
            time.sleep(1)


def main():
    app = QApplication(sys.argv)
    window = Window()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()