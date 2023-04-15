"""
We convert a number of png files into a 3d array of LED indexes and rgb values, then write these to csv files
in the form: 
index, blue, green, red
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
        img = cv2.resize(img, target_dimensions)
        height, width, _ = img.shape

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
    
    tweaked_img = []
    for i in range(1, height, 2):
        img[i, :] = np.flip(img[i, :], axis=0)  # Flip the row
    img = img.reshape(-1, img.shape[-1])

    for i in range(len(img)):
        #print(img[i])
        b,g,r = img[i]
        if b!=0 and g !=0 and r !=0:
            tweaked_img.append((i, b,g,r))

    #====================================================================================#

    with open(savepath, "w+", encoding = "utf-8", newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(tweaked_img)


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
                if os.path.isdir(folder_path):
                    print(folder_path)
                    convert_frames(folder_path, write_folder, target_dimensions)


def main() -> None:
    global header
    (tw, th) = get_res()
    # Header for frame csvs
    header = ['index', 'blue', 'green', 'red']
    # folder we write our folders of frames  to

    convert_all("dev/images/", "upload/csvs/", (tw,th))


if __name__ == "__main__":
    main()