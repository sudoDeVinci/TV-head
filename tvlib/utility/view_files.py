"""
This script traverses the file system of the board and prints it in a readbale fashion
"""

from sys import argv
from subprocess import Popen, PIPE
from parsers import parseStringtoInt
from ampy.pyboard import PyboardError

def traverse(paths: list[str], spacing = 0):
    symbol = "└ " if spacing != 0 else " "
    for file in paths:

        out = "\t" * spacing + f"{symbol}{file[1:]}" if file[0]=="/" else  "\t" * spacing + f"{symbol}{file}"

        if "." not in file:
            print(out)
            try:
                process = Popen(f"ampy --port COM{COM} ls {file}", stdout = PIPE)
                inner_paths = process.stdout.read().decode('utf-8').strip()[1:]
                inner_paths = list(inner_paths.split("\r\n"))
                # increment spacing before recursive call
                spacing += 1
                # Call recursively
                traverse(inner_paths, spacing)
                # Decrement spacing once returned.
                spacing -= 1
            except Exception as e:
                print("")
        
        else:
            print(out)
    
    return 

# If there is not a valid second argument for the COM port, default to COM 3.
# First check if there are at least 2 args passed to the script.
# Then check if the [1] arg can be cast to integer.
parsed = parseStringtoInt(argv[1]) if len(argv) >=2 else 6
COM = parsed if parsed else 3

try:
    process = Popen(f"ampy --port COM{COM} ls", stdout = PIPE)
    files = process.stdout.read().decode('utf-8').strip()[1:]
    files = list(files.split("\r\n"))
    if len(files) == 1:
        print("No files on board.")
        exit()
    traverse(files)

except PyboardError as e:
    print(e)

