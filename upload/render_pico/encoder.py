"""
TCP handler class taken from Mark Tolonen on Stackoverflow, Answered on Apr 2, 2020 ,
originally asked at https://stackoverflow.com/questions/60986276/python-tcp-networking-inconsistencies
"""

from socket import *
import struct

class Encoder:
    '''Buffer the TCP stream and extract meaningful data on message boundaries.'''

    def __init__(self,sock):
        self.sock = sock
        self.buffer = b''

    def __enter__(self):
        return self

    def __exit__(self,*args):
        self.sock.close()

    def __get_raw__(self,size) -> bytes:
        '''Request a specific number of bytes to extract from the stream.'''
        while len(self.buffer) < size:
            data = self.sock.recv(4096)
            if not data: # server closed
                return b''
            self.buffer += data
        msg,self.buffer = self.buffer[:size],self.buffer[size:]
        return msg

    def get(self):
        '''Extract a message from the stream.'''
        raw = self.__get_raw__(4)  # Get the 4-byte length data
        if not raw:
            return b''
        length = struct.unpack('<I',raw)[0]
        return self.__get_raw__(length) # Return the actual message


