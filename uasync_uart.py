import struct
from machine import Timer, UART, Pin
import uasyncio as asyncio
import micropython
from quaternion import Quaternion
from uart import Uart

tsf = asyncio.ThreadSafeFlag()
buffer= bytearray(16) #TODO change chack tp 32
buffer_list = list()
pin = Pin(29)
uart0 = UART(0, baudrate=115200, tx=Pin(28), rx=Pin(29), bits=8, parity=None, stop=1,rxbuf=1000)
flag_received = False
flag_decoded = False


async def read_uart():
    global buffer_list
    global flag_received
    global uart0
    await asyncio.sleep(1)
    while True:
        await asyncio.sleep(0)
        if uart0.any():
            new_buffer = bytearray(32)
            uart0.readinto(new_buffer)
            buffer_list.append(new_buffer)
            #flag_received = True

async def decode_message():
    global buffer
    global flag_received
    global flag_decoded
    await asyncio.sleep(1)
    while True:
        await asyncio.sleep(0)
        if flag_received: #TODO Add cases for diffrent Messages 
            if buffer[0] == 0x6d and buffer[1] == 0x09:
                print("1")
                pass
            elif buffer[0] == 2:
                print("2")
                pass
            else :
                print("else")
                pass

            flag_received = False
            flag_decoded = True

async def main():
    print("start")
    global flag_received
    global flag_decoded
    global buffer_list
    task1 = asyncio.create_task(read_uart())
    #task2 = asyncio.create_task(decode_message())
    print("main")
    while True:
        await asyncio.sleep(0)
        try:
            print(buffer_list.pop(0))
        except:
            pass
        """if flag_decoded:
            print(buffer)
            flag_decoded = False"""



asyncio.run(main())