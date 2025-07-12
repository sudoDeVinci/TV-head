from enum import Enum
from typing import Any, Optional, Tuple, TypeVar
from functools import lru_cache
import sys

T = TypeVar('T', bound='SelectorEnum')


class SelectorEnum():
    """
    Base Enum for menu selections with improved error handling.
    """

    NAC = None

    @classmethod
    def _missing_(cls, value: Any) -> Optional['SelectorEnum']:
        return cls.NAC

    @classmethod
    def members(cls) -> Optional[Tuple['SelectorEnum', ...]]:
        if not hasattr(cls, '__members__'):
            return None
        return tuple(ctype for _, ctype in cls.__members__.items())

    @classmethod
    def names(cls) -> Optional[Tuple[str, ...]]:
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


def parseIntInput(prompt: str = ">> ") -> int:
    """
    Take user input in a loop and attempt to parse an integer from it.
    
    Args:
        prompt: The prompt to display to the user
        
    Returns:
        The parsed integer value
    """
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                print("Please enter a value.")
                continue
            return int(user_input)
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled by user.")
            sys.exit(0)


def parseBoundedIntInput(upper: int, low: int, prompt: str = ">> ") -> int:
    """
    Parse integer input within specified bounds.
    
    Args:
        upper: Maximum allowed value (inclusive)
        low: Minimum allowed value (inclusive)
        prompt: The prompt to display to the user
        
    Returns:
        The parsed integer value within bounds
    """
    while True:
        value = parseIntInput(prompt)
        if low <= value <= upper:
            return value
        print(f"Input must be between {low} and {upper}. Please try again.")


def welcome() -> None:
    """Display welcome message."""
    print("\n" + "="*50)
    print("    Welcome to TV Head Controller (⌐ ͡■ ͜ʖ ͡■)")
    print("="*50 + "\n")


def config_loaded() -> None:
    """Display configuration loaded message."""
    print("✓ Configuration loaded successfully!\n")


def message_err(err: str) -> None:
    """
    Display error message with formatting.
    
    Args:
        err: The error message to display
    """
    print(f"\n⚠ ERROR: {err}\n")


# UI elements for selecting Image Mode
class ImageMode(SelectorEnum, Enum):
    BACK = 0
    SINGLE = 1
    MULTIPLE = 2
    SPRITE = 3


def ImageModeMenuPrintout() -> None:
    """Display the image mode selection menu."""
    print("\n" + "-"*30)
    print("SELECT IMAGE MODE")
    print("-"*30)
    print(f"  {ImageMode.BACK.value}: ← Back")
    print(f"  {ImageMode.SINGLE.value}: Single frame")
    print(f"  {ImageMode.MULTIPLE.value}: Multiple frames") 
    print(f"  {ImageMode.SPRITE.value}: Sprite Sheet")
    print("-"*30)


def ImageModeMenu() -> ImageMode:
    """Handle image mode menu selection."""
    members = ImageMode.members()
    if members is None:
        return ImageMode.NAC
    
    choice = parseBoundedIntInput(
        upper=len(members) - 1,
        low=ImageMode.BACK.value,
        prompt="Select option: "
    )
    return ImageMode.match(choice)


# UI elements for selecting image rotation
class RotationMode(SelectorEnum, Enum):
    BACK = 0
    ROTATE_90 = 1
    ROTATE_180 = 2
    ROTATE_270 = 3
    NONE = 4


def RotationModeMenuPrintout() -> None:
    """Display the rotation mode selection menu."""
    print("\n" + "-"*30)
    print("SELECT IMAGE ROTATION")
    print("-"*30)
    print(f"  {RotationMode.BACK.value}: ← Back")
    print(f"  {RotationMode.ROTATE_90.value}: Rotate 90° clockwise")
    print(f"  {RotationMode.ROTATE_180.value}: Rotate 180°")
    print(f"  {RotationMode.ROTATE_270.value}: Rotate 270°")
    print(f"  {RotationMode.NONE.value}: No rotation")
    print("-"*30)


def RotationModeMenu() -> RotationMode:
    """Handle rotation mode menu selection."""
    members = RotationMode.members()
    if members is None:
        return RotationMode.NAC
        
    choice = parseBoundedIntInput(
        upper=len(members) - 1,
        low=RotationMode.BACK.value,
        prompt="Select option: "
    )
    return RotationMode.match(choice)


# UI elements for selecting Image flip mode.
class FlipMode(SelectorEnum, Enum):
    BACK = 0
    VERTICAL_FLIP = 1
    HORIZONTAL_FLIP = 2
    VERTICAL_AND_HORIZONTAL_FLIP = 3
    NONE = 4


def FlipModeMenuPrintout() -> None:
    """Display the flip mode selection menu."""
    print("\n" + "-"*30)
    print("SELECT IMAGE FLIP")
    print("-"*30)
    print(f"  {FlipMode.BACK.value}: ← Back")
    print(f"  {FlipMode.VERTICAL_FLIP.value}: Vertical flip")
    print(f"  {FlipMode.HORIZONTAL_FLIP.value}: Horizontal flip")
    print(f"  {FlipMode.VERTICAL_AND_HORIZONTAL_FLIP.value}: Vertical and horizontal flip")
    print(f"  {FlipMode.NONE.value}: No flip")
    print("-"*30)


def FlipModeMenu() -> FlipMode:
    """Handle flip mode menu selection."""
    members = FlipMode.members()
    if members is None:
        return FlipMode.NAC
        
    choice = parseBoundedIntInput(
        upper=len(members) - 1,
        low=FlipMode.BACK.value,
        prompt="Select option: "
    )
    return FlipMode.match(choice)
