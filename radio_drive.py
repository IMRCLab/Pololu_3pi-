import time   #is this precise enough or should I use some time module of the 3pi+ #answer : it wasn't. we need ticks
from math import sin, cos, pi
from J_maths_module import *
from machine import Timer, UART, Pin
import json
from J_state_estimator import State_Estimator
from read_cnrt import Control
from J_robot import Robot
import struct   

from pololu_3pi_2040_robot import robot as three_pi_rob
rob = Robot()
buffer= bytearray(32)
pin = Pin(29)
uart0 = UART(0, baudrate=9600, tx=Pin(28), rx=Pin(29), bits=8, parity=None, stop=1,rxbuf=1000)


"""
+-------+-------+-------+-------+
        | ROLL  | PITCH |  YAW  |THRUST |
        +-------+-------+-------+-------+
Length      4       4       4       2      bytes
"""

def uart0_cb(pin):
    global flag
    flag = True
    global uart0
    global buffer
    if uart0.any():
        uart0.readinto(buffer)
    global interrupt_pin
    interrupt_pin = pin
    #uart0.flush()

pin.irq(handler=uart0_cb, trigger=Pin.IRQ_RISING, hard=True)

cnrtl = Control(tuple((1,3,3)),(time.time_ns() - rob.state_estimator.starttime))
controlling = True
flag = False
while controlling:
    flag = False
    while not flag:
        pass 
    print(buffer)
    yaw = struct.unpack("f",buffer[8:11])
    thrust = int.from_bytes(bytes=buffer[12:13],byteorder="little",signed=False)



