from machine import Pin, I2C
from oled import Write, GFX, SSD1306_I2C
from oled.fonts import ubuntu_mono_15, ubuntu_mono_20


########################################################################
class Oled_i2c:

    # ----------------------------------------------------------------------
    def __init__(self, scl, sda, rst=16, size=(128, 64)):
        """"""

        i2c = I2C(scl=Pin(scl), sda=Pin(sda))
        Pin(rst, Pin.OUT, value=1)

        self.oled = SSD1306_I2C(size[0], size[1], i2c)
        self.gfx = GFX(size[0], size[1], self.oled.pixel)

        self.fonts = {}

    # ----------------------------------------------------------------------
    def write(self, text, pos, font=ubuntu_mono_15):
        """"""

        if font.__name__ in self.fonts:
            self.fonts[font.__name__].text(text, *pos)
        else:
            self.fonts[font.__name__] = Write(self.oled, font)
            self.fonts[font.__name__].text(text, *pos)

    # ----------------------------------------------------------------------
    def __getattr__(self, attr):
        """"""

        if hasattr(self.oled, attr):
            return getattr(self.oled, attr)

        elif hasattr(self.gfx, attr):
            return getattr(self.gfx, attr)

