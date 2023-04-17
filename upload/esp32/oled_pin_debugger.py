from machine import Pin, I2C
from oled import Write, SSD1306_I2C
from oled.fonts import ubuntu_mono_15
from time import sleep_ms

scl = Pin(19)
sda = Pin(18)
rx = 35
tx = 34

br_pin = Pin(25, Pin.IN)
sp_pin = Pin(26, Pin.IN)
an_pin = Pin(27, Pin.IN)

i2c = I2C(scl=scl, sda=sda)
oled = SSD1306_I2C(128, 64, i2c)
writer = Write(oled, ubuntu_mono_15)

pins = [
    [br_pin,("Brightness: ",0,0)],
    [sp_pin,("Speed:      ",0,15)],
    [an_pin,("Channel:    ",0,30)]
    ]

def handle_interrupt(pin):
    global pins
    global writer
    
    for pin_details in pins:
        if pin_details[0] == pin:
            write_to_oled(writer, pin_details[1], pin.value())
            break

br_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_RISING, handler=handle_interrupt)
sp_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_RISING, handler=handle_interrupt)
an_pin.irq(trigger=Pin.IRQ_RISING | Pin.IRQ_RISING, handler=handle_interrupt)


    

def write_to_oled(writer, fields, value):
    global oled
    name, hor, vert = fields
    #print("Writing: ",name, value, hor, vert)
    writer.text(name+str(value), hor, vert)
    oled.show()
    
def main():
    global writer
    write_to_oled(writer, pins[0][1], br_pin.value())
    write_to_oled(writer, pins[1][1], sp_pin.value())
    write_to_oled(writer, pins[2][1], an_pin.value())
    
    while True:
        sleep_ms(50)
    
if __name__ == '__main__':
    main()