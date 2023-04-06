from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms
from os import listdir
from sys import exit


# Variable to keep running script or not.
running = True


# Pin numbers to address
P = 13
# Number of leds to address
N = 25

# Define display to draw to
# Display is our array of leds.

display = NeoPixel(Pin(P), N, timing = 1)

# Sequential snake
def snake(snake_length = 4, snake_colour = (50, 50, 50), ms = 30) -> None:

    # Snake repreesented as an array of indexes.
    # We have the upper and lower lmit so we don't need to hold the actual snake array
    # in memory.
    ul = snake_length - 1
    ll = 0 
    # Draw intial snake to the display
    for i in range(ll, ul+1):
        display[i] = snake_colour
    display.write()
    sleep_ms(ms)


    while ul < (N-1):
        display[ll] = (0,0,0)
        ul += 1
        display[ul] = (snake_colour) 
        display.write() 
        ll += 1
        sleep_ms(ms)
    
    while ll > 0:
        display[ul] = (0,0,0)
        ll -= 1
        display[ll] = snake_colour
        display.write()
        ul -= 1
        sleep_ms(ms)



def main() -> None:
    for i in range(3):
        snake(snake_colour=(250,150,250), ms=45)
        
main()
