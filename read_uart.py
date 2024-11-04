import struct
from machine import Timer, UART, Pin


message = {0x8f, 0x08, 0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x01 ,0x00 ,0x00 ,0x40 ,0x40}
message = bytearray(b'\x87\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x3f\x00\x00\x40\x40')

buffer= bytearray(16)
pin = Pin(29)
uart0 = UART(0, baudrate=9600, tx=Pin(28), rx=Pin(29), bits=8, parity=None, stop=1,rxbuf=1000)
flag=False

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
        print(buffer)
        value1 = struct.unpack('<f',buffer[-4:])[0]
        value2 = struct.unpack('<f',buffer[-8:-4])[0]
        value3 = struct.unpack('<f',buffer[-12:-8])[0]
        print(f"value3:{value3}, value2:{value2},value1:{value1}")
        flag = False
