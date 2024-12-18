import pygame
from tvlib._config import MatLike
from numpy import array, uint8
from typing import Tuple
from cv2 import cvtColor, COLOR_RGB2BGR


def _filter_pixels(arr: MatLike, value: int) -> MatLike:
    """
    Given a List of 3D numpy arrays representing images,
    filter out all images that are completely a single value
    """
    return array([img for img in arr if not (img == value).all()],
                 dtype=uint8)


def sprite_to_array(size: Tuple[int, int],
                    file: str,
                    background_value: int = 0) -> MatLike:
    """
    Converts a sprite sheet into an array of individual sprites.
    Args:
        size (Tuple[int, int]):
            The width and height of each sprite.

        file (str):
            The file path to the sprite sheet image.

        background_value (int, optional):
            The value to use for background pixels. Defaults to 0.

    Returns:
        MatLike: A numpy array containing the individual sprites.
    """

    width, height = size
    sprites = []

    pygame.display.set_mode(size)
    sheet = pygame.image.load(file)
    sheet_rect = sheet.get_rect()

    for y in range(0, sheet_rect.height - height + 1, height):
        for x in range(0, sheet_rect.width - width + 1, width):
            rect = pygame.Rect(x, y, width, height)
            img = sheet.subsurface(rect)
            imgdata = pygame.surfarray.array3d(img)
            imgdata = imgdata.swapaxes(0, 1)
            imgdata = cvtColor(imgdata, COLOR_RGB2BGR)
            sprites.append(imgdata)

    return _filter_pixels(array(sprites, dtype=uint8),
                          value=background_value)
