from __future__ import annotations
from typing import List, Tuple, Optional, TYPE_CHECKING
from os import path, listdir
import logging

# Handle optional imports
try:
    from numpy import array, nonzero, array_equal, flip, uint8, resize
except ImportError:
    logging.warning("NumPy not available. Some functionality may be limited.")
    array = list
    nonzero = lambda x: []
    array_equal = lambda x, y: x == y
    flip = lambda x, axis=None: x
    uint8 = int
    resize = lambda x, shape: x

try:
    from cv2 import imread
except ImportError:
    logging.warning("OpenCV not available. Image loading will be limited.")
    def imread(path: str):
        """Fallback imread function."""
        logging.error(f"Cannot load image {path} - OpenCV not available")
        return None

if TYPE_CHECKING:
    from tvlib._config import MatLike

from tvlib.transformations import Flip, Rotation
from tvlib._config import Config
from tvlib._fileio import write_json, FOLDERS, mkdir, isimage


def save_frames_json(frames: List[List[Tuple[int, int, int, int]]],
                     label: str,
                     target_dimensions: Tuple[int, int]) -> bool:
    """
    Save the converted frames to an optimized JSON file for microcontrollers.
    
    Args:
        frames: List of frame data
        label: Label for the output file
        target_dimensions: (width, height) of the display
        
    Returns:
        True if successful, False otherwise
    """
    if len(frames) == 0:
        logging.warning("No frames to save")
        return False

    try:
        width, height = target_dimensions
        
        # Create minimal JSON structure matching the specified format
        animation_data = {
            "metadata": {
                "name": label,
                "width": width,
                "height": height,
                "total_pixels": width * height,
                "frame_count": len(frames),
                "format": "bgr",
                "type": "diff"  # Global type for the animation
            },
            "frames": frames  # Simple array of frame data
        }

        # Save to JSON file
        output_dir = path.join(FOLDERS.JSON_DIR.value, label)
        mkdir(output_dir)
        savepath = path.join(output_dir, f'{label}.json')
        
        write_json(savepath, animation_data)
        
        # Calculate compression statistics
        total_pixels_uncompressed = len(frames) * width * height * 3  # 3 bytes per pixel
        total_pixels_compressed = sum(len(frame_data) for frame_data in frames) * 3
        compression_ratio = (1 - total_pixels_compressed / total_pixels_uncompressed) * 100
        
        logging.info(f"Saved animation '{label}' to JSON format: {savepath}")
        logging.info(f"Compression: {compression_ratio:.1f}% size reduction")
        logging.info(f"Frame count: {len(frames)}, Resolution: {width}x{height}")
        
        return True
        
    except Exception as e:
        logging.error(f"Error saving frames to JSON: {e}")
        return False


def _realign(img: 'MatLike',
             tw: int,
             th: int,
             rotator: Rotation = Rotation.NONE,
             flipper: Flip = Flip.NONE) -> 'MatLike':
    """
    Reorder image rows to fit strip design, then flatten image into 2D array.
    
    Args:
        img: Input image array
        tw: Target width
        th: Target height  
        rotator: Rotation transformation to apply
        flipper: Flip transformation to apply
        
    Returns:
        Flattened and transformed image array
    """
    if img is None:
        raise ValueError("Input image is None")
        
    logging.debug(f"Processing image with shape: {img.shape}")
    
    # Handle both grayscale (2D) and color (3D) images
    if len(img.shape) == 2:
        height, width = img.shape
        channels = 1
        # Convert grayscale to 3-channel for consistency
        img = array([img, img, img]).transpose(1, 2, 0)
        logging.debug(f"Converted grayscale to 3-channel, new shape: {img.shape}")
    elif len(img.shape) == 3:
        height, width, channels = img.shape
    else:
        raise ValueError(f"Unsupported image shape: {img.shape}")
    
    target_dimensions = (tw, th)
    if target_dimensions != (width, height):
        logging.debug(f"Resizing from ({width}, {height}) to {target_dimensions}")
        img = resize(img, target_dimensions)
        width, height = target_dimensions

    # Apply transformations
    try:
        img = rotator(img)
        img = flipper(img)
    except Exception as e:
        logging.error(f"Error applying transformations: {e}")
        raise

    # Ensure we still have the right shape after transformations
    if len(img.shape) != 3:
        raise ValueError(f"Image has wrong shape after transformations: {img.shape}")

    # Reverse the order of pixels in every second row
    img[1::2, :] = flip(img[1::2, :], axis=1)
    
    # Flatten the image
    flattened = img.reshape(-1, img.shape[-1])
    logging.debug(f"Flattened image shape: {flattened.shape}")
    
    return flattened


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
                   ) -> Optional[List[List[Tuple[int, int, int, int]]]]:
    """
    Convert a list of image paths into processed frame data.
    
    Args:
        img_paths: List of paths to image files
        target_dimensions: Target (width, height) for output
        rot: Rotation transformation to apply
        flip: Flip transformation to apply
        
    Returns:
        List of frame data or None if failed
    """
    if len(img_paths) == 0:
        logging.warning("No image paths provided")
        return None

    width, height = target_dimensions
    
    try:
        # Load images with error checking
        images = []
        for img_path in img_paths:
            img = imread(img_path)
            if img is None:
                logging.warning(f"Failed to load image: {img_path}")
                continue
            images.append(img)
        
        if not images:
            logging.error("No images could be loaded")
            return None
            
        IMAGES = array(images, dtype=uint8)
        logging.debug(f"Loaded {len(images)} images, applying rotation: {rot}")

        frames: List[List[Tuple[int, int, int, int]]] = comparator(IMAGES,
                                                                   width,
                                                                   height,
                                                                   rot,
                                                                   flip)

        return frames
        
    except Exception as e:
        logging.error(f"Error in convert_images: {e}")
        return None


def comparator(IMAGES: 'MatLike',
               width: int,
               height: int,
               rot: Rotation = Rotation.NONE,
               flip: Flip = Flip.NONE
               ) -> Optional[List[List[Tuple[int, int, int, int]]]]:
    """
    Given a list of images, convert these into frames and return it.
    
    Args:
        IMAGES: Array of images to process
        width: Target width
        height: Target height
        rot: Rotation transformation
        flip: Flip transformation
        
    Returns:
        List of frame data or None if failed
    """
    try:
        if IMAGES is None or len(IMAGES) == 0:
            logging.error("No images provided to comparator")
            return None
            
        frames: List[List[Tuple[int, int, int, int]]] = [
                                        [(0, 0, 0, 0)] for _ in range(len(IMAGES))
                                    ]

        logging.debug(f"Processing {len(IMAGES)} images")
        
        FRAMES = array([_realign(im, width, height, rot, flip) for im in IMAGES])
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
        
    except Exception as e:
        logging.error(f"Error in comparator: {e}")
        return None


def convert_dir(folder: str,
                target_dimensions: Tuple[int, int],
                rot: Rotation = Rotation.NONE,
                flip: Flip = Flip.NONE
                ) -> Optional[List[List[Tuple[int, int, int, int]]]]:
    """
    Convert all images in a directory to frame data.
    
    Args:
        folder: Name of the folder in the animations directory
        target_dimensions: Target (width, height) for output
        rot: Rotation transformation to apply
        flip: Flip transformation to apply
        
    Returns:
        List of frame data or None if failed
    """
    try:
        folder_path = path.join(FOLDERS.IMAGE_DIR.value, folder)
        
        if not path.exists(folder_path):
            logging.error(f"Folder not found: {folder_path}")
            return None
        
        if not path.isdir(folder_path):
            logging.error(f"Path is not a directory: {folder_path}")
            return None
            
        # Get all image files in the directory
        all_files = listdir(folder_path)
        image_files = [f for f in all_files if isimage(f)]
        
        if not image_files:
            logging.warning(f"No image files found in {folder_path}")
            return None
            
        # Create full paths
        animas = [path.join(folder_path, f) for f in image_files]
        
        logging.info(f"Processing {len(animas)} images from {folder}")
        
        frames = convert_images(animas, target_dimensions, rot, flip)
        
        if frames is not None:
            save_frames_json(frames, folder, target_dimensions)
            logging.info(f"Successfully processed folder: {folder}")
        else:
            logging.error(f"Failed to convert images in folder: {folder}")

        return frames
        
    except Exception as e:
        logging.error(f"Error processing folder {folder}: {e}")
        return None


def convert_all(target_dimensions: Tuple[int, int],
                rotator: Rotation = Rotation.NONE,
                flipper: Flip = Flip.NONE
                ) -> bool:
    """
    Convert all animation folders.
    
    Args:
        target_dimensions: Target (width, height) for output
        rotator: Rotation transformation to apply
        flipper: Flip transformation to apply
        
    Returns:
        True if successful, False otherwise
    """
    try:
        animations_dir = FOLDERS.IMAGE_DIR.value
        
        if not path.exists(animations_dir):
            logging.error(f"Animations directory not found: {animations_dir}")
            return False
            
        folders = [f for f in listdir(animations_dir) 
                  if path.isdir(path.join(animations_dir, f))]
        
        if not folders:
            logging.warning(f"No folders found in {animations_dir}")
            return False
            
        logging.info(f"Processing {len(folders)} animation folders")
        
        success_count = 0
        for folder in folders:
            logging.info(f"Processing folder: {folder}")
            result = convert_dir(folder, target_dimensions, rotator, flipper)
            if result is not None:
                success_count += 1
            
        logging.info(f"Successfully processed {success_count}/{len(folders)} folders")
        return success_count > 0
        
    except Exception as e:
        logging.error(f"Error in convert_all: {e}")
        return False
