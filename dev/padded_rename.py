from os import rename, walk, path


base_path = "dev\images"

def find_digit_bound(filename: str) -> tuple[bool, int] | tuple[bool, None]:
    #filename = filename[:-4]
    for i in range(1, len(filename)):
        i = 0-i
        if filename[i].isdigit():
            continue
        else:
            return (True, i)
    
    return (False, None)

def folder_traverse(base_path: str):
    if path.isdir(base_path):
            for root, folders, __ in walk(base_path):
                for folder in folders:
                    base_path = path.join(root, folder)
                    #print(base_path)
                    if path.isdir(base_path):
                        file_traverse(base_path)
                        

def file_traverse(base_path: str):
      if path.isdir(base_path):
        for root, _, images in walk(base_path):
            for image in images:
                frame_path = path.join(root, image)
                if path.isfile(frame_path):
                    print(path.basename(frame_path)[:-4])
                    filename = path.basename(frame_path)[:-4]
                    dirname = path.basename(path.dirname(frame_path))
                    padded_rename(filename, dirname, frame_path)

# folder_traverse(base_path)

def padded_rename(filename: str, dirname: str, frame_path: str) -> None:

    
    found, digit = find_digit_bound(filename)
    #print(digit)
    if found:
        new_filename_prefix = filename[:(digit+1)]
        new_filename_suffix = filename[(digit+1):].zfill(4) + ".png"

        print(new_filename_prefix + new_filename_suffix)
        rename(frame_path, path.join(base_path, dirname, new_filename_prefix + new_filename_suffix))

folder_traverse(base_path)

