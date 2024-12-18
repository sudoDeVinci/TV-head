from tvlib.transformations import Flip, Rotation
from tvlib._config import Config
from ui import (ImageMode, ImageModeMenu, ImageModeMenuPrintout,
                RotationMode, RotationModeMenu, RotationModeMenuPrintout,
                FlipMode, FlipModeMenu, FlipModeMenuPrintout,
                message_err, welcome, config_loaded)

done: bool = False
IMAGE_SETTINGS = {
    'rotation': Rotation.NONE,
    'flip': Flip.NONE,
    'imagemode': None
}

ERR = "Please select a choice from the menu given."


def init():
    global IMAGE_SETTINGS
    welcome()
    Config.load()
    config_loaded()
    IMAGE_SETTINGS['resolution'] = Config.resolution()


def main():
    global IMAGE_SETTINGS
    imageModeSelect()


def imageModeSelect() -> None:
    global image_settings

    mode: ImageMode

    while True:
        ImageModeMenuPrintout()
        mode = ImageModeMenu()
        if mode is ImageMode.NAC:
            message_err(ERR)
            continue
        elif mode is ImageMode.BACK:
            return None

        else:
            image_settings['imagemode'] = mode
            rotationModeSelect()
            if done:
                return None


def rotationModeSelect() -> None:
    global image_settings

    mode: RotationMode

    while True:
        RotationModeMenuPrintout()
        mode = RotationModeMenu()
        if mode is RotationMode.NAC:
            message_err(ERR)
            continue

        elif mode is RotationMode.BACK:
            return None

        else:
            match mode:
                case RotationMode.BACK:
                    return None
                case RotationMode.ROTATE_90:
                    image_settings['rotation'] = Rotation.ROTATE_90
                case RotationMode.ROTATE_180:
                    image_settings['rotation'] = Rotation.ROTATE_180
                case RotationMode.ROTATE_270:
                    image_settings['rotation'] = Rotation.ROTATE_270
                case RotationMode.NONE:
                    image_settings['rotation'] = Rotation.NONE
                case _:
                    image_settings['rotation'] = Rotation.NONE

            flipModeSelect()
            if done:
                return None


def flipModeSelect() -> FlipMode:
    global image_settings
    global done

    mode: FlipMode

    while True:
        FlipModeMenuPrintout()
        mode = FlipModeMenu()

        if mode is FlipMode.NAC:
            message_err(ERR)
            continue

        elif mode is FlipMode.BACK:
            return None

        else:
            match mode:
                case FlipMode.BACK:
                    return None
                case FlipMode.VERTICAL_FLIP:
                    image_settings['flip'] = Flip.VERTICAL_FLIP
                case FlipMode.HORIZONTAL_FLIP:
                    image_settings['flip'] = Flip.HORIZONTAL_FLIP
                case FlipMode.VERTICAL_AND_HORIZONTAL_FLIP:
                    image_settings['flip'] = Flip.VERTICAL_AND_HORIZONTAL_FLIP
                case FlipMode.NONE:
                    image_settings['flip'] = Flip.NONE
                case _:
                    image_settings['flip'] = Flip.NONE
            done = True
