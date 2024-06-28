# emergency exception buffer allocation
import micropython
micropython.alloc_emergency_exception_buf(100)

#import asyncio
from machine import UART, Pin


class Uart_Bridge():
    def __init__(self,baudrate= 9600,bites = 8, parity =None, stop = 1, tx=Pin(28), rx=Pin(29)): 
        self.baudrate = baudrate
        self.bites = bites
        self.parity = parity
        self.stop = stop
        self.tx = tx
        self.rx = rx
        self.uart = UART(0, baudrate=self.baudrate, tx=self.tx, rx=self.rx, bits=self, parity=None, stop=1)

"""
    async def receiver(self):
    sreader = asyncio.StreamReader(uart)
    while True:
        res = await sreader.readline()
        print('Recieved', res)
"""


