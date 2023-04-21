"""
To be able to control the globals  of the esp32 animations via potentiometers,
The pi pico acts as a pseudo schmitt trigger for our analog values.
The different steps/categories of change for each knob is on the other pico. 
This pico is concerned with signalling the other pico when the value of a knob changes
drastically, causing an interrupt on the other pico.
"""
from machine import Pin, ADC, UART
from time import sleep_ms
import machine
from math import sqrt, pow


br_pot = ADC(28)
sp_pot = ADC(27)
an_pot = ADC(26)


br_pin = Pin(10, Pin.OUT)
sp_pin = Pin(11, Pin.OUT)
an_pin = Pin(12, Pin.OUT)


out_pins = (
    ("Brightness", br_pin),
    ("Speed", sp_pin),
    ("Channel", an_pin))


values = {
    "Brightness":0,
    "Speed":0,
    "Channel":0
    }


ADC_PICO_UART = UART(1, 115200, 5, 4)
ADC_PICO_UART.init()


def zfill(string:str, size:int = 0):
    return f"{(size-len(string))*'X'}{string}"


def send_over_UART(string_data:str, value:int):
    global ADC_PICO_UART
    ADC_PICO_UART.write(zfill(string_data,19)+'\n')
    sleep_ms(2)
    ADC_PICO_UART.write(zfill(str(value), 19)+'\n')


def signal(key:str):
    for pin in out_pins:
        if pin[0] == key:
            pin[1].value(1)
            sleep_ms(10)
            pin[1].value(0)
            break

    
def compare(key:str, val2:int) -> None:
    global values
    if values[key]*0.80 <= val2 <= values[key]*1.2:
        return
    signal(key)
    print(key,": ",str(val2))
    values[key] = val2
    send_over_UART(key, val2)
    

def average_reading(pin:Pin, amount:int):
    readings = []
    pin.read_u16()
    for _ in range(amount):
        readings.append(pin.read_u16())
        sleep_ms(2)
    
    # Filter readings by standard deviation
    std, mean=std_dev(readings)
    u_b =  mean+(std*2)
    l_b =  mean-(std*2)
    filtered = tuple(reading for reading in readings if l_b<=reading<=u_b) 
    average = int(sum(filtered)/len(filtered))
    
    # Map our logarithmic value to a linear range 0-1000
    outrange = ((average/65535)**10)*10000

    return int(outrange)


def std_dev(readings):
    #print("Readings: \n",readings)
    mean = sum(readings)/len(readings)
    #print("\nMean: ", mean)
    sum_mean_delta_sq = sum((reading-mean)**2 for reading in readings)
    std = sqrt(sum_mean_delta_sq/(len(readings)-1))

    return std, mean


def monitor() -> None:
    global values
    global out_pins

    for pin in out_pins:
        pin[1].value(0)
    
    #print("Here!")
    
    while True:
        br_avg = average_reading(br_pot, 50)
        compare("Brightness", br_avg)
        sp_avg = average_reading(sp_pot, 50)
        compare("Speed", sp_avg)
        an_avg = average_reading(an_pot, 50)
        compare("Channel", an_avg)
        sleep_ms(10)


if __name__ == "__main__":
    monitor()