#!/usr/bin/env python3
"""
Debug script to test image loading and processing.
"""

import sys
import logging
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

# Set up debug logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')

def test_image_processing():
    """Test the image processing pipeline with a single image."""
    from tvlib.comparator import convert_dir
    from tvlib.transformations import Rotation, Flip
    from tvlib._config import Config
    import os
    
    # Load config
    Config.load()
    resolution = Config.resolution()
    print(f"Using resolution: {resolution}")
    
    # Check if animations directory exists
    animations_dir = "animations"
    if not os.path.exists(animations_dir):
        print(f"❌ Animations directory not found: {animations_dir}")
        return False
    
    # List available folders
    folders = [f for f in os.listdir(animations_dir) 
              if os.path.isdir(os.path.join(animations_dir, f))]
    
    if not folders:
        print("❌ No animation folders found")
        return False
    
    print(f"Found folders: {folders}")
    
    # Test with the first folder
    test_folder = folders[0]
    print(f"Testing with folder: {test_folder}")
    
    try:
        result = convert_dir(
            test_folder, 
            resolution, 
            Rotation.NONE, 
            Flip.NONE
        )
        
        if result is not None:
            print(f"✅ Successfully processed {test_folder}")
            print(f"Generated {len(result)} frames")
            return True
        else:
            print(f"❌ Failed to process {test_folder}")
            return False
            
    except Exception as e:
        print(f"❌ Exception during processing: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_single_image():
    """Test loading a single image file."""
    from cv2 import imread
    import os
    
    # Find a single image file
    animations_dir = "animations"
    for root, dirs, files in os.walk(animations_dir):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                print(f"Testing image: {image_path}")
                
                img = imread(image_path)
                if img is not None:
                    print(f"✅ Image loaded successfully, shape: {img.shape}")
                    return True
                else:
                    print(f"❌ Failed to load image: {image_path}")
                    return False
    
    print("❌ No image files found")
    return False

if __name__ == "__main__":
    print("=" * 50)
    print("TV HEAD IMAGE PROCESSING DEBUG")
    print("=" * 50)
    
    print("\n1. Testing single image loading...")
    if not test_single_image():
        print("Single image test failed")
        sys.exit(1)
    
    print("\n2. Testing full image processing pipeline...")
    if test_image_processing():
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Image processing test failed")
        sys.exit(1)
