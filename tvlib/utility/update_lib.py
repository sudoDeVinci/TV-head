"""
Upldate the libraries of the board.
If the first attempt to upload doesn't work, try once more.
After this, consoder the file "borked".
"""

from  os import listdir, path
from time import sleep
from subprocess import Popen
from parsers import parseStringtoInt
from sys import argv


folder = 'upload/lib'
# If no lib folder, exit
if not path.isdir(folder):
    print("No /lib folder to upload")
    exit()

files = listdir(folder)

# If there is not a valid second argument for the COM port, default to COM 3.
# First check if there are at least 2 args passed to the script.
# Then check if the [1] arg can be cast to integer.
parsed = parseStringtoInt(argv[1]) if len(argv) >=2 else 3
COM = parsed if parsed else 3

# if lib folder exists but is empty, exit
if len(files) == 0:
    print("Nothing in lib folder to upload")
    exit()

# Try to upload library files
retries = {}
for file in files:
    try:
        print(f"> ampy --port COM{COM} put {folder}/{file} /lib/{file}")
        process = Popen(f"ampy --port COM{COM} put {folder}/{file} /lib/{file}")
        process.wait()
        sleep(2)
    except Exception as e:
        print(f"-- Couldn't upload {file}, will retry.")
        retries[file] = 0


# Attempt to upload library files until 
# ALl have been done, or we've tried to upload that files 3 times


# List of borked file uploads for one reason or another.
borked = []
while len(retries)!=0:
    for file in list(retries.keys()):
        try:
            print(f"> ampy --port COM{COM} put {folder}/{file} /lib/{file}")
            process = Popen(f"ampy --port COM{COM} put {folder}{file} /lib/{file}")
            process.wait()
            sleep(2)
            del retries[file]
        except Exception as e:
            print(f"-- Couldn't upload {file}, will retry.")
            retries[file] += 1
            if retries[file] == 3:
                borked.append(retries[file])
                print(f"-- {file} is borked.")
                del retries[file]

if len(borked)!=0:
    print("\n The following files could not be uploaded :\n")
    for file in borked:
        print(f"-> {file}")