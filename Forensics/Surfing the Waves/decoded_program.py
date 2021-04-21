#!/usr/bin/env python3
import numpy as np
from scipy.io.wavfile import write
from binascii import hexlify
from random import random

with open('generate_wav.py', 'rb') as f:
        content = f.read()
        f.close()

# Convert this program into an array of hex values
hex_stuff = (list(hexlify(content).decode("utf-8")))

# Loop through the each character, and convert the hex a-f characters to 10-15
for i in range(len(hex_stuff)):
        if hex_stuff[i] == 'a':
                hex_stuff[i] = 10
        elif hex_stuff[i] == 'b':
                hex_stuff[i] = 11
        elif hex_stuff[i] == 'c':
                hex_stuff[i] = 12
        elif hex_stuff[i] == 'd':
                hex_stuff[i] = 13
        elif hex_stuff[i] == 'e':
                hex_stuff[i] = 14
        elif hex_stuff[i] == 'f':
                hex_stuff[i] = 15

        # To make the program actually audible, 100 hertz is added from the beginning, then the number is multiplied by
        # 500 hertz
        # Plus a cheeky random amount of noise
        hex_stuff[i] = 1000 + int(hex_stuff[i]) * 500 + (10 * random())


def sound_generation(name, rand_hex):
        # The hex array is converted to a 16 bit integer array
        scaled = np.int16(np.array(hex_stuff))
        # Sci Pi then writes the numpy array into a wav file
        write(name, len(hex_stuff), scaled)
        randomness = rand_hex


# Pump up the music!
# print("Generating main.wav...")
# sound_generation('main.wav')
# print("Generation complete!")

# Your ears have been blessed
# picoCTF{mU21C_1s_1337_115155af}