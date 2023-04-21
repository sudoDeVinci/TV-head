"""
Boilerplate from :
https://randomnerdtutorials.com/micropython-ws2812b-addressable-rgb-leds-neopixel-esp32-esp8266/
Idea from:
https://rose.systems/tv_head/
"""


from machine import Pin, UART, I2C
from neopixel import NeoPixel
from time import sleep_ms
from os import listdir, ilistdir
from math import pow
from random import randint

from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd


I2C_ADDR     = 39
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

i2c = I2C(1, sda=machine.Pin(26), scl=machine.Pin(27), freq=500000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)


br_pin = Pin(10, Pin.IN)
sp_pin = Pin(11, Pin.IN)
an_pin = Pin(12, Pin.IN)

uart = UART(1,115200, rx=Pin(5), tx=Pin(4))
uart.init()

# Variable to keep running script or not.
running = True

#Folder for animation csvs
animation_folder = "/csvs/"

def get_animations(folder_path = animation_folder) -> list[str]:
    folders = [animation_folder+file[0] for file in ilistdir(folder_path) if file[1] == 0x4000]
    return folders
animations = get_animations()
animation_amount = len(animations)-1
 
# Pin number to address
p = 15
# Number of leds to address
n = 96

# Define display to draw to
# Display is our array of leds.

display = NeoPixel(Pin(p), n, timing = 1)

uart = UART(1,115200, rx=Pin(5), tx=Pin(4))
uart.init()

pins = (
    (br_pin,"Brightness"),
    (sp_pin,"Speed"),
    (an_pin,"Channel"))

values = {
  "Brightness" : 0.5,
  "Speed" : 10,
  "Channel" : 0
  }



def recv():
    global uart
    while uart.any() < 40:
        pass
    
    #print("BUFFER: ", uart.any())
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
    
    int_data = int(int_data)
    if string_data == "Brightness":
        scaled =  int_data/10000
    elif string_data == "Channel":
        # scaled = map_to_range(int_data, animation_amount, True)
        scaled = int_data%animation_amount
    elif string_data == "Speed":
        scaled = map_to_range(int_data, 5000, True)
        if scaled == 0:
            scaled = 10
        
    values[string_data] = scaled
        
    print("Got: ",string_data, " | ",scaled )
        

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


def map_to_range(input_value, range_max, is_int:bool = False):
    scaled = ((input_value/10000)**10)*range_max

    if is_int:
        return int(scaled)
    return scaled


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
        #print(animations[values['Channel']])
        read_frames(animations[values['Channel']])
        sleep_ms(values['Speed']*10)
  

if __name__ == '__main__':
    main()
    clear()