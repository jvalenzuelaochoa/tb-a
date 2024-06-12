from cmath import inf
import time
import sys
from random import randint
from pynput.keyboard import Key, Controller
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import key_combination as kc
import runer_thread as rt

keyboard = Controller()

# TODO: validate dictionaries
REST_BONUS = 2
VOC_REGEN = {'Mage' : 2, 'Paladin' : 4/3, 'Knight': 2/3}
MANA_PER_SPELL = {'Avalanche/GFB' : 530, 'SD': 945, 'Fire Bomb' : 600, 'Energy Wall': 1000, 'Wild Growth' : 600, 'Enchented Spear': 350, 'Holy Missile': 300, 'Burst Arrow': 290, 'Salvation': 210}
FOOD_TIMERS = {'Brown Mushroom': 264, 'Dragon Ham' : 720, 'Ham': 360}
RING_TIMERS = {'LIFE_RING' : 1200 , 'RING_OF_HEALING' : 450}
ITEM_REGEN = {'SOFT_BOOTS' : 12*REST_BONUS/6, 'LIFE_RING' : 8*REST_BONUS/6, 'RING_OF_HEALING' : 24*REST_BONUS/6}
SB_DURATION = 14400

def no_routine():
    pass

def terminate_program():
    sys.exit()


def take_action(routine):
    key_combination, post_routine = routine
    key_combination.press()
    post_routine()


class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.soft_boots  = False
        self.ring = False
        self.ring_type = list(RING_TIMERS.keys())[0]
        self.soft_boots_timer = 0
        self.soft_boots_count = 0
        self.ring_timer = 0
        self.ring_count = 0
        self.voc   = list(VOC_REGEN.keys())[0]
        self.food  = list(FOOD_TIMERS.keys())[0]
        self.spell = list(MANA_PER_SPELL.keys())[0]
        self.logout = False
        self._runer_threads = dict()
        self.logout_time = 0
        self._run_main_thread = False
        self._display = "Select Settings and press Start!"

        # setting title
        self.setWindowTitle("Night's Watch")

        # setting geometry
        self.setGeometry(100, 100, 600, 800)

        # calling method
        self.Vocations()

        # calling Mana Modifiers
        self.Food()
        self.SoftBoots()
        self.Rings()

        # calling method
        self.Spell()
        self.LogOutBox()

        self.FlowButtons()

        self.DisplayBox()

        # showing all the widgets
        self.show()

    # method for widgets
    def Vocations(self):

        # creating a combo box widget
        self._voc_box = QComboBox(self)

        # setting geometry of combo box
        self._voc_box.setGeometry(50, 50, 150, 30)

        # making it editable
        self._voc_box.setEditable(True)

        # adding list of items to combo box
        self._voc_box.addItems(VOC_REGEN.keys())

        # adding action to combo box
        self._voc_box.activated.connect(self.update_voc)
    
    def DisplayBox(self):
        self._display_frame = QFrame(self)
        self._display_frame.setGeometry(50, 500, 500, 200)
        self._display_frame.setFrameShape(QFrame.Box)
        self._display_frame.setFrameShadow(QFrame.Sunken)

        self._display_label = QLabel(self._display, self._display_frame)
        self._display_label.setAlignment(Qt.AlignTop)
        self._display_label.setGeometry(0, 0, 500, 200)
        self._display_label.setWordWrap(True)
 
    def SoftBoots(self):
        self._sb_button = QCheckBox("Soft Boots", self)
        self._sb_button.setChecked(False)
        self._sb_button.move(50,250)
        self._sb_button.resize(200,50)
        self._sb_button.stateChanged.connect(self.soft_boots_state)

        self._sb_label = QLabel("Time Left", self)
        self._sb_label.setGeometry(50, 300, 120, 60)
        self._sb_label.setWordWrap(True)

        self._sb_time_textbox = QLineEdit('0', self)
        self._sb_time_textbox.setValidator(QIntValidator())
        self._sb_time_textbox.setMaxLength(3)
        self._sb_time_textbox.setAlignment(Qt.AlignRight)
        self._sb_time_textbox.setGeometry(100,300, 150, 40)
        self._sb_time_textbox.setFont(QFont("Arial", 12))
        self._sb_time_textbox.textChanged.connect(self.soft_boots_timer_changed)

        self._sb_count_label = QLabel("Amount", self)
        self._sb_count_label.setGeometry(50, 350, 120, 60)
        self._sb_count_label.setWordWrap(True)

        self._sb_count_textbox = QLineEdit('0', self)
        self._sb_count_textbox.setValidator(QIntValidator())
        self._sb_count_textbox.setMaxLength(3)
        self._sb_count_textbox.setAlignment(Qt.AlignRight)
        self._sb_count_textbox.setGeometry(100,350, 150, 40)
        self._sb_count_textbox.setFont(QFont("Arial", 12))
        self._sb_count_textbox.textChanged.connect(self.soft_boots_count_changed)

    def FlowButtons(self):

        self._start_button = QPushButton('Start!', self)
        self._start_button.setToolTip('Start Counters')
        self._start_button.move(250,80)

        self._stop_button = QPushButton('STOP!', self)
        self._stop_button.setToolTip('stop Counters')
        self._stop_button.move(250,150)
        self._stop_button.setEnabled(False)
        
        self._start_button.clicked.connect(self.start_main_thread)
        self._stop_button.clicked.connect(self.on_stop_click)

    def validate_num_box(self,text):
        try:
            return int(text)
        except:
            return 0

    def soft_boots_timer_changed(self,text):
        self.soft_boots_timer = self.validate_num_box(text)

    def soft_boots_count_changed(self,text):
        self.soft_boots_count = self.validate_num_box(text)

    def soft_boots_state(self, state):
        self.soft_boots = True if state == QtCore.Qt.Checked else False
        print(f'Updated sb [ {self.soft_boots} ]')

    def ring_state(self, state):
        self.ring = True if state == QtCore.Qt.Checked else False
        print(f'Updated ring usage [ {self.ring} ]')

    def ring_count_changed(self,text):
        self.ring_count = self.validate_num_box(text)

    def logout_state(self, state):
        self.logout = True if state == QtCore.Qt.Checked else False

    def logout_time_changed(self,text):
        self.logout_time = self.validate_num_box(text)

    @pyqtSlot()
    def on_stop_click(self):
        self.stop_main_thread()

    # method for widgets
    def Spell(self):

        # creating a combo box widget
        self._spell_box = QComboBox(self)

        # setting geometry of combo box
        self._spell_box.setGeometry(50, 100, 150, 30)
        # making it editable
        self._spell_box.setEditable(True)

        # adding list of items to combo box
        self._spell_box.addItems(MANA_PER_SPELL.keys())

        # adding action to combo box
        self._spell_box.activated.connect(self.update_spell)

    # method for widgets
    def Food(self):

        # creating a combo box widget
        self._food_box = QComboBox(self)

        # setting geometry of combo box
        self._food_box.setGeometry(50, 150, 150, 30)
        # making it editable
        self._food_box.setEditable(True)

        # adding list of items to combo box
        self._food_box.addItems(FOOD_TIMERS.keys())

        # adding action to combo box
        self._food_box.activated.connect(self.update_food)

    # method for widgets
    def Rings(self):

        self._ring_checkbox = QCheckBox("Use Rings", self)
        self._ring_checkbox.setChecked(False)
        self._ring_checkbox.move(300,250)
        self._ring_checkbox.resize(200,50)
        self._ring_checkbox.stateChanged.connect(self.ring_state)

        self._ring_count_textbox = QLineEdit('0', self)
        self._ring_count_textbox.setValidator(QIntValidator())
        self._ring_count_textbox.setMaxLength(3)
        self._ring_count_textbox.setAlignment(Qt.AlignRight)
        self._ring_count_textbox.setGeometry(350,300, 100, 40)
        self._ring_count_textbox.setFont(QFont("Arial", 12))
        self._ring_count_textbox.textChanged.connect(self.ring_count_changed)

        self._ring_label = QLabel("Amount", self)
        self._ring_label.setGeometry(300, 300, 120, 60)
        self._ring_label.setWordWrap(True)

        # creating a combo box widget
        self._ring_box = QComboBox(self)

        # setting geometry of combo box
        self._ring_box.setGeometry(400, 260, 150, 30)
        # making it editable
        self._ring_box.setEditable(True)

        # adding list of items to combo box
        self._ring_box.addItems(RING_TIMERS.keys())

        # adding action to combo box
        self._ring_box.activated.connect(self.update_ring)

    def LogOutBox(self):

        self._logout_checkbox = QCheckBox("Set Logout", self)
        self._logout_checkbox.setChecked(False)
        self._logout_checkbox.move(300,400)
        self._logout_checkbox.resize(200,50)
        self._logout_checkbox.stateChanged.connect(self.logout_state)

        self._logout_textbox = QLineEdit('0', self)
        self._logout_textbox.setValidator(QIntValidator())
        self._logout_textbox.setMaxLength(3)
        self._logout_textbox.setAlignment(Qt.AlignRight)
        self._logout_textbox.setGeometry(350,450, 100, 40)
        self._logout_textbox.setFont(QFont("Arial", 12))
        self._logout_textbox.textChanged.connect(self.logout_time_changed)

        self._logout_label = QLabel("Time", self)
        self._logout_label.setGeometry(300, 450, 120, 60)
        self._logout_label.setWordWrap(True)

    def update_food(self):
        self.food = self._food_box.currentText()

    def update_ring(self):
        self.ring_type = self._ring_box.currentText()

    def update_spell(self):
        self.spell = self._spell_box.currentText()

    def update_voc(self):
        self.voc = self._voc_box.currentText()
    
    def toggle_ui_controls(self, value):
        self._start_button.setEnabled(value)
        self._sb_button.setEnabled(value)
        self._sb_time_textbox.setEnabled(value)
        self._sb_count_textbox.setEnabled(value)
        self._voc_box.setEnabled(value)
        self._ring_box.setEnabled(value)
        self._ring_checkbox.setEnabled(value)
        self._ring_count_textbox.setEnabled(value)
        self._food_box.setEnabled(value)
        self._spell_box.setEnabled(value)

        self._stop_button.setEnabled(not value)


    @pyqtSlot()
    def start_main_thread(self):
        self._run_main_thread = True
        self.toggle_ui_controls(False)
        self._main_thread = threading.Thread(target=self.start)
        self._main_thread.start()


    def stop_main_thread(self):
        self._run_main_thread = False
        for x in self._runer_threads.keys():
            self._runer_threads[x].stop()
        while self._main_thread.is_alive():
            time.sleep(.1)
        self.toggle_ui_controls(True)    
        self._display = "Select Settings and press Start!"
        self.update_display()

    def update_display(self):
        self._display_label.setText(self._display)
    

    def start(self):
        print("Running Automationd for:")
        print(f"{self.voc} using \'{self.spell}\' eating {self.food}")
        print(f"{'Using' if self.soft_boots else 'not using'} soft boots")
        FOOD_HOTKEY = kc.KeyCombination(keyboard, '', Key.f1)
        RUNE_HOTKEY = kc.KeyCombination(keyboard, '', Key.f2)
        SB_HOTKEY   = kc.KeyCombination(keyboard, Key.shift, Key.f1)
        RING_HOTKEY = kc.KeyCombination(keyboard, Key.shift, Key.f2)
        LOGOUT_HOTKEY = kc.KeyCombination(keyboard, Key.ctrl_l, 'l' )

        #TODO: Change assignment to function
        mana_regen = VOC_REGEN[self.voc] if not self.soft_boots else VOC_REGEN[self.voc]+4

        RUNE_DURATION = MANA_PER_SPELL[self.spell] / mana_regen
        FOOD_DURATION = FOOD_TIMERS[self.food]

        # Startup time
        time.sleep(5)

        # Thread initialization
        self._runer_threads = dict()
        runer_struct = {'spell' : {'action' : (RUNE_HOTKEY, no_routine), 'duration' : RUNE_DURATION, 'limit' : inf, 'mana_impact' : 0, 'jitter' : 4},
                        'food' :  {'action' : (FOOD_HOTKEY, no_routine), 'duration' : FOOD_DURATION, 'limit' : inf, 'mana_impact' : VOC_REGEN[self.voc], 'jitter' : 3}}

        if self.soft_boots:
            runer_struct['sb'] = {'action' : (SB_HOTKEY, no_routine), 'duration' : SB_DURATION, 'limit' : self.soft_boots_count, 'mana_impact' : ITEM_REGEN['SOFT_BOOTS'], 'jitter' : 14}

        if self.ring:
            runer_struct['ring'] = {'action' : (RING_HOTKEY, no_routine), 'duration' : RING_TIMERS[self.ring_type], 'limit' : self.ring_count, 'mana_impact' : ITEM_REGEN[self.ring_type], 'jitter' : 9}

        if self.logout:
            runer_struct['logout'] = {'action' : (LOGOUT_HOTKEY, terminate_program), 'duration' : self.logout_time, 'limit' : 2, 'mana_impact' : 0, 'jitter' : 9} #limit is 2 to ensure it gets clicked at least once

        counters = dict()

        for x in  runer_struct.keys():
            self._runer_threads[x] = rt.RunerThread(x, 0)
            counters[x] = 0

        # Overwrite softboots initial counter
        if self.soft_boots:
            self._runer_threads['sb'].set_timeout( self.soft_boots_timer *60 )
            self._runer_threads['sb'].start()
            counters['sb'] = 1

        # Overwrite logout initial counter
        if self.logout:
            self._runer_threads['logout'].set_timeout( self.logout_time *60 )
            self._runer_threads['logout'].start()
            counters['logout'] = 1

        while(self._run_main_thread):
            display_log = []
            for i in runer_struct.keys():
                # Check if thread is finished
                if not self._runer_threads[i].is_alive():
                    counters[i] +=1
                    if counters[i] <= runer_struct[i]['limit']:
                        take_action(runer_struct[i]['action'])
                        # Add variable deadtime to avoid exact patterns
                        self._runer_threads[i] = rt.RunerThread(i, runer_struct[i]['duration'] + randint(0, runer_struct[i]['jitter']))
                        self._runer_threads[i].start()
                    else:
                        runer_struct[i]['mana_impact'] = 0
                # Extra white space to clear carries from larger numbers
                else:
                    display_log.append(f"{runer_struct[i]['limit'] - counters[i] + 1} {i} left. Timer: {self._runer_threads[i].time_left()} ")

            # Recalculate duration of spells based on current mana regen
            mana_regen = 0
            for x in  runer_struct.keys():
                mana_regen += runer_struct[x]['mana_impact']
            runer_struct['spell']['duration'] = MANA_PER_SPELL[self.spell] / mana_regen

            self._display = '\n'.join(display_log)
            self.update_display()
            time.sleep(.5)

def main():
    app = QApplication(sys.argv)
    window = Window()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()