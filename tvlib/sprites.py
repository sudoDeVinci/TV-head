import pygame
from pygame.locals import *
from tvlib._config import *


def _filter_pixels(arr: NDArray, value: int) -> NDArray:
    """
    Given a List of 3D numpy arrays representing images,
    filter out all images that are completely a single value
    """
    return array([img for img in arr if not (img == value).all()])


def sprite_to_array(size: Tuple[int, int], file: str, background_value:int = 0) -> NDArray:
    """
    Given a sprite sheet where the height and width of the sprites are known,
    extract each sprite to a seprate image and save them sequentially in an array.
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

    # return array([img for img in sprites])
    return _filter_pixels(array(sprites, dtype = uint8), value=background_value)
