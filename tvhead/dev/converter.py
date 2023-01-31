"""
We convert a number of png files into a 3d array of LED indexes and rgb values, then write these to csv files.
"""

import os
import cv2
import numpy as np
import csv 


# Create a new numpy array in the form [LED index, r, g ,b] 
def convert_image(path:str, write_folder: str) -> None:
    global header
    # read in the png file
    img = cv2.imread(path, cv2.IMREAD_COLOR)
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

    # flatten image to 2d array
    img_vector = img.reshape(-1, img.shape[-1])

    pixels = []

    for i in range(img_vector.shape[0]):
        if np.any(img_vector[i]):
            pixels.append([i, img_vector[i][2], img_vector[i][1], img_vector[i][0]])
    #if len(pixels) == 0: pixels.append([0,0,0,0])

    with open(savepath, "w+", encoding = "utf-8", newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(pixels)


# Convert all images in a folder sequentially.
def convert_frames(folder_path:str, write_folder:str) -> None:

    if os.path.isdir(folder_path):
        for root, _, images in os.walk(folder_path):
            for image in images:
                frame_path = os.path.join(root, image)
                if os.path.isfile(frame_path):
                    convert_image(frame_path, write_folder)


# Convert all folders of images within a given directory.
def convert_all(folder_path:str, write_folder:str) -> None:
    if os.path.isdir(folder_path):
        for root, folders, __ in os.walk(folder_path):
            for folder in folders:
                folder_path = os.path.join(root, folder)
                print(folder_path)
                if os.path.isdir(folder_path):
                    convert_frames(folder_path, write_folder)


def main() -> None:
    # Header for frame csvs
    header = ['index', 'red', 'green', 'blue']
    # folder we write our folders of frames  to
    write_folder = 'upload/csvs'

    convert_all("dev/images", write_folder)
    # convert_frames("dev/images/blink", write_folder)


if __name__ == "__main__":
    main()