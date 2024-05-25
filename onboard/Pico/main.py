from rotaryirq import *
from config import *

from machine import Pin, freq
from time import sleep_ms
from neopixel import NeoPixel
from micropython import alloc_emergency_exception_buf
import MPU6050
import _thread
from gc import collect

alloc_emergency_exception_buf(100)

# Define display to draw to.
# Display is our array of leds.
display = NeoPixel(Pin(P), N, timing = 1)
# Set up the I2C interface
i2c = machine.I2C(1, sda=machine.Pin(14), scl=machine.Pin(15))
# Set up the MPU6050 class 
mpu = MPU6050.MPU6050(i2c)
# wake up the MPU6050 from sleep
mpu.wake()

def clear() -> None:
    """
    Clear the display.
    """
    global display
    display.fill((0,0,0))
    display.write()


def animate(frames: Tuple[Tuple[Tuple[int, int, int, int]]]) -> None:
    """
    Play frames with a set time interval in ms.
    """
    global display
    global RENDER_VALUES
    global BRIGHTNESS
    global CHANNEL
    global SPEED
    
    b = RENDER_VALUES[BRIGHTNESS]
    ch = RENDER_VALUES[CHANNEL]
    for frame in frames:
        for p in frame:
            if RENDER_VALUES[CHANNEL] != ch or RENDER_VALUES[BRIGHTNESS] != b:
                clear()
                return
            display[p[0]] = int(p[3]*b), int(p[2]*b), int(p[1]*b)
        display.write()
        sleep_ms(int(RENDER_VALUES[SPEED]*20))
    
    for i in range(100):
        if RENDER_VALUES[CHANNEL] != ch or RENDER_VALUES[BRIGHTNESS] != b:
            clear()
            return
        sleep_ms(int(RENDER_VALUES[SPEED]*50))

def main() -> None:
    global RENDER_VALUES
    global RUNNING
    global animations
    global CHANNEL
    
    while True:
        animate(animations[RENDER_VALUES[CHANNEL]])
        collect()

main()