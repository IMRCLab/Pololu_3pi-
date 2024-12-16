import struct
from machine import Timer, UART, Pin
import uasyncio as asyncio
import micropython
from primitives.queue import Queue, QueueEmpty
from quaternion import Quaternion
from asyncio import Event


class Uart():
    def __init__(self,first_message:Event,event:Event, baudrate:int = 115200,txPin:int =28, rxPin:int = 29,bits:int=8, parity=None, stop:int=1,rxbuf:int=1000):
        self.uart =  UART(0,baudrate = baudrate, tx=Pin(txPin),rx=Pin(rxPin),bits = bits, parity= parity,stop=stop,rxbuf=rxbuf)
        self.event = event
        self.queue_receive = Queue()
        self.message_decode = tuple()
        self.read = asyncio.create_task(self.read_uart())
        self.decode = asyncio.create_task(self.decode_uart())
        self.first_message = first_message
    
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
        drone_number = 0xe7      
        while True:
            try:
                await asyncio.sleep(0.01)
                buffer = await self.queue_receive.get()
                #print(buffer)
                if buffer[0] == 0x6d and buffer[1] == 0x09: 
                    if drone_number == 0x08:
                        new_buffer = buffer[2:13]
                    elif drone_number == 0xe7:
                        new_buffer = buffer[13:]
              	    #print(new_buffer)
                    x = struct.unpack('<h',new_buffer[1:3])[0]
                    y = struct.unpack('<h',new_buffer[3:5])[0]
                    z = struct.unpack('<h',new_buffer[5:7])[0]
                    quaternion = Quaternion(int.from_bytes(new_buffer[7:11], 'little'))
                    self.message_decode=(x,y,z,quaternion)
                elif buffer[0] == 0x8f and buffer[1] == 0x05:
                    self.event.set()
                    print('start Event received')
                    continue
                else :
                    print("Unknown Message received")
                    pass
                if not self.first_message.is_set():
                        self.first_message.set()
                        print('Flag set')
            except:
                print("MemoryError : Decode")        
                self.decode = asyncio.create_task(self.decode_uart())

    def get_position(self) -> tuple:
        return self.message_decode