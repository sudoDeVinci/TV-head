"""
Clear all files from the board.
"""

import os
from time import sleep
from subprocess import Popen, PIPE
from parsers import parseStringtoInt
from sys import argv

# If there is not a valid second argument for the COM port, default to COM 3.
# First check if there are at least 2 args passed to the script.
# Then check if the [1] arg can be cast to integer.
parsed = parseStringtoInt(argv[1]) if len(argv) >=2 else 6
COM = parsed if parsed else 3

try:
    process = Popen(f"ampy --port COM{COM} ls", stdout = PIPE)
    files = process.stdout.read().decode('utf-8').strip()[1:]
except Exception as e:
        print(e)  

ls = list(files.split("\r\n"))

if len(ls) == 1:
    print("No files on board.")
    exit()

for file in ls:
    print(f"> {file}")
print("\n")

for file in ls:

    # We just assume that regular files dont have periods in the name.
    if "." not in file:
        cmd = f"ampy --port COM{COM} rmdir {file}"

    # We assume everything else is a file of some type.
    else: 
        cmd = f"ampy --port COM{COM} rm {file}"
    
    # Now actually execute command.
    try:
        print(">>> ",cmd)
        process = Popen(cmd, stdout = PIPE)
        process.wait()
        sleep(2)
    except Exception as e:
        print(f"-- Couldn't delete {file}, will retry.")
