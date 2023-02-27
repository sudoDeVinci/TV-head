from machine import Pin
from neopixel import NeoPixel


# The current animation being played
# This is a global value which is changed via the
# Interrupt handler for the buttons.

# Pin numbers to address
P = 16
# Number of leds to address
N = 100

# Define display to draw to
# Display is our array of leds.

# Uncomment for Pi Pico:
display = NeoPixel(Pin(P), N, timing = 1)

def clear(display):
    display.fill((0,0,0))
    display.write()

clear(display)