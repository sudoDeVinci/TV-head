from tvlib._config import *
from enum import Enum
from cv2 import ROTATE_90_COUNTERCLOCKWISE, ROTATE_180, ROTATE_90_CLOCKWISE, flip, rotate, imread, imshow, waitKey
from functools import partial

Flip = None
Rotation = None

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

    def _missing_(cls, value: Self):
        return cls.NONE

    def __call__(self, *args):
        return self.value(*args)

class Flip(Enum):
    VERTICAL_FLIP = partial(mapped_flip, flp = 1)
    HORIZONTAL_FLIP = partial(mapped_flip, flp = 0)
    VERTICAL_AND_HORIZONTAL_FLIP = partial(mapped_flip, flp = -1)
    NONE = partial(nothing, rot = None, flip = None)

    def _missing_(cls, value: Self):
        return cls.NONE

    def __call__(self, *args):
        return self.value(*args)

