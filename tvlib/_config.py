from cv2 import imread, IMREAD_COLOR,resize, Mat, compare, CMP_NE, findNonZero
from numpy import array_equal, ndarray, array, flip, uint8, nonzero, column_stack
import numpy.typing
from _fileio import *
from _boards import BoardCatalog
from os import listdir

# For typing, these are inexact because out memory layout differences between Mat and UMat
type NDArray = numpy.typing.NDArray[any]
type MatLike = numpy.typing.NDArray[numpy.uint8]

IMAGE_DIR:str = mkdir("animations")
CSV_DIR:str = mkdir("csvs")
DEBUG:bool = True
CONFIG_FILE:str = "conf.toml"
# Header for frame csvs
HEADER: Tuple[str] = ('index', 'blue', 'green', 'red')

# If debug is True, print. Otherwise, do nothing.
def out01(x:str) -> None:
    print(x)

def out02(x:str) -> None:
    pass

debug = out01 if DEBUG else out02


class Config:
    """
    Static Config class to hold configuration details.
    """
    _height: int = None
    _width: int = None
    _board_type: BoardCatalog = BoardCatalog.UNKNOWN
    _required_keys:Dict = {
        "resolution": ["width", "height"],
        "target": ["board"]
    }

    @staticmethod
    def _populate(width: int, height: int, board_type: BoardCatalog):
        """
        Populate the Config class with the given width, height and BoardCatalog.
        """
        Config._width = width
        Config._height = height
        Config._board_type = board_type
    
    @staticmethod
    def _config_valid(confdict:Dict) -> bool:
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
        if not path.exists(CONFIG_FILE):
            debug(f"Error: File '{CONFIG_FILE}' not found.")
            return None
        
        data = load_toml(CONFIG_FILE)
        if data is None:
            debug(f"Error: Config file '{CONFIG_FILE}' is None.")
            return None

        if not Config._config_valid(data):
            debug(f"Error: Config file '{CONFIG_FILE}' is invalid.")
            return None
        
        board = BoardCatalog.match(data["target"]["board"])
        Config._populate(data["resolution"]["width"], data["resolution"]["height"], board)

    @staticmethod
    def get_res() -> Tuple[int, int]:
        """
        Get the resolution of the display.
        """
        return Config._width, Config._height
    
    @staticmethod
    def get_board_type() -> BoardCatalog:
        """
        Get the board type.
        """
        return Config._board_type

if __name__ == "__main__":
    Config.load()
    debug(Config.get_board_type())
    debug(Config.get_res())