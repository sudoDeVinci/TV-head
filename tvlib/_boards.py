import functools
from enum import Enum
from typing import Optional


class BoardType:
    UNKNOWN = "unknown"

    @classmethod
    @functools.lru_cache(maxsize=None)
    def _match(cls, board_name: str) -> Optional['BoardType']:
        if not hasattr(cls, '__members__'):
            return None

        for _, bt in cls.__members__.items():
            if isinstance(bt.value, type) and issubclass(bt.value, BoardType):
                res = bt.value._match(board_name)
                if res is not None:
                    return res
            elif board_name == bt.value:
                return bt
        return None

    @classmethod
    @functools.lru_cache(maxsize=None)
    def match(cls, board_name: str) -> 'BoardType':
        board_name = board_name.lower()
        result = cls._match(board_name)
        return cls.UNKNOWN if result is None else result

    @classmethod
    @functools.lru_cache(maxsize=None)
    def __contains__(cls, board_name: str) -> bool:
        return BoardType.match(board_name) != cls.UNKNOWN


class ESP32Boards(BoardType, Enum):
    """
    ESP32 board types.
    """
    ESP32 = "esp32"
    ESP32S2 = "esp32s2"
    ESP32S3 = "esp32s3"


class RaspberryPiBoards(BoardType, Enum):
    """
    Raspberry pi board types.
    """
    RASPBERRY_PI_3 = "raspberry pi 3"
    RASPBERRY_PI_4 = "raspberry pi 4"
    RASPBERRY_PI_PICO = "raspberry pi pico"


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
