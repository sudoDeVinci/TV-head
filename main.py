from tvlib.comparator import *
from tvlib.transformations import *
from tvlib.sprites import *
from tvlib.padder import *
from cv2 import imshow, waitKey, destroyAllWindows
from colorama import init, Fore, Back, Style
import ui

ui.welcome()


Config.load()
resolution = Config.get_res()
width, height = resolution


ui.config_loaded()



"""
CURRENTLY ONLY AN EXAMPLE.

filename = '01-smile'
images = sprite_to_array(size = (8, 20), file = f"animations/{filename}.png")
print(f"Number of Images: {len(images)}")

frames = comparator(IMAGES = images, width = width, height = height, rotator = Rotation.ROTATE_90)
save_frames_json(frames, filename)
"""

convert_all((10, 10), Rotation.NONE, Flip.NONE)