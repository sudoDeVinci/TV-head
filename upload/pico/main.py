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


br_pot = ADC(28)
sp_pot = ADC(27)
an_pot = ADC(26)

br_pin = Pin(10, Pin.OUT)
sp_pin = Pin(11, Pin.OUT)
an_pin = Pin(12, Pin.OUT)

TX = 4
RX = 5
# initialize UART with baudrate of 115200, 8 data bits, no parity, 1 stop bit, and pins 1 and 0 for TX and RX, respectively
uart = UART(1, baudrate=115200, bits=8, parity=None, stop=1, tx=Pin(TX), rx=Pin(RX))


values = {
  "Brightness" : 0,
  "Speed" : 0,
  "Channel" : 0
  }

pins = [
  ["Brightness", br_pin],
  ["Speed", sp_pin],
  ["Channel", an_pin]
]

def signal(key:str):
    global pins
    for pin_details in pins:
        if pin_details[0] == key:
            pin_details[1].value(1)
            sleep_ms(50)
            pin_details[1].value(0)
            break

def send_over_UART(string_data, value):
    # pack a tuple containing a string and a 16-bit number
    data = (string_data, value)
    packed_data = ustruct.pack("<16sH", data[0].encode(), data[1])

    # send the packed data over UART
    uart.write(packed_data)
    print("\t> Sent: ",string_data,"\t",value)


def compare(key:str, val2:int) -> None:
    global values
    if values[key]*0.75 <= val2 <= values[key]*1.25:
        return
    signal(key)
    print(key + ": " + str(val2))
    values[key] = val2
    send_over_UART(key, val2)
    
def average_reading(pin):
    readings = []
    for i in range(30):
        readings.append(pin.read_u16())
        sleep_ms(5)
    return int(sum(readings)/30)
      
def monitor() -> None:
    global values
    global pins
    for pin in pins:
        pin[1].value(0)
    while True:
        br_avg = average_reading(br_pot)
        compare("Brightness", br_avg)
        sp_avg = average_reading(sp_pot)
        compare("Speed", sp_avg)
        an_avg = average_reading(an_pot)
        compare("Channel", an_avg)
        sleep_ms(300)


if __name__ == "__main__":
    monitor()