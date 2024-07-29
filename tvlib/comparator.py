from numpy import where
from tvlib.transformations import *
from tvlib._config import *
from tvlib._fileio import write_json




def save_frames_csv(frames:List[List[Tuple[int, int, int, int]]], label:str) -> None:
    """
    Save the converted frames to a csv file.
    """
    if len(frames) == 0: return None
    mkdir(path.join(CSV_DIR, label))
    
    savepaths:List[str] = [path.join(CSV_DIR, label, f'{str(count).zfill(4)}.csv') for count in range(len(frames))]
    for index, savepath in enumerate(savepaths):
        write_csv(savepath, HEADER, frames[index])
        
def save_frames_json(frames:List[List[Tuple[int, int, int, int]]], label:str) -> None:
    if len(frames) == 0: return None
    mkdir(path.join(JSON_DIR, label))
    
    savepath:str = path.join(JSON_DIR, label, f'{label}.json')
    write_json(savepath, {'frames': frames})
    

def _realign(img: MatLike, 
             tw: int, 
             th: int, 
             rotator: Rotation = Rotation.NONE, 
             flipper: Flip = Flip.NONE
            ) -> NDArray:
    """
    Reorder image rows to fit strip design, then flatten image into 2D array.
    """
    height, width, _ = img.shape
    target_dimensions = (tw, th)
    if target_dimensions!=(width, height):
        img = resize(img, target_dimensions)
        width, height = target_dimensions
    
    img = rotator(img)
    img = flipper(img)
    
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

def convert_images(img_paths: List[str],
                   target_dimensions:Tuple[int,int],
                   rotator: Rotation = Rotation.NONE,
                   flipper: Flip = Flip.NONE
                  ) -> None:
    """
    Given a list of image paths, convert these into  
    """
    if len(img_paths) == 0: return None
    label = path.basename(path.dirname(img_paths[0]))
    width, height = target_dimensions
    
    IMAGES = array([imread(img_path) for img_path in img_paths], dtype=uint8)

    frames:List[List[Tuple[int, int, int, int]]] = comparator(IMAGES,
                                                              label, 
                                                              width, 
                                                              height, 
                                                              rotator=rotator, 
                                                              flipper = flipper)

    write_json(img_path)
    #save_frames(frames, label)

def comparator(IMAGES: NDArray, 
               width: int, 
               height: int,  
               rotator: Rotation = Rotation.NONE, 
               flipper: Flip = Flip.NONE
               ) -> List[List[Tuple[int, int, int, int]]]:
    """
    Given a list of images, convert these into frames and return it.
    """

    frames:List[List[Tuple[int, int, int, int]]] = [ [(0,0,0,0)] for _ in range(len(IMAGES))]

    FRAMES = array([_realign(im, width, height, rotator=rotator, flipper = flipper) for im in IMAGES])
    old_frame = FRAMES[0]
    frames[0] = _nonzero(old_frame)
    
    
    for index, new_frame in enumerate(FRAMES[1:]):
        changes:List[Tuple[int, int, int, int]] = []
        
        if not array_equal(new_frame, old_frame):
            for i in range(len(new_frame)):
                if not array_equal(new_frame[i], old_frame[i]):
                    b,g,r = new_frame[i]
                    changes.append((i, b,g,r))
        
        # Store changes for further processing
        if len(changes) > 0: frames[index+1] = changes

        # Update old_frame for the next iteration
        old_frame = new_frame
    
    return frames

def convert_dir(folder: str, 
                target_dimensions:Tuple[int,int], 
                rotator: Rotation = Rotation.NONE, 
                flipper: Flip = Flip.NONE) -> None:
    
    animas = [path.join(IMAGE_DIR, folder, _) for _ in listdir(path.join(IMAGE_DIR, folder)) if isimage(_)]
    convert_images(animas, 
                   target_dimensions, 
                   rotator=rotator, 
                   flipper=flipper)

def convert_all(target_dimensions:Tuple[int,int],
                rotator: Rotation = Rotation.NONE, 
                flipper: Flip = Flip.NONE
                ) -> None:
    
    for folder in listdir(IMAGE_DIR):
        if path.isdir(path.join(IMAGE_DIR, folder)):
            print(folder)
            convert_dir(folder, 
                        target_dimensions,
                        rotator=rotator, 
                        flipper=flipper)