import csv
from glob import glob
from os import path, walk, mkdir
from numpy import array_equal, ndarray, flip
from cv2 import imread, IMREAD_COLOR,resize, Mat, compare, CMP_NE, findNonZero


# Resolve paths details and save file to csv
def resolve_path_and_save(image_path:str, write_folder:str, image:ndarray):
    global header
    filename = path.basename(image_path)[:-4]+".csv"
    # print(filename)
    foldername = path.basename(path.dirname(image_path))  
    # print(foldername)

    if foldername == path.basename(path.dirname(write_folder)):
        savepath = f"{write_folder}/{filename}"
    else:
        savepath = f"{write_folder}/{foldername}/{filename}"

    # If base writing folder doesnt exist, create it
    if not path.exists(f"{write_folder}"):
        mkdir(f"{write_folder}")
    # If subfolder does not exist, create it.
    if not path.exists(f"{write_folder}/{foldername}"):
        mkdir(f"{write_folder}/{foldername}")

    #============================================================================#

    with open(savepath, "w+", encoding = "utf-8", newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(image)


# Get the resolution of the display from the upload folder.
# tuple is in form (width, height)
def get_res() -> tuple[int, int]:
    res = []
    with open('upload/res.txt', 'r', encoding = 'utf-8') as r:
        res = [int(line.rstrip('\n')) for line in r]
    return tuple(res)


# Reorder image rows to fit strip design, then flatten image into 2D array. 
def realign(img:Mat, tw, th):
    height, width, _ = img.shape
    target_dimensions = (tw, th)
    if target_dimensions!=(width, height):
            # print(f"Image is {width} x {height}, we want {target_dimensions[0]} x {target_dimensions[1]}")
            img = resize(img, target_dimensions)
            # print(img.shape)
            height, width, _ = img.shape
    # Reverse the order of pixels in every second row
    for i in range(1, height, 2):
        img[i, :] = flip(img[i, :], axis=0)  # Flip the row
    return img.reshape(-1, img.shape[-1])
    

# Convert and save a single image
def convert_single_image(image:str, write_folder: str, target_dimensions:tuple[int,int]) -> Mat:

    width, height = target_dimensions
    img = imread(image, IMREAD_COLOR)
    img = realign(img, width, height)
    frame = []
    for i in range(len(img)):
        b,g,r = img[i]
        if b !=0 or g!= 0 or r!= 0:
            frame.append((i, b, g, r))

        
    resolve_path_and_save(image, write_folder, frame)
    return img


# Convert and save all images in a folder sequentially.
def convert_images(images:list(), write_folder: str, target_dimensions:tuple[int,int]) -> None:
        
    width, height = target_dimensions

    old_frame_path = images[0]
    old_frame = convert_single_image(old_frame_path, write_folder, target_dimensions)

    for index in range(1, len(images)):
        changes = []
        new_frame_path = images[index]
        new_frame_og = imread(new_frame_path, IMREAD_COLOR)
        new_frame = realign(new_frame_og, width, height)


        if not array_equal(new_frame, old_frame):
            for i in range(len(new_frame)):
                if not array_equal(new_frame[i], old_frame[i]):
                    b,g,r = new_frame[i]
                    changes.append((i, b,g,r))

            
            # print(f"Image {index} Changes:\n{changes}\n")
            if len(changes) > 0:
                resolve_path_and_save(new_frame_path, write_folder, changes)

        else:
            # Need to add arbitrary frame with only one pixel so that frame pacing can be kept.
            b,g,r = new_frame[0]
            changes.append((0, b,g,r))
            resolve_path_and_save(new_frame_path, write_folder, changes)
            

        # Make old frame the new frame.
        old_frame = new_frame


# Convert all images in a folder sequentially.
def convert_folder(folder_path:str, write_folder:str, target_dimensions:tuple[int,int]) -> None:
    regex = folder_path + "/*.png"
    images = glob(regex, recursive = False)
    if len(images) == 0:
        print(f"Image directory {folder_path} is empty")
        return
    elif len(images) == 1:
       convert_single_image(images[0], write_folder, target_dimensions)
    else:
        convert_images(images, write_folder, target_dimensions)
    

# Convert all folders of images within a given directory.
def convert_all(folder_path:str, write_folder:str, target_dimensions:tuple[int,int]) -> None:
    if path.isdir(folder_path):
        for root, folders, __ in walk(folder_path):
            for folder in folders:
                folder_path = path.join(root, folder)
                if path.isdir(folder_path):
                    print(folder_path)
                    convert_folder(folder_path, write_folder, target_dimensions)


def main() -> None:
    global header
    (tw, th) = get_res()
    # Header for frame csvs
    header = ['index', 'blue', 'green', 'red']
    # folder we write our folders of frames  to

    convert_all("dev/images", 'upload/render_pico/csvs/', (tw,th))

if __name__ == "__main__":
    main()