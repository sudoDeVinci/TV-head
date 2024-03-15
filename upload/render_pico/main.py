
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


# Attempt overclock for higher responsiveness
try:
    freq(200000000)
    debug("Core overclock applied succesfully!") 
except Exception as e:
    debug("Core overclock not applied.")
    
debug(f"-> Current speed is: {(freq()/1000000):.3f} MHZ")

def get_animation_paths(folder_path = ANIMATION_FOLDER) -> tuple[str]:
    """
    Get a tuple of the animation folder paths.
    """
    folders = tuple(ANIMATION_FOLDER+file[0] for file in ilistdir(folder_path) if file[1] == 0x4000)
    return folders

animation_paths = get_animation_paths()
animation_amount = len(animation_paths)
animations = list()

values = {
    BRIGHTNESS: 0.25,
    SPEED: 1,
    CHANNEL: 3
}

def read_frames(folder_path:str) -> list[list[int]]:
    """
    Read the frames within a given animation folder and return it as a tuple[index, r, g, b] of ints.
    """
    global animations
    global animation_paths
    frames = []
    for filename in listdir(folder_path):
        if filename.endswith('.csv'):
            with open("/".join([folder_path, filename]), 'r', encoding = "utf-8") as csvfile:
                """
                Skip the first line so we can directly convert each line to tuple[int, int, int, int].
                """
                next(csvfile)
                
                frame = tuple((int(i), int(a), int(b), int(c)) for i, a, b, c in (line.rstrip('\n').rstrip('\r').split(",") for line in csvfile))
                frames.append(frame)
    
    return frames

def clear() -> None:
    """
    Clear the display.
    """
    global display
    display.fill((0,0,0))
    display.write()

def animate(frames) -> None:
    """
    Play frames with a set time interval in ms.
    """
    global display
    global values
    global SPEED
    
    for frame in frames:
        b = values[BRIGHTNESS]
        c = values[CHANNEL]
        for p in frame:
            display[p[0]] = int(p[3]*b), int(p[2]*b), int(p[1]*b)
        display.write()
        if b != values[BRIGHTNESS] or c!= values[CHANNEL]:
            values[SPEED] = 0
            return False
        sleep_ms(values[SPEED]*10)
    return True
        


def main() -> None:
    global animations
    global values
    global RUNNING
    global SPEED

    animations = tuple(read_frames(folder) for folder in animation_paths)
    while RUNNING:
        if animate(animations[values[CHANNEL]]):
            sleep_ms(values[SPEED]*randint(200, 5000))

        
  

if __name__ == '__main__':
    try:
        clear()
        main()
    except Exception as e:    
        debug(e)
        clear()
     