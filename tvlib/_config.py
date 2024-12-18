import numpy.typing
from tvlib._boards import BoardCatalog
from tvlib._fileio import load_toml, FOLDERS, out01, out02

from typing import Any, Dict, Tuple, LiteralString
from os import path

HEADER: Tuple[LiteralString] = ('index', 'blue', 'green', 'red')
DEBUG: bool = True
debug = out01 if DEBUG else out02

# For typing, these are inexact because of memory
# layout differences between Mat and UMat
NDArray = numpy.typing.NDArray[Any]
MatLike = numpy.typing.NDArray[numpy.uint8]
UMat = numpy.typing.NDArray[numpy.uint8]


class Config:
    """
    Static Config class to hold configuration details.

    Example:
    ```Python
        Config.load()
        debug(Config.boardtype())
        debug(Config.resolution())
    ```
    """
    _height: int | None = None
    _width: int | None = None
    _board_type: BoardCatalog = BoardCatalog.UNKNOWN
    _required_keys: Dict = {
        "resolution": ["width", "height"],
        "target": ["board"]
    }

    @staticmethod
    def _populate(width: int, height: int, board_type: BoardCatalog):
        """
        Populate the Config class with the given width,
        height and BoardCatalog.
        """
        Config._width = width
        Config._height = height
        Config._board_type = board_type

    @staticmethod
    def _config_valid(confdict: Dict) -> bool:
        if confdict is None or not isinstance(confdict, dict):
            return False

        for key, subkeys in Config._required_keys.items():
            if confdict[key] is None:
                return False
            if key not in confdict:
                return False
            if not all(subkey in confdict[key] for subkey in subkeys):
                return False

        return True

    @staticmethod
    def load() -> None:
        """
        Load the configuration file and populate with its details.
        """

        conf = FOLDERS.CONFIG_FILE.value

        if not path.exists(conf):
            debug(f"Error: File '{conf}' not found.")
            return None

        data = load_toml(conf)
        if data is None:
            debug(f"Error: Config file '{conf}' is None.")
            return None

        if not Config._config_valid(data):
            debug(f"Error: Config file '{conf}' is invalid.")
            return None

        board = BoardCatalog.match(data["target"]["board"])
        Config._populate(data["resolution"]["width"],
                         data["resolution"]["height"],
                         board)

    @staticmethod
    def resolution() -> Tuple[int, int]:
        """
        Get the resolution of the display.
        """
        return (Config._width, Config._height)

    @staticmethod
    def boardtype() -> BoardCatalog:
        """
        Get the board type.
        """
        return Config._board_type
