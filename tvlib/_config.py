from __future__ import annotations
from typing import Any, Dict, Tuple, LiteralString, Optional
from os import path
import logging

try:
    import numpy.typing
    NDArray = numpy.typing.NDArray[Any]
    MatLike = numpy.typing.NDArray[numpy.uint8]
    UMat = numpy.typing.NDArray[numpy.uint8]
except ImportError:
    # Fallback types for environments without NumPy
    NDArray = Any
    MatLike = Any
    UMat = Any

from tvlib._boards import BoardCatalog
from tvlib._fileio import load_toml, FOLDERS, out01, out02

HEADER: Tuple[LiteralString, ...] = ('index', 'blue', 'green', 'red')
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
    _height: Optional[int] = None
    _width: Optional[int] = None
    _board_type: BoardCatalog = BoardCatalog.UNKNOWN
    _required_keys: Dict[str, list[str]] = {
        "resolution": ["width", "height"],
        "target": ["board"]
    }

    @staticmethod
    def _populate(width: int, height: int, board_type: BoardCatalog) -> None:
        """
        Populate the Config class with the given width,
        height and BoardCatalog.
        """
        Config._width = width
        Config._height = height
        Config._board_type = board_type

    @staticmethod
    def _config_valid(confdict: Optional[Dict[str, Any]]) -> bool:
        """Validate configuration dictionary structure."""
        if confdict is None or not isinstance(confdict, dict):
            return False

        for key, subkeys in Config._required_keys.items():
            if key not in confdict:
                debug(f"Missing required key: {key}")
                return False
            if confdict[key] is None:
                debug(f"Key '{key}' is None")
                return False
            if not all(subkey in confdict[key] for subkey in subkeys):
                missing = [sk for sk in subkeys if sk not in confdict[key]]
                debug(f"Missing subkeys in '{key}': {missing}")
                return False

        return True

    @staticmethod
    def load() -> bool:
        """
        Load the configuration file and populate with its details.
        Returns True if successful, False otherwise.
        """
        conf = FOLDERS.CONFIG_FILE.value

        if not path.exists(conf):
            debug(f"Error: File '{conf}' not found.")
            return False

        data = load_toml(conf)
        if data is None:
            debug(f"Error: Config file '{conf}' could not be loaded.")
            return False

        if not Config._config_valid(data):
            debug(f"Error: Config file '{conf}' is invalid.")
            return False

        board = BoardCatalog.match(data["target"]["board"])
        Config._populate(data["resolution"]["width"],
                         data["resolution"]["height"],
                         board)
        debug("Configuration loaded successfully")
        return True

    @staticmethod
    def resolution() -> Tuple[int, int]:
        """
        Get the resolution of the display.
        Raises ValueError if config not loaded.
        """
        if Config._width is None or Config._height is None:
            raise ValueError("Configuration not loaded. Call Config.load() first.")
        return (Config._width, Config._height)

    @staticmethod
    def boardtype() -> BoardCatalog:
        """
        Get the board type.
        """
        return Config._board_type
    
    @staticmethod
    def is_loaded() -> bool:
        """Check if configuration has been loaded."""
        return Config._width is not None and Config._height is not None
