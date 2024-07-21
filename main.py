from tvlib.comparator import *
from tvlib.transformations import *
from tvlib.sprites import *
from cv2 import imshow, waitKey
from colorama import init, Fore, Back, Style
import ui

ui.welcome()


Config.load()
resolution = Config.get_res()
width, height = resolution


ui.config_loaded()




filename = '01-smile'
images = sprite_to_array(size = resolution, file = f"animations/{filename}.png")
print(f"Number of Frames: {len(images)}")
frames = comparator(IMAGES = images, width = width, height = height, rotator = Rotation.ROTATE_90)
save_frames(frames, filename)

