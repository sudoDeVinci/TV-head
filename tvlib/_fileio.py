import toml
import csv
from json import dump, JSONEncoder
from os import path, makedirs, mkdir, walk, rename
from typing import Any, Dict, LiteralString, List
from numpy import integer, floating, ndarray
from enum import Enum
import logging

# Logging
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('.log'),
        ],
    )


def out01(x: str) -> None:
    """
    Print the given string.
    """
    print(x)


def out02(x: str) -> None:
    """
    Don't print the given string.
    This is a dummy function.
    """
    pass


# Directories
class FOLDERS(Enum):
    IMAGE_DIR: str = mkdir("animations")
    CSV_DIR: str = mkdir("csvs")
    JSON_DIR: str = mkdir("json")
    CONFIG_FILE: LiteralString = "conf.toml"


class NpEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, integer):
            return int(obj)
        if isinstance(obj, floating):
            return float(obj)
        if isinstance(obj, ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def mkdir(folder: str) -> str:
    """
    Ensure path exists before returning same path.
    """
    if not path.exists(folder):
        makedirs(folder)
    return folder


def write_toml(data: Dict, path: str) -> None:
    """
    Write to a toml file.
    """
    try:
        out = toml.dumps(data)
        with open(path, "w") as f:
            f.write(out)
    except Exception:
        return None


def load_toml(file_path: str) -> dict[str, Any] | None:
    """"
    Attempt to load data from toml file.
    """
    toml_data = None
    try:
        with open(file_path, 'r') as file:
            toml_data = toml.load(file)
            if not toml_data:
                return None
    except FileNotFoundError:
        return None
    except toml.TomlDecodeError:
        return None

    return toml_data


def write_csv(savepath: str,
              headers: List[str],
              data: List[List[str]]) -> None:
    """
    Attempt to write to csv file.
    """

    with open(savepath, 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)


def _write_json(savepath: str, data: dict) -> None:
    """
    Attempt to write to json file.
    """
    with open(savepath, 'w', encoding="utf-8") as jsonfile:
        dump(data, jsonfile, cls=NpEncoder)


def write_json(savepath: str, data: dict) -> None:
    try:
        _write_json(savepath, data)
    except Exception as e:
        print(f"Error writing to json file:-> {e}")
        return None


def isimage(file_path: str) -> bool:
    """
    Check if file is an image.
    """
    return path.splitext(file_path)[1].lower() in ['.jpg', '.jpeg', '.png',
                                                   '.bmp', '.gif', '.tif',
                                                   '.tiff', '.webp', '.ico',
                                                   '.heif', '.heic', '.raw']


def _find_digit_bound(filename: str) -> tuple[bool, int] | tuple[bool, None]:
    """
    Find the ending digit of a filename.
    If found, return true and the number.
    """
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
    else:
        print("Not a dir")


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
                    print(path.basename(frame_path)[:-4])
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
        new_filename_suffix = filename[(digit+1):].zfill(6) + ".png"
        newfn = f"{new_filename_prefix}{new_filename_suffix}"
        print(newfn)
        rename(frame_path, path.join(FOLDERS.IMAGE_DIR.value,
                                     dirname,
                                     newfn))
