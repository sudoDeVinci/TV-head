import toml
import csv
from json import dump
from os import path, walk, mkdir, makedirs, rename
from typing import List, Tuple, Sequence, Mapping, Dict, Any, Self


def mkdir(folder:str) -> str:
    """
    Ensure path exists before returning same path.
    """
    if not path.exists(folder): makedirs(folder)
    return folder

def write_toml(data:Dict, path:str) -> None:
    """
    Write to a toml file.
    """
    try:
        out = toml.dumps(data)
        with open(path, "w") as f:
            f.write(out)
    except Exception as e:
        return None

def load_toml(file_path:str) -> dict[str, Any] | None:
    """"
    Attempt to load data from toml file.
    """
    toml_data = None
    try:
        with open(file_path, 'r') as file:
            toml_data = toml.load(file)
            if not toml_data: return None
    except FileNotFoundError:
        return None
    except toml.TomlDecodeError as e:
        return None

    return toml_data

def write_csv(savepath: str, headers: List[str], data:List[List[str]]) -> None:
    """
    Attempt to write to csv file.
    """
    
    with open(savepath, 'w+', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        writer.writerows(data)

def write_json(savepath: str, data) -> None:
    """
    Attempt to write to json file.
    """
    with open(savepath, 'w+', encoding = "utf-8") as jsonfile:
        dump(data, jsonfile, indent = 4)
        
def isimage(file_path:str) -> bool:
    """
    Check if file is an image.
    """
    return path.splitext(file_path)[1].lower() in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tif', '.tiff', '.webp', '.ico', '.heif', '.heic', '.raw']