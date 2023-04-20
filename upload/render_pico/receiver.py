from machine import Pin, I2C, UART
from time import sleep_ms

RX = 35
TX = 34

uart = UART(1, baudrate=9600)

while True:
    uart.write('ACK')
    print("Sent: ACK")
    sleep_ms(2000)
    
