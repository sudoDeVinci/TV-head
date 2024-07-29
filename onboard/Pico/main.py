from rotaryirq import *
from config import *

from machine import Pin, freq, I2C
from time import sleep_ms
from neopixel import NeoPixel
from micropython import alloc_emergency_exception_buf
from MPU6050 import MPU6050
from gc import collect

alloc_emergency_exception_buf(100)

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
"""
def read_position():
    global mpu
    
    x, y ,z = mpu.sampled_gyro(SAMPLES)
"""

def main() -> None:
    global RENDER_VALUES
    global RUNNING
    global animations
    global CHANNEL
    
    while True:
        animate(animations[RENDER_VALUES[CHANNEL]])



"""
An attempt to overclock the §Pi Pico for higher responsiveness.
Pi Pico to overclockable safely to 240MHz - 270MHz.
Base clock is 125MHz.
"""
try:
    freq(240000000)
    print(f"GOOD TO GO @ {(freq()/1000000):.3f} MHZ")
except Exception as e:
    print("Core overclock not applied.")
    print(f"-> Current speed is: {(freq()/1000000):.3f} MHZ")

# Define display to draw to.
# Display is our array of leds.
display = NeoPixel(Pin(P), N, timing = 1)
# Set up the I2C interface
#i2c = I2C(1, sda = Pin(14), scl = Pin(15))
#print(i2c.scan())
# Set up the MPU6050 class 
#mpu = MPU6050(i2c)
# wake up the MPU6050 from sleep
#mpu.wake()

ROTARYIRQ_BRIGHTNESS = RotaryIRQ(pin_num_clk = 18,
                                pin_num_dt = 19,
                                label = CHANNEL,
                                min_val = 0,
                                max_val = animation_amount - 1,
                                reverse = False,
                                range_mode = Rotary.RANGE_WRAP
                            )


def rot_irq() -> None:
    global ROTARYIRQ_BRIGHTNESS
    global RENDER_VALUES
    global animation_amount
        
    #RENDER_VALUES[ROTARYIRQ_BRIGHTNESS.label()] = (ROTARYIRQ_BRIGHTNESS.value() / 200)
    #print(RENDER_VALUES[ROTARYIRQ_BRIGHTNESS.label()])
    print("***")


ROTARYIRQ_BRIGHTNESS.add_listener(rot_irq)
ROTARYIRQ_BRIGHTNESS.set(value = RENDER_VALUES[ROTARYIRQ_BRIGHTNESS.label()])

while True:
    print(ROTARYIRQ_BRIGHTNESS.value())

main()