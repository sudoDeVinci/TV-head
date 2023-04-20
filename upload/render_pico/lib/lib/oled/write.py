"""
Write
=====


"""


########################################################################
class Write:
    """"""
    # ----------------------------------------------------------------------

    def __init__(self, buffer, font):
        """Initialize a writer for custom font.
                
        Parameters
        ----------
        buffer : oled handler object
            This object must have the `.pixel` object.
        font : str
            The python module with the font.
        
        """

        self.buffer = buffer
        self.font = font._FONT

    # ----------------------------------------------------------------------
    def text(self, string, x0=0, y0=0, color=0xffff, bgcolor=0, colors=None):
        """Write a string win position x0, y0.
        
        Load from bitmat font and write character by character using
        `buffer.pixel`.
        
        Parameters
        ----------
        string : str
            The message to write.
        x0 : int
            X possition.
        y0 : int
            Y possition.
    
        """

        buffer = self.buffer
        font = self.font

        if colors is None:
            colors = (color, color, bgcolor, bgcolor)

        x = x0
        for c in string:

            if not ord(c) in font.keys():
                c = "?"

            row = y0
            _w, * _font = font[ord(c)]
            for byte in _font:
                unsalted = byte
                for col in range(x, x + _w):
                    color = colors[unsalted & 0x03]
                    if color is not None:
                        buffer.pixel(col, row, color)
                    unsalted >>= 2
                row += 1
            x += _w

    # ----------------------------------------------------------------------

    def char(self, c, x0=0, y0=0, color=0xffff, bgcolor=0, colors=None):
        """"""
        buffer = self.buffer
        font = self.font

        if colors is None:
            colors = (color, color, bgcolor, bgcolor)

        x = x0
        # for c in string:
        if not c in font.keys():
            return 0

        row = y0
        _w, * _font = font[c]
        for byte in _font:
            unsalted = byte
            for col in range(x, x + _w):
                color = colors[unsalted & 0x03]
                if color is not None:
                    buffer.pixel(col, row, color)
                unsalted >>= 2
            row += 1
        x += _w

