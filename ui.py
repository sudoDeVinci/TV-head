from tvlib._config import *
from tvlib.transformations import *
from typing import Any, Optional, Tuple
from functools import lru_cache

class SelectorEnum():
    """
    Base Enum for menu selections.
    """
    BACK = 0

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



class ImageMode(SelectorEnum, Enum):
    SINGLE = 1
    MULTIPLE = 2
    SPRITE = 3
    
def ImageModeMenuPrintout() -> None:
    out = f"""
    {SelectorEnum.BACK}: Back
    {ImageMode.SINGLE.value}: Single frame
    {ImageMode.MULTIPLE.value}: Multiple frames
    {ImageMode.SPRITE.value}: Sprite
    """
    print(out)

def ImageModeMenu() -> ImageMode:
    choice = parseBoundedIntInput(len(ImageMode.members()) - 1, SelectorEnum.BACK)
    return ImageMode.match(choice)
    

class RotationMode():
    ROTATE_90 = 1
    ROTATE_180 = 2
    ROTATE_270 = 3
    NONE = 4