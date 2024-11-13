"""
Future Plans
- asyncio to scedule multiple tasks
        I dont now whc tasks yet
- Rap everything in function
    make extra file only to run main 
- single inerrupt buffer might be to slow for 100Hz 
"""



import struct
from machine import Timer, UART, Pin
import uasyncio as asyncio
import micropython
import time
#Buffer for interrupt error messages
micropython.alloc_emergency_exception_buf(100) 


message = {0x8f, 0x08, 0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x01 ,0x00 ,0x00 ,0x40 ,0x40}
message = bytearray(b'\x87\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3f\x00\x00\x40\x40')

buffer= bytearray(16) #TODO change chack tp 32
pin = Pin(29)
uart0 = UART(0, baudrate=9600, tx=Pin(28), rx=Pin(29), bits=8, parity=None, stop=1,rxbuf=1000)
flag=True
"""
Keep the code as short and simple as possible.
Avoid memory allocation: no appending to lists or insertion into dictionaries, no floating point.
"""
def handle_interrupt(pin):
    global flag
    flag = True
    global uart0
    global buffer
    if uart0.any():
        uart0.readinto(buffer)
    global interrupt_pin
    interrupt_pin = pin
    #uart0.flush()

pin.irq(handler=handle_interrupt, trigger=Pin.IRQ_RISING, hard=True)

while True:
    if flag:
        #TODO deinint irq before reading and reinit after 
        print(buffer)
        value1 = struct.unpack('<f',buffer[-4:])[0]
        value2 = struct.unpack('<f',buffer[-9:-5])[0]
        value3 = struct.unpack('<f',buffer[-13:-9])[0]
        print(f"value3:{value3} : {buffer[-13:-9]}, value2:{value2} ; {buffer[-9:-5]},value1:{value1} : {buffer[-4:]}")
        flag = False

