from __future__ import annotations
from typing import TYPE_CHECKING, Union, Any, Optional
from enum import Enum
from functools import partial

try:
    from cv2 import (ROTATE_90_COUNTERCLOCKWISE, ROTATE_180, ROTATE_90_CLOCKWISE,
                     flip, rotate)
except ImportError:
    # Fallback for environments without OpenCV
    ROTATE_90_COUNTERCLOCKWISE = 0
    ROTATE_180 = 1
    ROTATE_90_CLOCKWISE = 2
    
    def flip(image: Any, flipCode: int) -> Any:
        """Fallback flip function."""
        return image
    
    def rotate(image: Any, rotateCode: int) -> Any:
        """Fallback rotate function."""
        return image

if TYPE_CHECKING:
    from tvlib._config import MatLike, UMat

# Type aliases for better readability
ImageType = Union['MatLike', 'UMat']


def mapped_flip(image: ImageType, flp: 'Flip') -> ImageType:
    """Apply flip transformation to image."""
    return flip(image, flp)


def mapped_rotate(image: ImageType, rot: 'Rotation') -> ImageType:
    """Apply rotation transformation to image."""
    return rotate(image, rot)


def nothing(image: ImageType,
            rot: Optional['Rotation'] = None,
            flip_param: Optional['Flip'] = None) -> ImageType:
    """No-op transformation function."""
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
        _missing_(cls, value):
            Returns the NONE rotation if the given value is not
            found in the enumeration.

        __call__(self, *args):
            Calls the partial function associated with the enumeration value.
    """

    ROTATE_90 = partial(mapped_rotate, rot=ROTATE_90_COUNTERCLOCKWISE)
    ROTATE_180 = partial(mapped_rotate, rot=ROTATE_180)
    ROTATE_270 = partial(mapped_rotate, rot=ROTATE_90_CLOCKWISE)
    NONE = partial(nothing, rot=None, flip_param=None)

    @classmethod
    def _missing_(cls, value: Any) -> 'Rotation':
        return cls.NONE

    def __call__(self, *args: Any) -> Any:
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
        _missing_(cls, value) -> Flip:
            Returns the NONE transformation if the provided value is
            not a valid Flip member.

        __call__(self, *args):
            Calls the partial function associated with the Flip member.
    """
    VERTICAL_FLIP = partial(mapped_flip, flp=1)
    HORIZONTAL_FLIP = partial(mapped_flip, flp=0)
    VERTICAL_AND_HORIZONTAL_FLIP = partial(mapped_flip, flp=-1)
    NONE = partial(nothing, rot=None, flip_param=None)

    @classmethod
    def _missing_(cls, value: Any) -> 'Flip':
        return cls.NONE

    def __call__(self, *args: Any) -> Any:
        return self.value(*args)
