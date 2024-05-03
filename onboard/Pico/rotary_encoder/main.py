# MIT License (MIT)
# Copyright (c) 2020 Mike Teachman
# Copyright (c) 2021 Eric Moyer
# https://opensource.org/licenses/MIT

# Platform-specific MicroPython code for the rotary encoder module
# Raspberry Pi Pico implementation

# Documentation:
#   https://github.com/MikeTeachman/micropython-rotary

from machine import Pin, freq
from rotary import Rotary

IRQ_RISING_FALLING = Pin.IRQ_RISING | Pin.IRQ_FALLING


class RotaryIRQ(Rotary):
    def __init__(
        self,
        pin_num_clk,
        pin_num_dt,
        min_val=0,
        max_val=10,
        incr=1,
        reverse=False,
        range_mode=Rotary.RANGE_UNBOUNDED,
        pull_up=False,
        half_step=False,
        invert=False
    ):
        super().__init__(min_val, max_val, incr, reverse, range_mode, half_step, invert)

        if pull_up:
            self._pin_clk = Pin(pin_num_clk, Pin.IN, Pin.PULL_UP)
            self._pin_dt = Pin(pin_num_dt, Pin.IN, Pin.PULL_UP)
        else:
            self._pin_clk = Pin(pin_num_clk, Pin.IN)
            self._pin_dt = Pin(pin_num_dt, Pin.IN)

        self._hal_enable_irq()

    def _enable_clk_irq(self):
        self._pin_clk.irq(self._process_rotary_pins, IRQ_RISING_FALLING)

    def _enable_dt_irq(self):
        self._pin_dt.irq(self._process_rotary_pins, IRQ_RISING_FALLING)

    def _disable_clk_irq(self):
        self._pin_clk.irq(None, 0)

    def _disable_dt_irq(self):
        self._pin_dt.irq(None, 0)

    def _hal_get_clk_value(self):
        return self._pin_clk.value()

    def _hal_get_dt_value(self):
        return self._pin_dt.value()

    def _hal_enable_irq(self):
        self._enable_clk_irq()
        self._enable_dt_irq()

    def _hal_disable_irq(self):
        self._disable_clk_irq()
        self._disable_dt_irq()

    def _hal_close(self):
        self._hal_disable_irq()
       
       
       
       
from machine import Pin, UART
from time import sleep_ms

# Attempt overclock for higher responsiveness
try:
    freq(180000000)
    print("Core overclock applied succesfully!") 
except Exception as e:
    print("Core overclock not applied.")
    
print(f"-> Current speed is: {(freq()/1000000):.3f} MHZ")

channel = RotaryIRQ(pin_num_clk=18,
              pin_num_dt=19,
              min_val=0,
              max_val=20,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_WRAP)


brightness = RotaryIRQ(pin_num_clk=27,
              pin_num_dt=26,
              min_val=0,
              max_val=20,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_WRAP)


br_pin = Pin(10, Pin.OUT)
sp_pin = Pin(11, Pin.OUT)
an_pin = Pin(12, Pin.OUT)


out_pins = (
    ("Brightness", br_pin),
    ("Speed", sp_pin),
    ("Channel", an_pin))


PICO_UART = UART(1, 115200, 5, 4)
PICO_UART.init()


def zfill(string:str, size:int = 0):
    return f"{(size-len(string))*'X'}{string}"


def send_over_UART(string_data:str, value:int):
    #global ADC_PICO_UART
    #PICO_UART.write(zfill(string_data,19)+'\n')
    #sleep_ms(2)
    #PICO_UART.write(zfill(str(value), 19)+'\n')
    print(string_data)

def signal(key:str):
    for pin in out_pins:
        if pin[0] == key:
            pin[1].value(1)
            sleep_ms(10)
            pin[1].value(0)
            break
        

def monitor():
    channel_old = channel.value()
    brightness_old = brightness.value()
    
    while True:
        channel_new = channel.value()
        brightness_new = brightness.value()
        
        if channel_old != channel_new:
            channel_old = channel_new
            signal("Channel")
            send_over_UART("Channel", channel_new)
            print('Channel: ', channel_new)
            
        if brightness_old != brightness_new:
            brightness_old = brightness_new
            signal("Channel")
            send_over_UART("Brightness", brightness_new)
            print('Brightness: ', brightness_new)

        sleep_ms(5)


if __name__ == "__main__":
    monitor()