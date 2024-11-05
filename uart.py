import struct
from machine import Timer, UART, Pin
import uasyncio as asyncio
import micropython

class Uart():
    def __init__(self, baudrate:int = 115200,txPin:int =28, rxPin:int = 29,bits:int=8, parity=None, stop:int=1,rxbuf:int=1000):
        self.uart =  UART(0,baudrate = baudrate, tx=Pin(txPin),rx=Pin(rxPin),bits = bits, parity= parity,stop=stop,rxbuf=rxbuf)
        self.list_receive = list()
        self.list_decode = list()
        self.read = asyncio.create_task(self.read_uart)
        self.decode = asyncio.create_task(self.decode_uart)
    
    async def read_uart(self):
        await asyncio.sleep(1)
        while True:
            await asyncio.sleep(0)
            if self.uart.any():
                new_buffer = bytearray(32)
                self.uart.readinto(new_buffer)
                self.list_receive.append(new_buffer) 

    async def decode_uart(self):
        await asyncio.sleep(1)
        while True:
            await asyncio.sleep(0)
            try:
                buffer = self.list_receive.pop(0)
                if buffer[0] == 1:
                    print("1")
                    pass
                elif buffer[0] == 2:
                    print("2")
                    pass
                else :
                    print("else")
                    pass
            except:
                pass
                
    def read_position(self):
        result = None
        try:
            result = self.list_decode.pop(0)
        except:
            result = None
    
        return result