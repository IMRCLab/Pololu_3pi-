import struct
from machine import Timer, UART, Pin
import uasyncio as asyncio
import micropython
from primitives.queue import Queue, QueueEmpty
from quaternion import Quaternion
from asyncio import Event


class Uart():
    def __init__(self,event:Event, message_decode:list, baudrate:int = 115200,txPin:int =28, rxPin:int = 29,bits:int=8, parity=None, stop:int=1,rxbuf:int=1000):
        self.uart =  UART(0,baudrate = baudrate, tx=Pin(txPin),rx=Pin(rxPin),bits = bits, parity= parity,stop=stop,rxbuf=rxbuf)
        self.event = event
        self.queue_receive = Queue()
        self.message_decode = message_decode
        self.read = asyncio.create_task(self.read_uart())
        self.decode = asyncio.create_task(self.decode_uart())
    
    async def read_uart(self):
        await asyncio.sleep(1)
        while True:
            try:
                await asyncio.sleep(0.01)
                if self.uart.any():
                    new_buffer = bytearray(32)
                    self.uart.readinto(new_buffer)
                    self.queue_receive.put_nowait(new_buffer) 
            except MemoryError:
                print('MemoryError: Receive')
                self.read = asyncio.create_task(self.read_uart())

    async def decode_uart(self):
        await asyncio.sleep(1)
        while True:
            try:
                await asyncio.sleep(0.01)
                buffer = await self.queue_receive.get()
                if buffer[0] == 0x6d and buffer[1] == 0x09: 
                    x = struct.unpack('<h',buffer[3:5])[0]
                    y = struct.unpack('<h',buffer[5:7])[0]
                    z = struct.unpack('<h',buffer[7:9])[0]
                    quaternion = Quaternion(int.from_bytes(buffer[9:13], 'little'))
                    self.message_decode=[x,y,z,quaternion]
                elif buffer[0] == 2 and buffer[1] == 0x05:
                    self.event.set()
                else :
                    print("else")
                    pass
            except:
                print("MemoryError : Decode")        
                self.decode = asyncio.create_task(self.decode_uart())

    async def get_position(self) : # TODO: Add return type 
        return await self.queue_decode.get()