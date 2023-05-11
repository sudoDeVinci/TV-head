
"""
Boilerplate from :
https://randomnerdtutorials.com/micropython-ws2812b-addressable-rgb-leds-neopixel-esp32-esp8266/
Idea from:
https://rose.systems/tv_head/
"""


from machine import Pin, UART,freq
from neopixel import NeoPixel
from time import sleep_ms
from os import listdir, ilistdir
from math import pow
from random import randint

br_pin = Pin(10, Pin.IN)
sp_pin = Pin(11, Pin.IN)
an_pin = Pin(12, Pin.IN)

uart = UART(1,115200, rx=Pin(5), tx=Pin(4))
uart.init()

# Attempt overclock for higher responsiveness
try:
    freq(200000000)
    print("Core overclock applied succesfully!") 
except Exception as e:
    print("Core overclock not applied.")
    
print(f"-> Current speed is: {(freq()/1000000):.3f} MHZ")

# Variable to keep running script or not.
running = True

#Folder for animation csvs
animation_folder = "/csvs/"

def get_animations(folder_path = animation_folder) -> tuple[str]:
    folders = tuple(animation_folder+file[0] for file in ilistdir(folder_path) if file[1] == 0x4000)
    return folders
animations = get_animations()
animation_amount = len(animations)-1
 
# Pin number to address
p = 16
# Number of leds to address
n = 100

# Define display to draw to
# Display is our array of leds.
display = NeoPixel(Pin(p), n, timing = 1)


pins = (
    (br_pin,"Brightness"),
    (sp_pin,"Speed"),
    (an_pin,"Channel"))


values = {
  "Brightness" : 0.10,
  "Speed" : 40,
  "Channel" : 0
  }

def zfill(string:str, size:int = 0):
    return f"{(size-len(string))*'0'}{string}"


# Receive value from rotary encoder via other pico
def recv():
    global uart
    while uart.any() < 40:
        pass
    
    data = uart.readline()
    try:
        data = data.decode('utf-8')
        if '\n' in data:
            data = data.rstrip('\n')
            string = data.replace('X', '')
        #print("Got: ", data.replace('X', ''))
    except Exception as e:
        print("Couldn't decode ", data)
        return (None,None)
        
    sleep_ms(5)
    
    data = uart.readline()
    try:
        data = data.decode('utf-8')
        if '\n' in data:
            data = data.rstrip('\n')
            value = data.replace('X', '')
        #print("Got: ", data.replace('X', ''))
    except Exception as e:
        print("Couldn't decode ", data)
        return (None,None)
    
    return (string, value)


def handle_interrupt(pin):
    global pins
    global values
    global animation_amount
    
    string_data, int_data = recv()
    if string_data is None or int_data is None:
        return
    
    # Try to convert integer portion
    try:
        int_data = int(int_data)
    except Exception as e:
        # It is sometimes the case that the data arrives OUT OF ORDER and our
        # int and string data is swapped. We attempt to swap and convert them.
        # If this does not work, simply say the data is worngly transmitted and continue.
        try:
            intermediate = int_data
            int_data = int(string_data)
            string_data= intermediate
        except Exception as ex:
            print("Data corrupt/wrong order.")
            return
    if string_data == "Brightness":
        int_data = int_data/20
    elif string_data == "Channel":
        int_data = int_data%animation_amount
        clear()
    values[string_data] = int_data

    print("Got: ",string_data, " | ",int_data )
        

br_pin.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
sp_pin.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
an_pin.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)


def read_frames(folder_path:str) -> list[list[int]]:
    global animations
    for filename in listdir(folder_path):
        if folder_path != animations[values['Channel']]:
            return
        if filename.endswith('.csv'):
            with open("/".join([folder_path, filename]), 'r', encoding = "utf-8") as csvfile:
                frame = tuple((line.rstrip('\n').rstrip('\r').split(",")) for line in csvfile)
            animate(frame)

def clear():
    global display
    display.fill((0,0,0))
    display.write()       


# Play frames with a set time interval in ms.
def animate(frame) -> None:
    global dispaly
    b = values["Brightness"]
    for p in frame[1:]:
        display[int(p[0])] = (int(int(p[3])*b), int(int(p[2])*b), int(int(p[1])*b))
    display.write()
    sleep_ms(values["Speed"])


def main() -> None:
    global animations
    global values
    global running


    while running:
        #print(f"Playing: {animations[values['Channel']]}")
        read_frames(animations[values['Channel']])
        sleep_ms(values["Speed"]*10)
  

if __name__ == '__main__':
    try:
        main()
    except Exception as e:    
        print(e)
        clear()
     