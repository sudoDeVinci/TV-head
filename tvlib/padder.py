"""
This script renames the sequencially numbered files with a new name with padded zeroes.
"""

from tvlib._config import *

def _find_digit_bound(filename: str) -> tuple[bool, int] | tuple[bool, None]:
    """
    Find the ending digit of a filename.
    If found, return true and the number.
    """
    #filename = filename[:-4]
    for i in range(1, len(filename)):
        i = 0-i
        if filename[i].isdigit():
            continue
        else:
            return (True, i)
    
    return (False, None)

def padder(base_path: str):
    """
    Traverse through the folders in a top-folder.
    """
    if path.isdir(base_path):
            for root, folders, __ in walk(base_path):
                for folder in folders:
                    base_path = path.join(root, folder)
                    if path.isdir(base_path):
                        _file_traverse(base_path)
                        

def _file_traverse(base_path: str):
    """
    Traverse through files in a directory. 
    If the fil ehas a number to it, pad
    """
    if path.isdir(base_path):
        for root, _, images in walk(base_path):
            for image in images:
                frame_path = path.join(root, image)
                if path.isfile(frame_path):
                    debug(path.basename(frame_path)[:-4])
                    filename = path.basename(frame_path)[:-4]
                    dirname = path.basename(path.dirname(frame_path))
                    _padded_rename(filename, dirname, frame_path)


def _padded_rename(filename: str, dirname: str, frame_path: str) -> None:
    """
    Attempt to rename a file if its ending number is found.
    """
    found, digit = _find_digit_bound(filename)
    if found:
        new_filename_prefix = filename[:(digit+1)]
        new_filename_suffix = filename[(digit+1):].zfill(4) + ".png"
        debug(new_filename_prefix + new_filename_suffix)
        rename(frame_path, path.join(IMAGE_DIR, dirname, new_filename_prefix + new_filename_suffix))


if __name__ == "__main__":
    padder(IMAGE_DIR)