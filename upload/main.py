"""
Boilerplate from :
https://randomnerdtutorials.com/micropython-ws2812b-addressable-rgb-leds-neopixel-esp32-esp8266/
Idea from:
https://rose.systems/tv_head/
"""



from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms
from os import listdir, path
from random import randint



# Variable to keep running script or not.
running = True



# The current animation being played
# This is a global value which is changed via the
# Interrupt handler for  the buttons.
current_animation = "/csvs/big_eye"
 
# Pin numbers to address
p = 16
# Number of leds to address
n = 100

# Define display to draw to
# Display is our array of leds.


# Uncomment for ESP-32:
display = NeoPixel(Pin(p), n, timing = 1)

def read_frames(folder_path:str) -> list[list[int]]:

    for filename in listdir(folder_path):
        if filename.endswith('.csv'):
            with open("/".join([folder_path, filename]), 'r', encoding = "utf-8") as csvfile:
                frame = tuple((line.rstrip('\n').rstrip('\r').split(",")) for line in csvfile)
            animate(frame)


def get_animations(folder_path = "/csvs/") -> list[str]:
    folders = [name for name in listdir(folder_path) if path.isdir(name)]

            

# Clear the display
def clear_display() -> None:
    display.fill((0, 0, 0))
    display.write()


# Play frames with a set time interval in ms.
def animate(frame, sleep:int = 0) -> None:
    for p in frame[1:]:
        display[int(p[0])] = (int(p[3]), int(p[2]), int(p[1]))
    display.write()
    # sleep_ms(sleep)


def main() -> None:
    animations = ["/csvs/big_eye","/csvs/blink","/csvs/smile","/csvs/question","/csvs/standby"]
    
    global current_animation
    global running
    while running:
        animation_index = randint(0, len(animations)-1)
        current_animation = animations[animation_index]
        
        if current_animation in ("/csvs/big_eye","/csvs/blink","/csvs/question"):
            animation_length = randint(2,5)
        else:
            animation_length = randint(100, 200)
        
        
        for i in range(animation_length):
            read_frames(current_animation)
  

if __name__ == '__main__':
    main()
    clear_display()