from typing import *
from micropython import const

# If debug is True, our debug lines throughtout the code will print. Otherwise, do nothing
DEBUG:bool = False
def out01(x:str) -> None:
    pass
def out02(x:str) -> None:
    pass
debug = out01 if DEBUG else out02

# Variable to keep running script or not
RUNNING: bool = True

# Variables to define constant labels
BRIGHTNESS: str = "Brightness"
CHANNEL: str = "Channel"
SPEED: str = "Speed"

# Folder for animation csvs
ANIMATION_FOLDER:str = "/csvs/"

# Pin number to address
P: int = const(16)
# Number of leds to address
N: int = const(160)

# Render variable values for playing animations.
RENDER_VALUES: Dict[str, int | float] = {
    BRIGHTNESS: 0.15,
    SPEED: 1,
    CHANNEL: 4
}
