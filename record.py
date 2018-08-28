import os
from shutil import copyfile
from pynput import keyboard
from aiy._drivers._led import LED
from aiy._drivers._button import Button
import aiy.audio


class ButtonRecorder():
    def __init__(self):

        # list of possible buttons to overwrite
        self.buttons = ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']

        # path for sfx files
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.temp_file = '{}/sfx/temp.wav'.format(self.dir_path)

        # init
        self.start_recorder()
        self.start_button()
        self.start_listener()

    def start_recorder(self):
        self.recorder = aiy.audio.get_recorder()
        self.recorder.start()

    def start_button(self):
        # turn light on
        self.pi_button = Button(channel = 23)
        self.pi_led = LED(channel = 25)
        self.pi_led.start()

    def start_listener(self):
        while True:
            # wait for input
            print('Press the button')
            self.pi_led.set_state(LED.PULSE_QUICK)
            self.pi_button.wait_for_press()

            # record
            self.pi_led.set_state(LED.ON)
            aiy.audio.say('Record some sound after the beep. Beep!')
            aiy.audio.record_to_wave(self.temp_file, 3)

            # playback
            self.pi_led.set_state(LED.DECAY)
            aiy.audio.say('Here is your audio recording')
            aiy.audio.play_wave(self.temp_file)

            # save
            aiy.audio.say('Select a button to save to')
            self.pi_led.set_state(LED.BEACON_DARK)
            with keyboard.Listener(on_release=self.on_release) as listener:
                listener.join()

    def on_release(self, key):
        # skip modifiers
        if key in [keyboard.Key.ctrl, keyboard.Key.shift, keyboard.Key.alt]:
            print('ignore modifier key')
            return

        # save?
        for button in self.buttons:
            if str(key) == "'{}'".format(button):
                print('save', button)
                self.save(button)
                return False

        # discard if key not found
        print('discard', str(key))
        aiy.audio.say('Recording discarded')
        return False

    def save(self, button):
        dest = '{}/sfx/{}.wav'.format(self.dir_path, button)
        copyfile(self.temp_file, dest)
        print('file saved', dest)
        aiy.audio.say('Recording saved')


button_recorder = ButtonRecorder()
