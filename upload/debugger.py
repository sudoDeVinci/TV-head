from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms
from os import listdir
from sys import exit
from clear import clear


# Variable to keep running script or not.
running = True


# The current animation being played
# This is a global value which is changed via the
# Interrupt handler for the buttons.

# Pin numbers to address
P = 16
# Number of leds to address
N = 100

# Define display to draw to
# Display is our array of leds.

display = NeoPixel(Pin(P), N, timing = 1)

# Sequential snake
def snake(snake_length = 5, snake_colour = (50, 50, 50), ms = 30) -> None:

    # snake repreesented as an array of indexes
    coords = [i for i in range(snake_length)]

    # Increment snake indexes until the last one reaches the end of the display
    while coords[-1] <= (N-1):
        clear(display)
        # Draw snake to the display
        for i in range(snake_length):
            display[coords[i]] = snake_colour
        display.write()
        

        # Incrmemnt snake indexes
        coords = [i+1 for i in coords]

        sleep_ms(ms)
    
    # Decremnt snake indexes
    coords = [i-1 for i in coords]
        
    while coords[0] >= 0:
        
        clear(display)
        
        # Draw snake to the display
        for i in range(snake_length):
            display[coords[i]] = snake_colour
        display.write()
        
        # Decremnt snake indexes
        coords = [i-1 for i in coords]
        
        sleep_ms(ms)



def main() -> None:
    for i in range(3):
        snake(snake_colour=(50,10,50))
        
main()
