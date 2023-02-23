from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms
from os import listdir
from sys import exit


# Variable to keep running script or not.
running = True


# The current animation being played
# This is a global value which is changed via the
# Interrupt handler for the buttons.
current_animation = "/csvs/eye"

# Pin numbers to address
p = 16
# Number of leds to address
n = 150

# Define display to draw to
# Display is our array of leds.

# Uncomment for Pi Pico:
display = NeoPixel(Pin(p), n, timing = 1)

# Uncomment for ESP-32:
# display = NeoPixel(Pin(p), n, timing = 1)



def read_frames(folder_path:str) -> list[list[int]]:
    for filename in listdir(folder_path):
        # print("/".join([folder_path, filename]))
        if filename.endswith('.csv'):
            
            frame = []
            with open("/".join([folder_path, filename]), 'r', encoding = "utf-8") as csvfile:
                for line in csvfile:
                  frame.append(line.rstrip('\n').rstrip('\r').split(","))
            animate(frame)


# Clear the display
def clear_display() -> None:
    display.fill((0, 0, 0))
    display.write()



# Play frames with a set time interval in ms.
def animate(frame, sleep:int = 20) -> None:
    # print(frame)
    display.fill((0, 0, 0))
    for p in frame[1:]:
        # print("index: ",p[0], p[1], p[2], p[3])
        display[int(p[0])] = (int(p[1]), int(p[2]), int(p[3]))
    display.write()
    sleep_ms(sleep)

def main() -> None:
    count = 0
    while count < 3:
        read_frames(current_animation)
        count += 1
        
main()
