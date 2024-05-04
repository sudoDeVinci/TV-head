
"""
Boilerplate from :
https://randomnerdtutorials.com/micropython-ws2812b-addressable-rgb-leds-neopixel-esp32-esp8266/
Idea from:
https://rose.systems/tv_head/
"""


from machine import Pin, UART,freq
from neopixel import NeoPixel
from time import sleep_ms
from os import listdir, ilistdir, statvfs
from math import pow
from typing import List, Tuple, Dict, Callable, Any, Union, Optional
from random import randint
import gc

# If debug is True, our debug lines throughtout the code will print. Otherwise, do nothing
DEBUG:bool = False
def out01(x:str) -> None:
    pass
def out02(x:str) -> None:
    pass
debug = out01 if DEBUG else out02

# Variables to define constant labels
BRIGHTNESS = "Brightness"
CHANNEL = "Channel"
SPEED = "Speed"

# Variable to keep running script or not.
RUNNING:bool = True

# Folder for animation csvs
ANIMATION_FOLDER:str = "/csvs/"

# Pin number to address
P = 16
# Number of leds to address
N = 160

# Define display to draw to
# Display is our array of leds.
display = NeoPixel(Pin(P), N, timing = 1)

"""
 Attempt overclock ESP32 for higher responsiveness
 ESP32S3 is overclockable at 240MHz.
 ESP32 Base is overclockable at 200MHz.
"""
try:
    freq(200000000)
    debug("Core overclock applied succesfully!") 
except Exception as e:
    debug("Core overclock not applied.")
    
debug(f"-> Current speed is: {(freq()/1000000):.3f} MHZ")

def get_animation_paths(folder_path = ANIMATION_FOLDER) -> Tuple[str]:
    """
    Get a tuple of the animation folder paths.
    """
    return tuple(ANIMATION_FOLDER+file[0] for file in ilistdir(folder_path) if file[1] == 0x4000)

animation_paths = get_animation_paths()
animation_amount = len(animation_paths)
animations = list()

values = {
    BRIGHTNESS: 0.25,
    SPEED: 1,
    CHANNEL: 3
}

def read_frames(folder_path:str) -> Tuple[Tuple[Tuple[int, int, int, int]]]:
    """
    Read the frames within a given animation folder and return it as a tuple[index, r, g, b] of ints.
    """
    def assemble(filename:str) -> Tuple[Tuple[int, int, int, int]]:
        frame: Tuple[Tuple[int, int, int, int]] = None
        with open(filename, 'r', encoding = "utf-8") as csvfile:
            """
            Skip the first line so we can directly convert each line to tuple[int, int, int, int].
            """
            next(csvfile)
            frame = tuple((int(i), int(a), int(b), int(c)) for i, a, b, c in (line.rstrip('\n').rstrip('\r').split(",") for line in csvfile))
            
        return frame
                
    frames = tuple(assemble("/".join([folder_path, filename])) for filename in listdir(folder_path) if filename.endswith('.csv'))
    
    return frames

def clear() -> None:
    """
    Clear the display.
    """
    global display
    display.fill((0,0,0))
    display.write()

def animate(frames: Tuple[Tuple[Tuple[int, int, int, int]]]) -> None:
    """
    Play frames with a set time interval in ms.
    """
    global display
    b = values["Brightness"]
    for frame in frames:
        for p in frame:
            display[p[0]] = int(p[3]*b), int(p[2]*b), int(p[1]*b)
        display.write()
        sleep_ms(int(values["Speed"]*20))
        


def main() -> None:
    global animations
    global values
    global RUNNING
    
    # Pre-load animations in a Tuple. 
    animations = tuple(read_frames(folder) for folder in animation_paths)
    
    while RUNNING:
        animate(animations[values['Channel']])
        sleep_ms(int(values["Speed"]*5000))
  

if __name__ == '__main__':
    try:
        clear()
        main()
    except Exception as e:    
        print(e)
        clear()