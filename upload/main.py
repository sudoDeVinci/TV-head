"""
Boilerplate from :
https://randomnerdtutorials.com/micropython-ws2812b-addressable-rgb-leds-neopixel-esp32-esp8266/
Idea from:
https://rose.systems/tv_head/

This works currently with a 12 x 8 LED array.
"""

from machine import Pin
from neopixel import NeoPixel
from time import sleep_ms
from os import listdir

# define interrupt handling functions
def button_handler(pin):
#change global to be used in while loop
  clear_display()
  global button_pressed
  button_pressed = pin

# configure pushbuttons as interrupts
# Button to play base animation
button1 = Pin(15, Pin.IN)
button1.irq(trigger=Pin.IRQ_RISING, handler=button_handler)

# Button to play blinking nimation
button2 = Pin(14, Pin.IN)
button2.irq(trigger=Pin.IRQ_RISING, handler=button_handler)

# Button to play eye movement animation
button3 = Pin(13, Pin.IN)
button3.irq(trigger=Pin.IRQ_RISING, handler=button_handler)

button_pressed = button1

# Pin numbers to address
p = 5
# Number of leds to address
n = 96
# Define display to draw to
# Display is our array of leds.
display = NeoPixel(Pin(p), n)


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
  for i in range(n):
    display[i] = (0, 0, 0)
  display.write()


# Play frames with a set time interval in ms.
def animate(frames_path:str, sleep:int = 83) -> None:
  frames = read_frames(frames_path)

  for frame in frames:
    for p in frame[1:]:
      display[p[0]] = (p[1], p[2], p[3])
    display.write()
    sleep_ms(sleep)


def main():
  while True:
    if button_pressed is button1:
      animate("/csvs/base")
    elif button_pressed is button2:
      animate("/csvs/blink")
    elif button_pressed is button3:
      animate("/csvs/eye_movement")
    else:
      print("bruh")
  

if __name__ == '__main__':
  main()