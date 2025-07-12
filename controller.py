from dataclasses import dataclass
from typing import Optional
from tvlib.transformations import Flip, Rotation
from tvlib._config import Config
from ui import (ImageMode, ImageModeMenu, ImageModeMenuPrintout,
                RotationMode, RotationModeMenu, RotationModeMenuPrintout,
                FlipMode, FlipModeMenu, FlipModeMenuPrintout,
                message_err, welcome, config_loaded)


@dataclass
class ImageSettings:
    """Encapsulate image processing settings."""
    rotation: Rotation = Rotation.NONE
    flip: Flip = Flip.NONE
    imagemode: Optional[ImageMode] = None
    resolution: Optional[tuple[int, int]] = None
    
    def reset(self) -> None:
        """Reset all settings to defaults."""
        self.rotation = Rotation.NONE
        self.flip = Flip.NONE
        self.imagemode = None
        self.resolution = None


class TVHeadController:
    """Main controller for TV Head configuration interface."""
    
    def __init__(self):
        self.settings = ImageSettings()
        self.done = False
        self.ERR_MSG = "Please select a choice from the menu given."
    
    def initialize(self) -> bool:
        """Initialize the controller and load configuration."""
        try:
            welcome()
            Config.load()
            config_loaded()
            self.settings.resolution = Config.resolution()
            return True
        except Exception as e:
            message_err(f"Failed to initialize: {e}")
            return False
    
    def run(self) -> Optional[ImageSettings]:
        """Run the main configuration flow."""
        if not self.initialize():
            return None
            
        if self._select_image_mode():
            return self.settings
        return None


    def _select_image_mode(self) -> bool:
        """Handle image mode selection."""
        while True:
            ImageModeMenuPrintout()
            mode = ImageModeMenu()
            if mode is ImageMode.NAC:
                message_err(self.ERR_MSG)
                continue
            elif mode is ImageMode.BACK:
                return False
            else:
                self.settings.imagemode = mode
                return self._select_rotation_mode()

    def _select_rotation_mode(self) -> bool:
        """Handle rotation mode selection."""
        while True:
            RotationModeMenuPrintout()
            mode = RotationModeMenu()
            if mode is RotationMode.NAC:
                message_err(self.ERR_MSG)
                continue
            elif mode is RotationMode.BACK:
                return False
            else:
                self._apply_rotation(mode)
                return self._select_flip_mode()

    def _apply_rotation(self, mode: RotationMode) -> None:
        """Apply the selected rotation mode."""
        rotation_map = {
            RotationMode.ROTATE_90: Rotation.ROTATE_90,
            RotationMode.ROTATE_180: Rotation.ROTATE_180,
            RotationMode.ROTATE_270: Rotation.ROTATE_270,
            RotationMode.NONE: Rotation.NONE,
        }
        self.settings.rotation = rotation_map.get(mode, Rotation.NONE)

    def _select_flip_mode(self) -> bool:
        """Handle flip mode selection."""
        while True:
            FlipModeMenuPrintout()
            mode = FlipModeMenu()
            if mode is FlipMode.NAC:
                message_err(self.ERR_MSG)
                continue
            elif mode is FlipMode.BACK:
                return False
            else:
                self._apply_flip(mode)
                self.done = True
                return True

    def _apply_flip(self, mode: FlipMode) -> None:
        """Apply the selected flip mode."""
        flip_map = {
            FlipMode.VERTICAL_FLIP: Flip.VERTICAL_FLIP,
            FlipMode.HORIZONTAL_FLIP: Flip.HORIZONTAL_FLIP,
            FlipMode.VERTICAL_AND_HORIZONTAL_FLIP: Flip.VERTICAL_AND_HORIZONTAL_FLIP,
            FlipMode.NONE: Flip.NONE,
        }
        self.settings.flip = flip_map.get(mode, Flip.NONE)


# Legacy function interfaces for backward compatibility
def init() -> bool:
    """Initialize the TV Head controller (legacy interface)."""
    controller = TVHeadController()
    return controller.initialize()


def main() -> Optional[ImageSettings]:
    """Run the main controller flow (legacy interface)."""
    controller = TVHeadController()
    return controller.run()


def imageModeSelect() -> None:
    """Legacy function - use TVHeadController class instead."""
    ERR = "Please select a choice from the menu given."
    global IMAGE_SETTINGS

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
            IMAGE_SETTINGS['imagemode'] = mode
            rotationModeSelect()
            if done:
                return None


def rotationModeSelect() -> None:
    """Legacy function - use TVHeadController class instead."""
    ERR = "Please select a choice from the menu given."
    global IMAGE_SETTINGS

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
                    IMAGE_SETTINGS['rotation'] = Rotation.ROTATE_90
                case RotationMode.ROTATE_180:
                    IMAGE_SETTINGS['rotation'] = Rotation.ROTATE_180
                case RotationMode.ROTATE_270:
                    IMAGE_SETTINGS['rotation'] = Rotation.ROTATE_270
                case RotationMode.NONE:
                    IMAGE_SETTINGS['rotation'] = Rotation.NONE
                case _:
                    IMAGE_SETTINGS['rotation'] = Rotation.NONE

            flipModeSelect()
            if done:
                return None


def flipModeSelect() -> FlipMode:
    """Legacy function - use TVHeadController class instead."""
    ERR = "Please select a choice from the menu given."
    global IMAGE_SETTINGS
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
                    IMAGE_SETTINGS['flip'] = Flip.VERTICAL_FLIP
                case FlipMode.HORIZONTAL_FLIP:
                    IMAGE_SETTINGS['flip'] = Flip.HORIZONTAL_FLIP
                case FlipMode.VERTICAL_AND_HORIZONTAL_FLIP:
                    IMAGE_SETTINGS['flip'] = Flip.VERTICAL_AND_HORIZONTAL_FLIP
                case FlipMode.NONE:
                    IMAGE_SETTINGS['flip'] = Flip.NONE
                case _:
                    IMAGE_SETTINGS['flip'] = Flip.NONE
            done = True


# Legacy global variables for backward compatibility
done: bool = False
IMAGE_SETTINGS = {
    'rotation': Rotation.NONE,
    'flip': Flip.NONE,
    'imagemode': None
}
