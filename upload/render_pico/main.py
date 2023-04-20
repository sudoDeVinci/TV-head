"""
Boilerplate from :
https://randomnerdtutorials.com/micropython-ws2812b-addressable-rgb-leds-neopixel-esp32-esp8266/
Idea from:
https://rose.systems/tv_head/
"""


from machine import Pin, ADC
from neopixel import NeoPixel
from time import sleep_ms
from os import listdir
from random import randint


br_pin = Pin(25, Pin.IN)
sp_pin = Pin(26, Pin.IN)
an_pin = Pin(27, Pin.IN)


# Variable to keep running script or not.
running = True

# The current animation being played
# This is a global value which is changed via the
# Interrupt handler for  the buttons.
current_animation = "/csvs/big_eye"
 
# Pin numbers to address
p = 13
# Number of leds to address
n = 96

# Global brightness coefficient
b = 0.25

# Define display to draw to
# Display is our array of leds.


# Uncomment for ESP-32:
display = NeoPixel(Pin(p), n, timing = 1)

def read_frames(folder_path:str) -> list[list[int]]:

    for filename in listdir(folder_path):
        if filename.endswith('.csv'):
            with open("/".join([folder_path, filename]), 'r', encoding = "utf-8") as csvfile:
                frame = tuple((line.rstrip('\n').rstrip('\r').split(",")) for line in csvfile)
            animate(frame)


def get_animations(folder_path = "/csvs/") -> list[str]:
    folders = [name for name in listdir(folder_path) if path.isdir(name)]
    

# Play frames with a set time interval in ms.
def animate(frame, sleep:int = 0) -> None:
    global b
    for p in frame[1:]:
        display[int(p[0])] = (int(int(p[3])*b), int(int(p[2])*b), int(int(p[1])*b))
    display.write()
    sleep_ms(sleep)


def main() -> None:
    for i in range(20):
        read_frames(current_animation)
        sleep_ms(2000)
  

if __name__ == '__main__':
    main()
    clear_display()