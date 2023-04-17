"""
To be able to control the globals  of the esp32 animations via potentiometers,
The pi pico acts as a pseudo schmitt trigger for our analog values.
The different steps/categories of change for each knob is on the esp32, the pico is concerned with
signalling the esp32 when the value of a knob changes drastically, causing an interrupt on the esp32. 
"""
from machine import Pin, ADC
from time import sleep_ms

br_pot = ADC(28)
sp_pot = ADC(27)
an_pot = ADC(26)

br_pin = Pin(10, Pin.OUT)
sp_pin = Pin(11, Pin.OUT)
an_pin = Pin(12, Pin.OUT)


values = {
  "brightness" : 300,
  "speed" : 300,
  "animation" : 300
  }

pins = [
  ["brightness", br_pin],
  ["speed", sp_pin],
  ["animation", an_pin]
]


def signal(key:str):
    global pins
    for pin_details in pins:
        if pin_details[0] == key:
            pin_details[1].value(1)
            sleep_ms(50)
            pins[key].value(0)
            break
    

def compare(key:str, val2:int) -> None:
    global values
    if val2*0.80 <= values[key] <= val2*0.80:
        signal(key, val2)
        values[key] = val2
      
def monitor() -> None:
    global values
    global pins
    for pin in pins:
        pin[1].value(0)
    for i in range(200):
        compare("brightness", br_pot.read_u16())
        compare("speed", sp_pot.read_u16())
        compare("animation", an_pot.read_u16())
        sleep_ms(300)


if __name__ == "__main__":
    monitor()
