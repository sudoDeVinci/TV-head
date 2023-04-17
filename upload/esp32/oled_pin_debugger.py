from machine import Pin, I2C, UART
from oled import Write, SSD1306_I2C
from oled.fonts import ubuntu_mono_15
from time import sleep_ms
import ustruct

scl = Pin(19)
sda = Pin(18)
rx = 35
tx = 34

br_pin = Pin(25, Pin.IN)
sp_pin = Pin(26, Pin.IN)
an_pin = Pin(27, Pin.IN)
uart = UART(0, baudrate=115200, bits=8, parity=None, stop=1, tx=34, rx=35, timeout = 1000)
i2c = I2C(scl=scl, sda=sda)

oled = SSD1306_I2C(128, 64, i2c)
writer = Write(oled, ubuntu_mono_15)

pins = [
    [br_pin,("Brightness",0,0)],
    [sp_pin,("Speed",0,15)],
    [an_pin,("Channel",0,30)]
    ]

values = {
  "Brightness" : 0.5,
  "Speed" : 0.0,
  "Channel" : 0.0
  }

def handle_interrupt(pin):
    global pins
    global writer
    string_data, int_data = read_from_UART()
    for pin_details in pins:
        if pin_details[0] == string_data:
            write_to_oled(writer, pin_details[1], int_data)
            values[string_data] = int_data
            break
        

br_pin.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
sp_pin.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
an_pin.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)
    

def write_to_oled(writer, fields, value):
    global oled
    name, hor, vert = fields
    writer.text(name+"     "+str(value), hor, vert)
    oled.show()
    
def read_from_UART():
        data = uart.read(18) # read 18 bytes (16-byte string + 2-byte integer) from UART buffer
        unpacked_data = ustruct.unpack("<16sH", data) # unpack the data
        string_data = unpacked_data[0].decode().strip('\x00') # extract the string and remove any trailing null bytes
        int_data = unpacked_data[1] # extract the integer
        print("\t> Received: ",string_data,"\t",value)
        return (string_data, int_data)
        
def main():
    global writer
    write_to_oled(writer, pins[0][1], values["Brightness"])
    write_to_oled(writer, pins[1][1], values["Speed"])
    write_to_oled(writer, pins[2][1], values["Channel"])

    while True:
        sleep_ms(50)
    
if __name__ == '__main__':
    main()