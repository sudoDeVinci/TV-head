from tvlib._config import *
from enum import Enum
from cv2 import ROTATE_90_COUNTERCLOCKWISE, ROTATE_180, ROTATE_90_CLOCKWISE, flip, rotate, imread, imshow, waitKey
from functools import partial

type Flip = None
type Rotation = None

def mapped_flip(image: MatLike | UMat, flp: Flip) -> MatLike | UMat:
    return flip(image, flp)

def mapped_rotate(image: MatLike | UMat, rot: Rotation) -> MatLike | UMat:
    return rotate(image, rot)

def nothing(image: MatLike | UMat, rot: Rotation = None, flip: Flip = None) -> MatLike | UMat:
    return image

class Rotation(Enum):
    ROTATE_90 = partial(mapped_rotate, rot = ROTATE_90_COUNTERCLOCKWISE)
    ROTATE_180 = partial(mapped_rotate, rot = ROTATE_180)
    ROTATE_270 = partial(mapped_rotate, rot = ROTATE_90_CLOCKWISE)
    NONE = partial(nothing, rot = None, flip = None)

    def __call__(self, *args):
        return self.value(*args)

class Flip(Enum):
    VERTICAL_FLIP = partial(mapped_flip, flp = 1)
    HORIZONTAL_FLIP = partial(mapped_flip, flp = 0)
    VERTICAL_AND_HORIZONTAL_FLIP = partial(mapped_flip, flp = -1)
    NONE = partial(nothing, rot = None, flip = None)

    def __call__(self, *args):
        return self.value(*args)


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





