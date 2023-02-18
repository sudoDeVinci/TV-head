"""
Boilerplate from :
https://randomnerdtutorials.com/micropython-ws2812b-addressable-rgb-leds-neopixel-esp32-esp8266/
Idea from:
https://rose.systems/tv_head/
"""

from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms
from os import listdir
from micropython import alloc_emergency_exception_buf



# The current animation being played
# This is a global value which is changed via the
# Interrupt handler for the buttons.
current_animation = "/csvs/base/"



# Pin numbers to address
p = 16
# Number of leds to address
n = 100

# Define display to draw to
# Display is our array of leds.
display = NeoPixel(Pin(p), n)



# Buttons to be mapped to animations
button1 = Pin(17, Pin.IN, Pin.PULL_DOWN)
button2 = Pin(18, Pin.IN, Pin.PULL_DOWN)
button3 = Pin(19, Pin.IN, Pin.PULL_DOWN)



def read_frames(folder_path:str) -> list[list[int]]:
    frames = []

    for filename in listdir(folder_path):
        if filename.endswith('.csv'):
            frame = []
            with open("/".join([folder_path, filename]), 'r', encoding = "utf-8") as csvfile:
                for line in csvfile:
                  frame.append(line.rstrip('\n').rstrip('\r').split(","))
                frames.append(frame)
    return frames



# Clear the display
def clear_display() -> None:
    global n
    for i in range(n):
        display[i] = (0, 0, 0)
    display.write()



# Play frames with a set time interval in ms.
def animate(frames_path:str, sleep:int = 300) -> None:
    global n
    frames = read_frames(frames_path)

    for frame in frames:
        for i in range(n):
            display[i] = (0, 0, 0)
        for p in frame[1:]:
            display[int(p[0])] = (int(p[1]), int(p[2]), int(p[3]))
        display.write()
        sleep_ms(sleep)
        #clear_display()



def main() -> None:
    global current_animation
    alloc_emergency_exception_buf(100)
    loop = 0
    while loop < 5:
        loop += 1
        animate(current_animation)
  

if __name__ == '__main__':
  main()