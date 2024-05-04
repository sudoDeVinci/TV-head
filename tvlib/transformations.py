from tvlib._config import *
from enum import Enum
from cv2 import ROTATE_90_COUNTERCLOCKWISE, ROTATE_180, ROTATE_90_CLOCKWISE, flip, rotate
from functools import partial

type Flip = None
type Rotation = None

def mapped_flip(image: MatLike | UMat, flp: Flip):
    return flip(image, flp)

def mapped_rotate(image: MatLike | UMat, rot: Rotation):
    return rotate(image, rot)

def nothing(): pass


class Rotation(Enum):
    ROTATE_90 = partial(mapped_flip, flp = ROTATE_90_COUNTERCLOCKWISE)
    ROTATE_180 = partial(mapped_flip, flp = ROTATE_180)
    ROTATE_270 = partial(mapped_flip, flp = ROTATE_90_CLOCKWISE)
    NONE = nothing


class Flip(Enum):
    VERTICAL_FLIP = partial(mapped_rotate, rot = 1)
    HORIZONTAL_FLIP = partial(mapped_rotate, rot = 0)
    VERTICAL_AND_HORIZONTAL_FLIP = partial(mapped_rotate, rot = -1)
    NONE = None


def _realign(img: MatLike, tw: int, th: int) -> NDArray:
    """
    Reorder image rows to fit strip design, then flatten image into 2D array.
    """
    height, width, _ = img.shape
    target_dimensions = (tw, th)
    if target_dimensions!=(width, height):
        img = resize(img, target_dimensions)
        height, width, _ = img.shape
    # Reverse the order of pixels in every second row
    img[1::2, :] = flip(img[1::2, :], axis=1)
    return img.reshape(-1, img.shape[-1])

