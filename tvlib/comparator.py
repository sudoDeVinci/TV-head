from tvlib.transformations import Flip, Rotation
from tvlib._config import MatLike, write_csv, isimage, HEADER
from tvlib._fileio import write_json, FOLDERS
from os import path, listdir, mkdir
from numpy import array, nonzero, array_equal, flip, uint8, resize
from typing import List, Tuple
from cv2 import imread


def save_frames_csv(frames: List[List[Tuple[int, int, int, int]]],
                    label: str) -> None:
    """
    Save the converted frames to a csv file.
    """
    if len(frames) == 0:
        return None

    csvs = FOLDERS.CSV_DIR.value
    mkdir(path.join(csvs, label))

    savepaths: List[str] = [path.join(csvs, label,
                                      f'{str(count).zfill(4)}.csv'
                                      ) for count in range(len(frames))]

    for index, savepath in enumerate(savepaths):
        write_csv(savepath, HEADER, frames[index])


def save_frames_json(frames: List[List[Tuple[int, int, int, int]]],
                     label: str) -> None:
    if len(frames) == 0:
        return None

    mkdir(path.join(FOLDERS.JSON_DIR.value, label))

    savepath: str = path.join(FOLDERS.JSON_DIR.value,
                              label,
                              f'{label}.json')
    write_json(savepath, {'frames': frames})


def _realign(img: MatLike,
             tw: int,
             th: int,
             rotator: Rotation = Rotation.NONE,
             flipper: Flip = Flip.NONE) -> MatLike:
    """
    Reorder image rows to fit strip design, then flatten image into 2D array.
    """
    height, width, _ = img.shape
    target_dimensions = (tw, th)
    if target_dimensions != (width, height):
        img = resize(img, target_dimensions)
        width, height = target_dimensions

    img = rotator(img)
    img = flipper(img)

    # Reverse the order of pixels in every second row
    img[1::2, :] = flip(img[1::2, :], axis=1)
    return img.reshape(-1, img.shape[-1])


def _nonzero(img: MatLike) -> List[Tuple[int, int, int, int]]:
    """
    Extract non-zero values from image.
    """
    nonzero_pixels = nonzero(img.any(axis=1))
    frame = [(i, *img[i]) for i in nonzero_pixels[0]]
    return frame


def convert_images(img_paths: List[str],
                   target_dimensions: Tuple[int, int],
                   rot: Rotation = Rotation.NONE,
                   flip: Flip = Flip.NONE
                   ) -> List[List[Tuple[int, int, int, int]]]:
    """
    Given a list of image paths, convert these into
    """
    if len(img_paths) == 0:
        return None

    width, height = target_dimensions

    IMAGES = array([imread(img_path) for img_path in img_paths], dtype=uint8)

    print(rot)

    frames: List[List[Tuple[int, int, int, int]]] = comparator(IMAGES,
                                                               width,
                                                               height,
                                                               rot,
                                                               flip)

    return frames


def comparator(IMAGES: MatLike,
               width: int,
               height: int,
               rot: Rotation = Rotation.NONE,
               flip: Flip = Flip.NONE
               ) -> List[List[Tuple[int, int, int, int]]] | None:
    """
    Given a list of images, convert these into frames and return it.
    """

    frames: List[List[Tuple[int, int, int, int]]] = [
                                    [(0, 0, 0, 0)] for _ in range(len(IMAGES))
                                ]

    FRAMES = array([_realign(im,
                             width,
                             height,
                             rot,
                             flip) for im in IMAGES])
    old_frame = FRAMES[0]
    frames[0] = _nonzero(old_frame)

    for index, new_frame in enumerate(FRAMES[1:]):
        changes: List[Tuple[int, int, int, int]] = []

        if not array_equal(new_frame, old_frame):
            for i in range(len(new_frame)):
                if not array_equal(new_frame[i], old_frame[i]):
                    b, g, r = new_frame[i]
                    changes.append((i, b, g, r))

        # Store changes for further processing
        if len(changes) > 0:
            frames[index+1] = changes

        # Update old_frame for the next iteration
        old_frame = new_frame

    return frames


def convert_dir(folder: str,
                target_dimensions: Tuple[int, int],
                rot: Rotation = Rotation.NONE,
                flip: Flip = Flip.NONE
                ) -> List[List[Tuple[int, int, int, int]]]:

    animas = [path.join(FOLDERS.IMAGE_DIR.value,
                        folder, _) for _ in listdir(path.join(
                            FOLDERS.IMAGE_DIR.value,
                            folder)) if isimage(_)]
    frames = convert_images(animas,
                            target_dimensions,
                            rot,
                            flip)

    save_frames_csv(frames, folder)

    return frames


def convert_all(target_dimensions: Tuple[int, int],
                rotator: Rotation = Rotation.NONE,
                flipper: Flip = Flip.NONE
                ) -> None:

    for folder in listdir(FOLDERS.IMAGE_DIR.value):
        if path.isdir(path.join(FOLDERS.IMAGE_DIR.value,
                                folder)):
            print(folder)
            convert_dir(folder,
                        target_dimensions,
                        rotator,
                        flipper)
