from rotaryirq import ROTARYIRQ_BRIGHTNESS
from machine import Pin, freq, I2C
from neopixel import NeoPixel
from micropython import alloc_emergency_exception_buf
from MPU6050 import MPU6050
import uasyncio as asyncio
from typing import Tuple
from config import (RENDER_VALUES, BRIGHTNESS, CHANNEL, SPEED,
                    animations, P, N, debug)

alloc_emergency_exception_buf(100)


def clear() -> None:
    """
    Clear the display.
    """
    global display
    display.fill((0, 0, 0))
    display.write()


async def read_gyro():
    global mpu

    while True:
        if mpu is None:
            await asyncio.sleep_ms(250)
        else:
            x, y, z = mpu.sampled_gyro(20)

            """
            TODO:
            if over 250, one animation, if under -250, another animation.
            """
            if x > 240:
                pass
            if x < -240:
                pass
            await asyncio.sleep_ms(50)


async def render(frames: Tuple[Tuple[Tuple[int, int, int, int]]]) -> bool:

    b = RENDER_VALUES[BRIGHTNESS]
    ch = RENDER_VALUES[CHANNEL]
    for frame in frames:
        for p in frame:
            if RENDER_VALUES[CHANNEL] != ch or RENDER_VALUES[BRIGHTNESS] != b:
                return 1
            display[p[0]] = int(p[3]*b), int(p[2]*b), int(p[1]*b)
        display.write()
        await asyncio.sleep_ms(int(RENDER_VALUES[SPEED]*100))
    return 0


async def animate() -> None:
    global RENDER_VALUES
    global CHANNEL
    global BRIGHTNESS

    """
    Play frames with a set time interval in ms.
    """

    while True:
        b = RENDER_VALUES[BRIGHTNESS]
        ch = RENDER_VALUES[CHANNEL]

        current_frames = animations[RENDER_VALUES[CHANNEL]]

        render_value = await render(current_frames)
        if render_value:
            clear()
            continue

        for i in range(100):
            if RENDER_VALUES[CHANNEL] != ch or RENDER_VALUES[BRIGHTNESS] != b:
                clear()
                break
            await asyncio.sleep_ms(int(RENDER_VALUES[SPEED]*50))


async def main() -> None:
    global RENDER_VALUES
    global animations
    global CHANNEL

    clear()
    asyncio.create_task(animate())
    asyncio.create_task(read_gyro())
    while True:
        await asyncio.sleep_ms(10_000_000)


"""
An attempt to overclock the §Pi Pico for higher responsiveness.
Pi Pico to overclockable safely to 240MHz - 270MHz.
Base clock is 125MHz.
"""
try:
    freq(240000000)
except Exception:
    debug("Core overclock not applied.")

print(f"-> Current speed is: {(freq()/1000000):.3f} MHZ")

# Define display to draw to.
# Display is our array of leds.
display = NeoPixel(Pin(P), N, timing=1)
# Set up the I2C interface
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
# Set up the MPU6050 class
mpu = MPU6050(i2c)
# wake up the MPU6050 from sleep
mpu.wake()

ROTARYIRQ_BRIGHTNESS.set(value=RENDER_VALUES[ROTARYIRQ_BRIGHTNESS.label()])

asyncio.run(main())
