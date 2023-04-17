from machine import Pin, I2C, UART
from oled import Write, SSD1306_I2C
from oled.fonts import ubuntu_mono_15
from time import sleep_ms
import ustruct

scl = Pin(19)
sda = Pin(18)
RX = 35
TX = 34

i2c = I2C(scl=scl, sda=sda)

oled = SSD1306_I2C(128, 64, i2c)
writer = Write(oled, ubuntu_mono_15)

def write_to_oled(writer, value):
    global oled
    writer.text("Got: "+str(value), 0, 0)
    oled.show()

uart = UART(2, baudrate=115200, bits=8, parity=None, stop=1, tx=TX, rx=RX, timeout = 1000)

write_to_oled(writer, "waiting")
while True:
    if uart.any():
        data = uart.read()
        if data is not None:
            write_to_oled(writer,datadecode())
