from config import *
from machine import Pin, UART,freq
from neopixel import NeoPixel
from time import sleep_ms
from os import listdir, ilistdir, statvfs
from math import pow
import gc

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


# Define display to draw to.
# Display is our array of leds.
display = NeoPixel(Pin(P), N, timing = 1)


def get_animation_paths(folder_path = ANIMATION_FOLDER) -> Tuple[str]:
    """
    Get a tuple of the animation folder paths.
    """
    return tuple(ANIMATION_FOLDER+file[0] for file in ilistdir(folder_path) if file[1] == 0x4000)


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


def animate(frames: Tuple[Tuple[Tuple[int, int, int, int]]]) -> None:
    """
    Play frames with a set time interval in ms.
    """
    global display
    b = RENDER_VALUES["Brightness"]
    for frame in frames:
        for p in frame:
            display[p[0]] = int(p[3]*b), int(p[2]*b), int(p[1]*b)
        display.write()
        sleep_ms(int(RENDER_VALUES["Speed"]*20))


def main() -> None:
    animation_paths = get_animation_paths()
    animation_amount = len(animation_paths)
    animations = list()
    global RENDER_VALUES
    global RUNNING
    
    # Pre-load animations in a Tuple. 
    animations = tuple(read_frames(folder) for folder in animation_paths)
    
    while RUNNING:
        animate(animations[RENDER_VALUES['Channel']])
        sleep_ms(int(RENDER_VALUES["Speed"]*5000))
