import struct
from machine import Timer, UART, Pin
import uasyncio as asyncio
import micropython
from primitives.queue import Queue, QueueEmpty
from quaternion import Quaternion

class Uart():
    def __init__(self, baudrate:int = 115200,txPin:int =28, rxPin:int = 29,bits:int=8, parity=None, stop:int=1,rxbuf:int=1000):
        self.uart =  UART(0,baudrate = baudrate, tx=Pin(txPin),rx=Pin(rxPin),bits = bits, parity= parity,stop=stop,rxbuf=rxbuf)
        self.list_receive = Queue()
        self.list_decode = Queue()
        self.read = asyncio.create_task(self.read_uart())
        self.decode = asyncio.create_task(self.decode_uart())
    
    async def read_uart(self):
        await asyncio.sleep(1)
        while True:
            await asyncio.sleep(0)
            if self.uart.any():
                new_buffer = bytearray(32)
                self.uart.readinto(new_buffer)
                self.list_receive.put_nowait(new_buffer) 

    async def decode_uart(self):
        await asyncio.sleep(1)
        while True:
            await asyncio.sleep(0)
            buffer = await self.list_receive.get()
            if buffer[0] == 0x6d and buffer[1] == 0x09: 
                x = struct.unpack('<h',buffer[3:5])
                y = struct.unpack('<h',buffer[5:7])
                z = struct.unpack('<h',buffer[7:9])
                quaternion = Quaternion(int.from_bytes(buffer[9:13], 'little'))
                self.list_decode.put_nowait([x,y,z,quaternion])
            elif buffer[0] == 2:
                print("2")
                pass
            else :
                print("else")
                pass
                
    async def get_position(self) : # TODO: Add return type 
        return await self.list_decode.get()
