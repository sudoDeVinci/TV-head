from tvlib._config import *
from tvlib.transformations import *
from typing import Any, Optional, Tuple
from functools import lru_cache

class SelectorEnum():
    """
    Base Enum for menu selections.
    """

    @classmethod
    def _missing_(cls, value: Any) -> Optional['SelectorEnum']:
        return cls.BACK
    
    @classmethod
    def members(cls) -> Tuple[Self] | None:
        if not hasattr(cls, '__members__'): return None
        return tuple(ctype for _, ctype in cls.__members__.items())
    
    @classmethod
    def names(cls) -> Tuple[str] | None:
        if not hasattr(cls, '__members__'): return None
        return tuple(names for names, _ in cls.__members__.items())
    
    @classmethod
    @lru_cache(maxsize=None)
    def match(cls, choice: int) -> Optional['SelectorEnum']:
        if not hasattr(cls, '__members__'):
            return None
        
        for _, ctype in cls.__members__.items():
            if choice == ctype.value:
                return ctype
            
        return cls.BACK

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


# UI elements for selecting Image Mode

class ImageMode(SelectorEnum, Enum):
    BACK = 0
    SINGLE = 1
    MULTIPLE = 2
    SPRITE = 3
    
def ImageModeMenuPrintout() -> None:
    out = f"""
    {ImageMode.BACK.value}: Back
    {ImageMode.SINGLE.value}: Single frame
    {ImageMode.MULTIPLE.value}: Multiple frames
    {ImageMode.SPRITE.value}: Sprite Sheet
    """
    print(out)

def ImageModeMenu() -> ImageMode:
    choice = parseBoundedIntInput(len(ImageMode.members()) - 1, ImageMode.BACK)
    return ImageMode.match(choice)
    

# UI elements for selecting image rotation

class RotationMode(SelectorEnum, Enum):
    BACK = 0
    ROTATE_90 = 1
    ROTATE_180 = 2
    ROTATE_270 = 3
    NONE = 4
    
def rotationModeMenuPrintout() -> None:
    out = f"""
    {RotationMode.BACK.value}: Back
    {RotationMode.ROTATE_90.value}: Rotate 90° clockwise
    {RotationMode.ROTATE_180.value}: Rotate 180°
    {RotationMode.ROTATE_270.value}: Rotate 270°
    {RotationMode.NONE.value}: No rotation
    """
    print(out)
    

def rotationModeMenu() -> RotationMode:
    choice = parseBoundedIntInput(len(RotationMode.members()) - 1, RotationMode.BACK)
    return RotationMode.match(choice)


# UI elements for selecting Image flip mode.

class FlipMode(SelectorEnum, Enum):
    BACK = 0
    VERTICAL_FLIP = 1
    HORIZONTAL_FLIP = 2
    VERTICAL_AND_HORIZONTAL_FLIP = 3
    NONE = 4
    

def flipModeMenuPrintout() -> None:
    out = f"""
    {FlipMode.BACK.value}: Back
    {FlipMode.VERTICAL_FLIP.value}: Vertical flip
    {FlipMode.HORIZONTAL_FLIP.value}: Horizontal flip
    {FlipMode.VERTICAL_AND_HORIZONTAL_FLIP.value}: Vertical and horizontal flip
    {FlipMode.NONE.value}: No flip
    """
    print(out)


def flipModeMenu() -> FlipMode:
    choice = parseBoundedIntInput(len(FlipMode.members()) - 1, FlipMode.BACK)
    return FlipMode.match(choice)

