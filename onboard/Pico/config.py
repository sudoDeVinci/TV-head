from typing import Dict, Tuple
from micropython import const
from os import listdir, ilistdir


# If debug is True, our debug lines throughtout the code will print. Otherwise, do nothing
DEBUG: bool = True


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


debug = out02 if DEBUG else out01

# Variable to keep running script or not
RUNNING: bool = True

# Variables to define constant labels
BRIGHTNESS: str = const("Brightness")
CHANNEL: str = const("Channel")
SPEED: str = const("Speed")

# Folder for animation csvs
ANIMATION_FOLDER: str = "/csvs/"

# Pin number to address
P: int = const(16)
# Number of leds to address
N: int = const(100)

# Render variable values for playing animations.
RENDER_VALUES: Dict[str, int | float] = {
    BRIGHTNESS: 0.1,
    SPEED: 1,
    CHANNEL: 1
}


def get_animation_paths(folder_path: str = ANIMATION_FOLDER) -> Tuple[str]:
    global ANIMATION_FOLDER
    """
    Get a tuple of the animation folder paths.
    """
    return tuple(ANIMATION_FOLDER+file[0]
                 for file in ilistdir(folder_path) if file[1] == 0x4000)


def read_frames(folder_path: str) -> Tuple[Tuple[Tuple[int, int, int, int]]]:
    """
    Read the frames within a given animation
    folder and return it as a tuple[index, r, g, b] of ints.
    """
    def assemble(filename: str) -> Tuple[Tuple[int, int, int, int]]:
        frame: Tuple[Tuple[int, int, int, int]] = None
        with open(filename, 'r', encoding="utf-8") as csvfile:
            """
            Skip the first line so we can directly convert
            each line to tuple[int, int, int, int].
            """
            next(csvfile)
            frame = tuple((int(i), int(a), int(b), int(c))
                          for i, a, b, c in
                          (line.rstrip('\n').rstrip('\r').split(",")
                           for line in csvfile))

        return frame

    frames = tuple(assemble("/".join([folder_path, filename]))
                   for filename in listdir(folder_path)
                   if filename.endswith('.csv'))

    return frames


# Pre-load animations in a Tuple.
animation_paths = get_animation_paths()
animation_amount = len(animation_paths)
animations = tuple(read_frames(folder) for folder in animation_paths)
