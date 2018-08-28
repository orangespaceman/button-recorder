import os
import sys
import random
import subprocess


# get button
if len(sys.argv) > 1:
    button = sys.argv[1]

# if not set (a.k.a. big red), pick one at random
else:
    buttons = ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
    button = random.choice(buttons)

# set sound file path
dir_path = os.path.dirname(os.path.realpath(__file__))
mp3 = '{}/sfx/{}.mp3'.format(dir_path, button)
wav = '{}/sfx/{}.wav'.format(dir_path, button)

# play
if os.path.isfile(wav):
    subprocess.call(['aplay', wav])
elif os.path.isfile(mp3):
    subprocess.call(['mpg321', mp3])
