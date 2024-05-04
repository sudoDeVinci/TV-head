from numpy import where
from tvlib._config import *
from glob import glob

def save_frames(frames:List[List[Tuple[int, int, int, int]]], label:str) -> None:
    """
    Save the changes to a csv file.
    """
    if len(frames) == 0: return None
    mkdir(path.join(CSV_DIR, label))
    
    savepaths:List[str] = [path.join(CSV_DIR, label, f'{str(count).zfill(4)}.csv') for count in range(len(frames))]
    for index, savepath in enumerate(savepaths):
        write_csv(savepath, HEADER, frames[index])

def _realign(img: MatLike, tw: int, th: int) -> NDArray:
    """
    Reorder image rows to fit strip design, then flatten image into 2D array.
    """
    height, width, _ = img.shape
    target_dimensions = (tw, th)
    if target_dimensions!=(width, height):
        img = resize(img, target_dimensions)
        height, width, _ = img.shape
    # Reverse the order of pixels in every second row
    img[1::2, :] = flip(img[1::2, :], axis=1)
    return img.reshape(-1, img.shape[-1])


def _nonzero(img: Mat) -> Tuple[Tuple[int, int, int, int]]:
    """
    Extract non-zero values from image.
    """
    nonzero_pixels = nonzero(img.any(axis=1))
    frame = [(i, *img[i]) for i in nonzero_pixels[0]]
    return frame

def convert_images(img_paths: List[str], target_dimensions:Tuple[int,int]) -> None:
    if len(img_paths) == 0: return None
    label = path.basename(path.dirname(img_paths[0]))
    width, height = target_dimensions
    
    frames:List[List[Tuple[int, int, int, int]]] = [ [(0,0,0,0)] for _ in range(len(img_paths))]
    
    IMAGES = array([imread(img_path) for img_path in img_paths], dtype=uint8)

    old_img = IMAGES[0]
    old_frame = _realign(old_img, width, height)
    frames[0] = _nonzero(old_frame)

    for index, img in enumerate(IMAGES[1:]):
        changes:List[Tuple[int, int, int, int]] = []
        new_frame = _realign(img, width, height)
        
        if not array_equal(new_frame, old_frame):
            for i in range(len(new_frame)):
                if not array_equal(new_frame[i], old_frame[i]):
                    b,g,r = new_frame[i]
                    changes.append((i, b,g,r))
        
        # Store changes for further processing
        if len(changes) > 0: frames[index] = changes

        # Update old_frame for the next iteration
        old_frame = new_frame
    
    save_frames(frames, label)


def convert_dir(folder: str) -> None:
    animas = [path.join(IMAGE_DIR, folder, _) for _ in listdir(path.join(IMAGE_DIR, folder)) if isimage(_)]
    convert_images(animas, (10, 10))
    
def convert_all() -> None:
    for folder in listdir(IMAGE_DIR):
        if path.isdir(path.join(IMAGE_DIR, folder)):
            print(folder)
            convert_dir(folder)
