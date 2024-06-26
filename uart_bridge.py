from machine import UART


class Uart_Bridge():
    def __init__(self): 
        self.baudrate = 9800
        self.bites = 8 
        self.parity = None
        self.stop = 1

