from tvlib._config import MatLike, UMat, Self
from enum import Enum
from cv2 import (ROTATE_90_COUNTERCLOCKWISE, ROTATE_180, ROTATE_90_CLOCKWISE,
                 flip, rotate)
from functools import partial


Flip = None
Rotation = None


def mapped_flip(image: MatLike | UMat, flp: Flip) -> MatLike | UMat:
    return flip(image, flp)


def mapped_rotate(image: MatLike | UMat, rot: Rotation) -> MatLike | UMat:
    return rotate(image, rot)


def nothing(image: MatLike | UMat,
            rot: Rotation = None,
            flip: Flip = None) -> MatLike | UMat:
    return image


class Rotation(Enum):
    """
    An enumeration representing different rotation transformations.

    Members:
        ROTATE_90 (partial):
            A partial function that rotates an image
            90 degrees counterclockwise.

        ROTATE_180 (partial):
            A partial function that rotates an image 180 degrees.

        ROTATE_270 (partial):
            A partial function that rotates an image 90 degrees clockwise.

        NONE (partial): A partial function that performs no rotation or flip.

    Methods:
        _missing_(cls, value: Self):
            Returns the NONE rotation if the given value is not
            found in the enumeration.

        __call__(self, *args):
            Calls the partial function associated with the enumeration value.
    """

    ROTATE_90 = partial(mapped_rotate, rot=ROTATE_90_COUNTERCLOCKWISE)
    ROTATE_180 = partial(mapped_rotate, rot=ROTATE_180)
    ROTATE_270 = partial(mapped_rotate, rot=ROTATE_90_CLOCKWISE)
    NONE = partial(nothing, rot=None, flip=None)

    def _missing_(cls, value: Self):
        return cls.NONE

    def __call__(self, *args):
        return self.value(*args)


class Flip(Enum):
    """
    An enumeration representing different types of image flip transformations.

    Members:
        VERTICAL_FLIP (partial):
            A partial function that performs a vertical flip on an image.

        HORIZONTAL_FLIP (partial):
            A partial function that performs a horizontal flip on an image.

        VERTICAL_AND_HORIZONTAL_FLIP (partial):
            A partial function that performs both vertical and
            horizontal flips on an image.

        NONE (partial):
            A partial function that performs no transformation on an image.

    Methods:
        _missing_(cls, value: Self) -> Flip:
            Returns the NONE transformation if the provided value is
            not a valid Flip member.

        __call__(self, *args):
            Calls the partial function associated with the Flip member.
    """
    VERTICAL_FLIP = partial(mapped_flip, flp=1)
    HORIZONTAL_FLIP = partial(mapped_flip, flp=0)
    VERTICAL_AND_HORIZONTAL_FLIP = partial(mapped_flip, flp=-1)
    NONE = partial(nothing, rot=None, flip=None)

    def _missing_(cls, value: Self):
        return cls.NONE

    def __call__(self, *args):
        return self.value(*args)
