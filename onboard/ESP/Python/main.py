"""
Boilerplate from :
https://randomnerdtutorials.com/micropython-ws2812b-addressable-rgb-leds-neopixel-esp32-esp8266/
Idea from:
https://rose.systems/tv_head/
"""

from machine import Pin, UART, freq
from neopixel import NeoPixel
from time import sleep_ms
from os import listdir, ilistdir, statvfs
from random import randint
import gc


# If debug is True, our debug lines throughtout the code will print. Otherwise, do nothing
DEBUG: bool = False


def out01(x: str) -> None:
    """
    Print the given string.
    """
    print(x)


def out02(x: str) -> None:
    """
    Don't print the given string.
    This is a dummy function.
    """
    pass


debug = out01 if DEBUG else out02

# Variables to define constant labels
BRIGHTNESS = "Brightness"
CHANNEL = "Channel"
SPEED = "Speed"

# Variable to keep running script or not.
RUNNING: bool = True

# Folder for animation csvs
ANIMATION_FOLDER: str = "/csvs/"

# Pin number to address
P = 21
# Number of leds to address
N = 100

# Define display to draw to
# Display is our array of leds.
display = NeoPixel(Pin(P), N, timing=1)

"""
 Attempt overclock ESP32 for higher responsiveness
 ESP32S3 is overclockable at 240MHz.
 ESP32 Base is overclockable at 200MHz.
"""
try:
    freq(240000000)
    print("Core overclock applied succesfully!")
except Exception:
    print("Core overclock not applied.")

debug(f"-> Current speed is: {(freq()/1000000):.3f} MHZ")


def get_animation_paths(folder_path: str = ANIMATION_FOLDER) -> tuple[str]:
    """
    Get a tuple of the animation folder paths.
    """
    return tuple(ANIMATION_FOLDER+file[0]
                 for file in ilistdir(folder_path) if file[1] == 0x4000)


animation_paths = get_animation_paths()
animation_amount = len(animation_paths)-1
animations = list()

values: dict[str, float | int] = {
    BRIGHTNESS: 0.15,
    SPEED: 1,
    CHANNEL: 0
}


def read_frames(folder_path: str) -> tuple[tuple[tuple[int, int, int, int]]]:
    """
    Read the frames within a given animation folder and return it
    as a tuple[index, r, g, b] of ints.
    """
    def assemble(filename: str) -> tuple[tuple[int, int, int, int]]:
        frame: tuple[tuple[int, int, int, int]] = None
        with open(filename, 'r', encoding="utf-8") as csvfile:
            """
            Skip the first line so we can directly
            convert each line to tuple[int, int, int, int].
            """
            next(csvfile)
            frame = tuple((int(i), int(a), int(b), int(c))
                          for i, a, b, c in (
                              line.rstrip('\n').rstrip('\r').split(",")
                              for line in csvfile))

        return frame

    frames = tuple(assemble("/".join([folder_path, filename]))
                   for filename in listdir(folder_path)
                   if filename.endswith('.csv'))

    return frames


def clear() -> None:
    """
    Clear the display.
    """
    global display
    display.fill((0, 0, 0))
    display.write()


def df() -> str:
    """
    Checking file space free similar to Unix df.
    """
    s = statvfs('//')
    return ('{0} MB'.format((s[0]*s[3])/1048576))


def free(full=False) -> str:
    """
    Return free RAM as a percentage.
    """

    gc.collect()
    F = gc.mem_free()
    A = gc.mem_alloc()
    T = F+A
    P = 'FREE: {0:.4f}%'.format(F/T*100)
    if not full:
        return P
    else:
        return ('Total:{0} Free:{1} ({2})'.format(T, F, P))


def animate(frames: tuple[tuple[tuple[int, int, int, int]]]) -> None:
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

    # Pre-load animations in a tuple.
    animations = tuple(read_frames(folder) for folder in animation_paths)

    debug(free())

    while RUNNING:
        animate(animations[values['Channel']])
        sleep_ms(randint(int(values["Speed"]*500),
                         int(values["Speed"]*10_000)))


if __name__ == '__main__':
    try:
        clear()
        main()
    except Exception as e:
        debug(e)
        clear()
