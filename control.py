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
    def __init__(self,robot:Robot,first_message:Event, event:Event, uart_handler:Uart, states:list, actions:list, gains:tuple, logging:bool, car:StateDisplay,logging_interval:float) -> None:
        self._robot = robot
        self.event = event
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

        await self.event.wait()
        
        print('start control')
        self.car.driving()
        self._run = True
        index = 0
        self._start_time = time.time_ns()
        while self._run:
            try:
                await asyncio.sleep(0)
                t = time.time_ns() - self._start_time
                t *= (10**-9)
                print(t)
                index =  round(len(self._actions) * t / self.path_duration)
                state = self._states_mocap.get_position()
                print(state)
                x,y,_,_ = state 
                x = x/1000
                y = y/1000
                theta = state[3].yaw
                print("x "+str(x))
                print("y "+str(y))
                print("theta "+str(theta))
                print(t)
                print(f"action i:{index} ; state i:{index}")
                #get desired state and velocities
                if index >= len(self._actions)-1:
                    print("no more action left : goal should be reached")
                    self._robot.motors.off()
                    self._run = False
                    self.car.finish_driving()
                    break
                
                await asyncio.sleep(0.0)
                #get desired state and velocities
                x_d, y_d, theta_d = self._states[index+1]
                print(f'x_d:{x_d}; y_d:{y_d}; theta_d:{theta_d}')

                #print(index)
                v_d, omega_d = self._actions[index]

                #compute error
                x_e = (x_d-x)*cos(theta) + (y_d - y)*sin(theta)
                y_e = -(x_d - x)*sin(theta) + (y_d - y)*cos(theta)
                
                theta_e_org = theta_d - theta
                theta_e = atan2(sin(theta_d-theta), cos(theta_d-theta))
                print(f'Theta Error Original:{theta_e_org}, Theta_e_new:{theta_e}')
                
                #compute unicycle-model control variables (forwards speed and rotational speed)
                v_ctrl = v_d*cos(theta_e) + self.K_x * x_e
                omega_ctrl = omega_d + v_d*(self.K_y*y_e + self.K_theta*sin(theta_e)) + self.K_theta*theta_e
                await asyncio.sleep(0)

                
                #transform unicycle-model variables v_ctrl and omega_ctrl to differential-drive
                #model control variables (angular speed of wheels) 
                u_L, u_R = self._robot.trsfm_ctrl_outputs(v_ctrl, omega_ctrl)
                #transform [rad/s] speed to a value the motors can understand (0-6000)
                u_L, u_R = self._robot.angular_speed_to_motor_speed(u_L), self._robot.angular_speed_to_motor_speed(u_R)
                self._robot.motors.set_speeds(u_L, u_R)
                await asyncio.sleep(0.00)
                if t % self.logging_interval  < 0.02 and self.logging:
                    self._robot.state_estimator.past_values.append([t,x, y, theta,v_ctrl, omega_ctrl, index]) 
            except:
                print('invalid message received')
            

from uart import Uart
async def main():
    with open("/config/config.json","r") as f:
        config = json.load(f)
    trajectory = config["trajectory"]
    droneID = int(config['ID'],16)
    logging = int(config['Logging'])
    gains = tuple(config["Gains"])
    logging_interval = float(config['Logging Interval'])
    max_speed_lvl = int(config["Max Speed"])
    
    rob = Robot(max_speed_lvl=max_speed_lvl)
    car = StateDisplay()
    with open("/trajectories/" + trajectory,"r") as f:
        data = json.load(f)
    try:
        states = data["result"]['states']
        ctrl_actions = data["result"]["actions"]
    except:
        states = data["result"][0]['states']
        ctrl_actions = data["result"][0]["actions"]
    start_event = Event()
    first_message_event = Event()
    connection = Uart(droneID=droneID,first_message=first_message_event,event=start_event,baudrate=115200)
    control = Control(robot=rob,first_message=first_message_event, event=start_event, uart_handler=connection,states=states,actions=ctrl_actions,gains=gains,logging=bool(logging),car=car, logging_interval=logging_interval)
    if logging:
        rob.state_estimator.create_logging_file(trajectory,gains)
    await start_event.wait()
    while True:
        await asyncio.sleep(10)
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

