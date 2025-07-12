"""
TV Head Library

A library for processing and displaying images on LED matrix displays
for TV Head cosplay projects.
"""

from .transformations import Rotation, Flip
from ._config import Config
from .comparator import convert_all, convert_dir, convert_images
from .sprites import sprite_to_array

__version__ = "1.0.0"
__author__ = "Your Name"

__all__ = [
    "Rotation",
    "Flip", 
    "Config",
    "convert_all",
    "convert_dir",
    "convert_images",
    "sprite_to_array"
]