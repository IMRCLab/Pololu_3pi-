from J_maths_module import *
#from J_state_estimate_ticks import *
from J_robot import *
from math import atan2, sqrt, sin, cos, pi
from primitives.queue import Queue
import time
import json
import uasyncio as asyncio
from asyncio import Event
import gc
from uart import Uart
from state_display import StateDisplay



class Control():
    """ 
    """
    def __init__(self,robot:Robot,first_message:Event, start_event:Event, uart_handler:Uart, gains:tuple, logging:bool, car:StateDisplay,logging_interval:float, states:list= [], actions:list =[]) -> None:
        self._robot = robot
        self.start_event = start_event
        self.first_message = first_message
        self._states_mocap = uart_handler
        self._states = states
        self._actions = actions
        self.threshold = 0.05
        self.K_x, self.K_y, self.K_theta = gains 
        self.logging = logging
        self.logging_interval = logging_interval
        self.car = car
        self.path_duration = len(states)/10
        self._run:bool = True
        self.controller = asyncio.create_task(self.control())

    def running(self) -> bool:
        return self._run
    async def control(self)-> None:
        await asyncio.sleep(1)
        await self.first_message.wait()
        self.car.ready()

        await self.start_event.wait()
        
        print('start control')
        self.car.driving()
        self._run = True
        self._start_time = time.time_ns()
        while self._run:
            try:
                await asyncio.sleep(0)
                t = time.time_ns() - self._start_time
                t *= (10**-9)
                print(t)
                remote_action = self._states_mocap.get_remote_control_message()
                print(remote_action)
                velocity = remote_action[0]/65565*self._robot.max_speed
                omega = remote_action[1]
                print(f"Velocity:{velocity}; Omega:{omega}")

                #compute unicycle-model control variables (forwards speed and rotational speed)
                v_ctrl = velocity
                omega_ctrl = omega
                await asyncio.sleep(0)
                
                #transform unicycle-model variables v_ctrl and omega_ctrl to differential-drive
                #model control variables (angular speed of wheels) 
                u_L, u_R = self._robot.trsfm_ctrl_outputs(v_ctrl, omega_ctrl)
                #transform [rad/s] speed to a value the motors can understand (0-6000)
                u_L, u_R = self._robot.angular_speed_to_motor_speed(u_L), self._robot.angular_speed_to_motor_speed(u_R)
                self._robot.motors.set_speeds(u_L, u_R)
                await asyncio.sleep(0.00)
                if t % self.logging_interval  < 0.02 and self.logging:
                   self._robot.state_estimator.past_values.append([t,v_ctrl, omega_ctrl]) 
            except:
                print('invalid message received')
            

from uart import Uart
async def main():
    with open("/config/config.json","r") as f:
        config = json.load(f)
    droneID = int(config['ID'],16)
    logging = int(config['Logging'])
    gains = tuple(config["Gains"])
    logging_interval = float(config['Logging Interval'])
    max_speed_lvl = int(config["Max Speed"])
    logging_time = float(config['Logging Time'])
    print(f"Logging Time {logging_time}")
    rob = Robot(max_speed_lvl=max_speed_lvl)
    car = StateDisplay()
    trajectory_event = Event()
    start_event = Event()
    first_message_event = Event()
    connection = Uart(droneID=droneID,first_message=first_message_event,start_event=start_event, trajectory_event=trajectory_event,baudrate=115200)
    car.waiting_for_trajectory()
    await trajectory_event.wait()   

    control = Control(robot=rob,first_message=first_message_event, start_event=start_event, uart_handler=connection,gains=gains,logging=bool(logging),car=car, logging_interval=logging_interval)
    if logging:
        rob.state_estimator.create_logging_file('remote_control',gains)
    await start_event.wait()
    while True:
        await asyncio.sleep(logging_time)
        if logging:
            if rob.state_estimator.past_values == [] and not control.running():
                logging = False
                car.finish_saving()
            print("Free memory:", gc.mem_free())            
            print(rob.state_estimator.past_values)
            rob.state_estimator.write_past_values()
        print('Collectiong Garbage')
        gc.collect()
        print('allive')
        

        
asyncio.run(main())

