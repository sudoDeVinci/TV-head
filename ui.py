from tvlib._config import *
from tvlib.transformations import *


class SelectorEnum(Enum):
    """
    Base Enum for manu selections.
    """
    BACK = 0

    @classmethod
    def _missing_(cls, value):
        return cls.BACK
    
    @classmethod
    def members(cls) -> Tuple[Self]:
        return tuple(ctype for _, ctype in cls.__members__.items())
    
    @classmethod
    def names(cls) -> Tuple[str]:
        return tuple(names for names, _ in cls.__members__.items())

def parseIntInput() -> int:
    """
    Take user input in a loop and attempt to parse a string from it.
    """
    out: int
    while True:
        try:
            out = int(input(str))
            break
        except ValueError:
            print("Invalid input. Try again.")
            continue
    
    return out

def parseBoundedIntInput(upper: int, low: int) -> int:
    out: int
    while True:
        try:
            out = parseIntInput()
            if out < low or out > upper:
                print("Invalid input. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Try again.")
            continue
    




def welcome() -> None:
    print("\n\tWelcome (⌐ ͡■ ͜ʖ ͡■) \n\n------------- WELCOME ------------\n")

def config_loaded() -> None:
    print("\n\tWelcome (⌐ ͡■ ͜ʖ ͡■) \n\n------------- WELCOME ------------\n")



class ImageModeSelect(SelectorEnum):
    SINGLE = 1
    MULTIPLE = 2
    SPRITE = 3

def ImageModeSelect():
    pass