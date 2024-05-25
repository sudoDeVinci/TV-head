from tvlib.comparator import *
from tvlib.transformations import *
from cv2 import imshow, waitKey
from colorama import init, Fore, Back, Style

Config.load()
resolution = Config.get_res()

convert_all(resolution)
