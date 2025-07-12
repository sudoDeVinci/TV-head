from __future__ import annotations
from functools import lru_cache
from enum import Enum
from typing import Optional, Type, Any


class BoardType:
    """Base class for board type definitions."""
    UNKNOWN = "unknown"

    @classmethod
    @lru_cache(maxsize=None)
    def _match(cls, board_name: str) -> Optional['BoardType']:
        """Internal method to match board names."""
        if not hasattr(cls, '__members__'):
            return None

        for _, bt in cls.__members__.items():
            if hasattr(bt, 'value') and isinstance(bt.value, type) and issubclass(bt.value, BoardType):
                res = bt.value._match(board_name)
                if res is not None:
                    return res
            elif hasattr(bt, 'value') and board_name == bt.value:
                return bt
        return None

    @classmethod
    @lru_cache(maxsize=None)
    def match(cls, board_name: str) -> 'BoardType':
        """
        Match a board name to a BoardType.
        
        Args:
            board_name: The name of the board to match
            
        Returns:
            The matching BoardType or UNKNOWN if not found
        """
        if not isinstance(board_name, str):
            return cls.UNKNOWN
            
        board_name = board_name.lower().strip()
        result = cls._match(board_name)
        return result if result is not None else cls.UNKNOWN

    @classmethod
    @lru_cache(maxsize=None)
    def __contains__(cls, board_name: str) -> bool:
        """Check if a board name is supported."""
        return cls.match(board_name) != cls.UNKNOWN


class ESP32Boards(BoardType, Enum):
    """
    ESP32 board types.
    """
    ESP32 = "esp32"
    ESP32S2 = "esp32s2"
    ESP32S3 = "esp32s3"
    ESP32C3 = "esp32c3"


class RaspberryPiBoards(BoardType, Enum):
    """
    Raspberry pi board types.
    """
    RASPBERRY_PI_3 = "raspberry pi 3"
    RASPBERRY_PI_4 = "raspberry pi 4"
    RASPBERRY_PI_PICO = "raspberry pi pico"
    RASPBERRY_PI_PICO_2 = "raspberry pi pico 2"


class BoardCatalog(BoardType, Enum):
    """
    Various board types for usage.
    """
    ESP32 = ESP32Boards
    RASPBERRY_PI = RaspberryPiBoards


if __name__ == "__main__":
    print(f"Matching via the match method: "
          f"{BoardCatalog.match('esp32') == ESP32Boards.ESP32}")
    print(f"Matching via .value attribute: "
          f"{BoardCatalog.ESP32.value.ESP32S3 == ESP32Boards.ESP32S3}")
