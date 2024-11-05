import struct
from machine import Timer, UART, Pin
import uasyncio as asyncio
import micropython

tsf = asyncio.ThreadSafeFlag()
buffer= bytearray(16) #TODO change chack tp 32
pin = Pin(29)
uart0 = UART(0, baudrate=115200, tx=Pin(28), rx=Pin(29), bits=8, parity=None, stop=1,rxbuf=1000)
flag_received = False
flag_decoded = False


async def read_uart():
    global buffer
    global flag_received
    global uart0
    await asyncio.sleep(1)
    while True:
        await asyncio.sleep(0)
        if uart0.any():
            uart0.readinto(buffer)
            flag_received = True

async def decode_message():
    global buffer
    global flag_received
    global flag_decoded
    await asyncio.sleep(1)
    while True:
        await asyncio.sleep(0)
        if flag_received:
            if buffer[0] == 1:
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
    global buffer
    task1 = asyncio.create_task(read_uart())
    task2 = asyncio.create_task(decode_message())
    print("main")
    while True:
        await asyncio.sleep(0)
        if flag_decoded:
            print(buffer)
            flag_decoded = False



asyncio.run(main())