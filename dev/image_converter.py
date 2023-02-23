"""
We convert a number of png files into a 3d array of LED indexes and rgb values, then write these to csv files
in the form: 
index, red, green, blue.
"""

import os
import cv2
import numpy as np
import csv 


# Get the resolution of the display from the upload folder.
# tuple is in form (width, height)
def get_res() -> tuple[int, int]:
    res = []
    with open('upload/res.txt', 'r', encoding = 'utf-8') as r:
        res = [int(line.rstrip('\n')) for line in r]
    return tuple(res)

 
# Create a new numpy array in the form [LED index, r, g ,b] 
def convert_image(path:str, write_folder: str, target_dimensions:tuple[int,int]) -> None:
    global header

    #====================================================================================#

    # read in the png file
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    # Read the dimensions of the image.
    height, width, _ = img.shape
    # If the dimensions dont match the display dimensions, resize it.
    if target_dimensions!=(width, height):
        # print(f"Image is {width} x {height}, we want {target_dimensions[0]} x {target_dimensions[1]}")
        img = cv2.resize(img, target_dimensions, interpolation = cv2.INTER_AREA)

    #====================================================================================#

    filename = os.path.basename(path)[:-4]+".csv"
    # print(filename)
    foldername = os.path.basename(os.path.dirname(path))
    # print(foldername)

    if foldername == os.path.basename(os.path.dirname(write_folder)):
        savepath = f"{write_folder}/{filename}"
    else:
        savepath = f"{write_folder}/{foldername}/{filename}"

    # If base writing folder doesnt exist, create it
    if not os.path.exists(f"{write_folder}"):
        os.mkdir(f"{write_folder}")
    # If subfolder does not exist, create it.
    if not os.path.exists(f"{write_folder}/{foldername}"):
            os.mkdir(f"{write_folder}/{foldername}")

    #====================================================================================#
    # flatten image to 2d array
    img_vector = img.reshape(-1, img.shape[-1])
    # print(width)

    # Flip every odd row in the array.
    # "Row" as in row of pixels on the tv head.
    # Assuming the wiring is as simple as possible.

    # Image is sized to our dimensions so we use them
    for i in range(width, (height*width), width*2):
        # Start iterating at the first odd row
        # Skip to every other odd row afterward.
        # Flip the odd row and insert it in-place
        img_vector[i:(i+width)] = np.flip(img_vector[i:(i+width)], axis=1)

    """
    A frame which looks like this:

    [00 01 02 03 04 05 06 07 08 09]
    [10 11 12 13 14 15 16 17 18 19]
    [20 21 22 23 24 25 26 27 28 29]
    [30 31 32 33 34 35 36 37 38 39]
    [40 41 42 43 44 45 46 47 48 49]
    [50 51 52 53 54 55 56 57 58 59]
    [60 61 62 63 64 65 66 67 68 69]
    [70 71 72 73 74 75 76 77 78 79]
    [80 81 82 83 84 85 86 87 88 89]
    [90 91 92 93 94 95 96 97 98 99]

    Will now look like this:
    
    [00 01 02 03 04 05 06 07 08 09]
    [19 18 17 16 15 14 13 12 11 10]
    [20 21 22 23 24 25 26 27 28 29]
    [39 38 37 36 35 34 33 32 31 30]
    [40 41 42 43 44 45 46 47 48 49]
    [59 58 57 56 55 54 53 52 51 50]
    [60 61 62 63 64 65 66 67 68 69]
    [79 78 77 76 75 74 73 72 71 70]
    [80 81 82 83 84 85 86 87 88 89]
    [99 98 97 96 95 94 93 92 91 90]
    """


    pixels = []


    reverse = False
    for i in range(img_vector.shape[0]):
        if i%(width) == 0:
            reverse = not reverse
        if np.any(img_vector[i]):
            if reverse:
                pixels.append([i, img_vector[i][2], img_vector[i][1], img_vector[i][0]])
                #print(f"Index: {i} \t| |\t ({img_vector[i][2]},{img_vector[i][1]},{img_vector[i][0]})")
            else:
                pixels.append([i, img_vector[i][0], img_vector[i][1], img_vector[i][2]])
                #print(f"Index: {i} \t| |\t ({img_vector[i][0]},{img_vector[i][1]},{img_vector[i][2]})")

    #====================================================================================#

    with open(savepath, "w+", encoding = "utf-8", newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(pixels)


# Convert all images in a folder sequentially.
def convert_frames(folder_path:str, write_folder:str, target_dimensions:tuple[int,int]) -> None:
    if os.path.isdir(folder_path):
        for root, _, images in os.walk(folder_path):
            for image in images:
                frame_path = os.path.join(root, image)
                if os.path.isfile(frame_path):
                    convert_image(frame_path, write_folder, target_dimensions)


# Convert all folders of images within a given directory.
def convert_all(folder_path:str, write_folder:str, target_dimensions:tuple[int,int]) -> None:
    if os.path.isdir(folder_path):
        for root, folders, __ in os.walk(folder_path):
            for folder in folders:
                folder_path = os.path.join(root, folder)
                print(folder_path)
                if os.path.isdir(folder_path):
                    convert_frames(folder_path, write_folder, target_dimensions)


def main() -> None:
    global header
    (tw, th) = get_res()
    # Header for frame csvs
    header = ['index', 'red', 'green', 'blue']
    # folder we write our folders of frames  to
    write_folder = 'upload/csvs'

    convert_all("dev/images", write_folder, (tw,th))


if __name__ == "__main__":
    main()