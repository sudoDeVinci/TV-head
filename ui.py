from enum import Enum
from typing import Any, Optional, Tuple, Self
from functools import lru_cache


class SelectorEnum():
    """
    Base Enum for menu selections.
    """

    NAC = None

    @classmethod
    def _missing_(cls, value: Any) -> Optional['SelectorEnum']:
        return cls.NAC

    @classmethod
    def members(cls) -> Tuple[Self] | None:
        if not hasattr(cls, '__members__'):
            return None
        return tuple(ctype for _, ctype in cls.__members__.items())

    @classmethod
    def names(cls) -> Tuple[str] | None:
        if not hasattr(cls, '__members__'):
            return None
        return tuple(names for names, _ in cls.__members__.items())

    @classmethod
    @lru_cache()
    def match(cls, choice: int) -> Optional['SelectorEnum']:
        if not hasattr(cls, '__members__'):
            return None

        for _, ctype in cls.__members__.items():
            if choice == ctype.value:
                return ctype

        return cls.NAC


def parseIntInput() -> int:
    """
    Take user input in a loop and attempt to parse a string from it.
    """
    out: int
    while True:
        try:
            out = int(input(">> "))
            break
        except ValueError:
            print("Invalid input. Try again.")
            continue

    return out


def parseBoundedIntInput(upper: int, low: int) -> int:
    out: int
    while True:
        out = parseIntInput()
        if out < low or out > upper:
            print("Invalid input. Try again.")
            continue
        break
    return out


def welcome() -> None:
    print("\n\tWelcome (⌐ ͡■ ͜ʖ ͡■) \n\n------------- WELCOME ------------\n")


def config_loaded() -> None:
    print("\n\tᕕ(ᐛ)ᕗ Config Loaded!\n")


def message_err(err: str):
    print(f"\n\tERR:-> {err}")


# UI elements for selecting Image Mode
class ImageMode(SelectorEnum, Enum):
    BACK = 0
    SINGLE = 1
    MULTIPLE = 2
    SPRITE = 3


def ImageModeMenuPrintout() -> None:
    out = f"""Select Image Mode:\n
    {ImageMode.BACK.value}: Back
    {ImageMode.SINGLE.value}: Single frame
    {ImageMode.MULTIPLE.value}: Multiple frames
    {ImageMode.SPRITE.value}: Sprite Sheet
    """
    print(out)


def ImageModeMenu() -> ImageMode:
    choice = parseBoundedIntInput(len(ImageMode.members()) - 2,
                                  ImageMode.BACK.value)
    return ImageMode.match(choice)


# UI elements for selecting image rotation
class RotationMode(SelectorEnum, Enum):
    BACK = 0
    ROTATE_90 = 1
    ROTATE_180 = 2
    ROTATE_270 = 3
    NONE = 4


def RotationModeMenuPrintout() -> None:
    out = f"""Select Image Rotation:
    {RotationMode.BACK.value}: Back
    {RotationMode.ROTATE_90.value}: Rotate 90° clockwise
    {RotationMode.ROTATE_180.value}: Rotate 180°
    {RotationMode.ROTATE_270.value}: Rotate 270°
    {RotationMode.NONE.value}: No rotation
    """
    print(out)


def RotationModeMenu() -> RotationMode:
    choice = parseBoundedIntInput(len(RotationMode.members()) - 2,
                                  RotationMode.BACK.value)
    return RotationMode.match(choice)


# UI elements for selecting Image flip mode.
class FlipMode(SelectorEnum, Enum):
    BACK = 0
    VERTICAL_FLIP = 1
    HORIZONTAL_FLIP = 2
    VERTICAL_AND_HORIZONTAL_FLIP = 3
    NONE = 4


def FlipModeMenuPrintout() -> None:
    out = f"""Select Image Flip
    {FlipMode.BACK.value}: Back
    {FlipMode.VERTICAL_FLIP.value}: Vertical flip
    {FlipMode.HORIZONTAL_FLIP.value}: Horizontal flip
    {FlipMode.VERTICAL_AND_HORIZONTAL_FLIP.value}: Vertical and horizontal flip
    {FlipMode.NONE.value}: No flip
    """
    print(out)


def FlipModeMenu() -> FlipMode:
    choice = parseBoundedIntInput(len(FlipMode.members()) - 2,
                                  FlipMode.BACK.value)
    return FlipMode.match(choice)
