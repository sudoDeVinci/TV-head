from tvlib import *
from ui import *

def main ():
    welcome()
    Config.load()
    config_loaded()
    
    resolution = Config.get_res()
    
    
def imageModeSelect() -> ImageMode:
    ImageModeMenuPrintout()
    return ImageModeMenu()
    

def rotationModeSelect() -> Rotation:
    RotationModeMenuPrintout()
    rotation = RotationModeMenu()
    
    match rotation:
        case RotationMode.BACK:
            return None
        case RotationMode.ROTATE_90:
            return Rotation.ROTATE_90
        case RotationMode.ROTATE_180:
            return Rotation.ROTATE_180
        case RotationMode.ROTATE_270:
            return Rotation.ROTATE_270
        case RotationMode.NONE:
            return Rotation.NONE
        case _:
            raise ValueError("Invalid rotation mode")
        

def flipModeSelect() -> FlipMode:
    FlipModeMenuPrintout()
    flip = FlipModeMenu()
    
    match flip:
        case FlipMode.BACK:
            return None
        case FlipMode.VERTICAL_FLIP:
            return Flip.VERTICAL_FLIP
        case FlipMode.HORIZONTAL_FLIP:
            return Flip.HORIZONTAL_FLIP
        case FlipMode.VERTICAL_AND_HORIZONTAL_FLIP:
            return Flip.VERTICAL_AND_HORIZONTAL_FLIP
        case FlipMode.NONE:
            return Flip.NONE
        case _:
            raise ValueError("Invalid flip mode")
        

