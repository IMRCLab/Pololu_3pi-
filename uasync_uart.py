import struct
from machine import Timer, UART, Pin
import uasyncio as asyncio
import micropython, copy

tsf = asyncio.ThreadSafeFlag()
buffer= bytearray(16) #TODO change chack tp 32
pin = Pin(29)
uart0 = UART(0, baudrate=9600, tx=Pin(28), rx=Pin(29), bits=8, parity=None, stop=1,rxbuf=1000)
flag = False


async def read_uart():
    global buffer
    global flag
    while True:
        await asyncio.sleep(0)
        if uart0.any():
            uart0.readinto(buffer)
            flag = True

        pass

async def main():
    global flag
    global buffer
    asyncio.run(read_uart())
    while True:
        await asyncio.sleep(0)
        if flag:
            #TODO deinint irq before reading and reinit after 
            print(buffer)
            value1 = struct.unpack('<f',buffer[-4:])[0]
            value2 = struct.unpack('<f',buffer[-9:-5])[0]
            value3 = struct.unpack('<f',buffer[-13:-9])[0]
            print(f"value3:{value3} : {buffer[-13:-9]}, value2:{value2} ; {buffer[-9:-5]},value1:{value1} : {buffer[-4:]}")
            flag = False



asyncio.run(main())