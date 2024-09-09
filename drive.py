import time   #is this precise enough or should I use some time module of the 3pi+ #answer : it wasn't. we need ticks
from math import sin, cos, pi
from J_maths_module import *
from machine import Timer, UART, Pin
import json
from J_state_estimator import State_Estimator
from read_cnrt import control_from_json
from J_robot import Robot

from pololu_3pi_2040_robot import robot as three_pi_rob
rob = Robot()
buffer= bytearray(1)
pin = Pin(29)
uart0 = UART(0, baudrate=9600, tx=Pin(28), rx=Pin(29), bits=8, parity=None, stop=1,rxbuf=1000)


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


traj_list = ["line","rotation","curve"]
flag = False
while not flag:
    pass

traj = "/trajectories/" + traj_list[buffer[0]] + ".json"
print(traj)

with open(traj) as f:
    data = json.load(f)
states = data["result"][0]['states']
ctrl_actions = data["result"][0]["actions"]
print(len(states), " ", states)
print(len(ctrl_actions), " ", ctrl_actions)
time.sleep(0.5)

gains = tuple((1,3,3))
print(gains)
time.sleep(1)
rob.state_estimator.start(True)
print("starting controler")
counter = 0
controlling=True
#time where the trajectory starts, with t=0.0 being the moment where the robot is initialized
#this isn't great coding I should change it later
t_start_traj = time.time_ns() - rob.state_estimator.starttime
print("start " + str(t_start_traj))
rob.state_estimator.display_state()
while controlling :
    controlling = control_from_json(rob, states, ctrl_actions, gains, t_start_traj)
    counter += 1
    if counter % 25 == 0:
        rob.state_estimator.display_state()
    time.sleep(0.005)
rob.motors.off()
rob.state_estimator.display_state()
rob.state_estimator.start(False)
rob.state_estimator.write_states_to_json(gains=gains, traj=traj)
print("finished")
