"""
To be able to control the globals  of the esp32 animations via potentiometers,
The pi pico acts as a pseudo schmitt trigger for our analog values.
The different steps/categories of change for each knob is on the esp32, the pico is concerned with
signalling the esp32 when the value of a knob changes drastically, causing an interrupt on the esp32. 
"""
from machine import Pin, ADC, UART
from time import sleep_ms
import machine
import ustruct

TX = 4
RX = 5
# initialize UART with baudrate of 115200, 8 data bits, no parity, 1 stop bit, and pins 1 and 0 for TX and RX, respectively
uart = UART(1, baudrate=115200, bits=8, parity=None, stop=1, tx=Pin(TX), rx=Pin(RX),timeout=1000)

def send_over_UART(string_data):
    # pack a tuple containing a string and a 16-bit number
    uart.write(string_data)
    print("> Sent: ",string_data)
    
while True:
    send_over_UART("TEST\n")
    sleep_ms(2000)

