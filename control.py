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



class Control():
    def __init__(self,robot:Robot,first_message:Event, event:Event, start_time:int, uart_handler:Uart, states:list, actions:list, gains:tuple) -> None:
        self._robot = robot
        self.event = event
        self.first_message = first_message
        self._start_time = start_time
        self._states_mocap = uart_handler
        self._states = states
        self._actions = actions
        self.threshold = 0.05
        self.K_x, self.K_y, self.K_theta = gains 
        self.controller = asyncio.create_task(self.control())

    async def control(self)-> None:
        await asyncio.sleep(1)
        await self.event.wait()
        await self.first_message.wait()
        print('start control')
        run = True
        index = 0
        finish_time = 5
        self._start_time = time.time_ns()
        while run: #TODO What happens if trajectory is done -> just stops right now 
            try:
                await asyncio.sleep(0)
                t = time.time_ns() - self._start_time
                t *= (10**-9)
                print(t)
                index =  round(len(self._actions) * t / finish_time)
                state = self._states_mocap.get_position()
                print(state)
                x,y,_,_ = state # TODO Add transformation for positions so real is accounted for not postion of marker deck 
                x = x/1000
                y = y/1000
                theta = state[3].yaw
                if theta < 0: # might have to change when position of tracker deck moves
                    theta += math.pi
                else:
                    theta -= math.pi
                print("x "+str(x))
                print("y "+str(y))
                print("theta "+str(theta))
                print(t)
                print(f"action i:{index} ; state i:{index}")
                # TODO take states and actions according to time 
                #get desired state and velocities
                if index >= len(self._actions)-1:
                    print("no more action left : goal should be reached")
                    self._robot.motors.off()
                    run = False
                    #self._robot.state_estimator.write_states_to_csv(gains=(self.K_x,self.K_y,self.K_theta), traj="/trajectories/unicycle_flatness.json")
                    break
                
                await asyncio.sleep(0.0)
                #get desired state and velocities
                x_d, y_d, theta_d = self._states[index+1]
                #print(f'x_d:{x_d}; y_d:{y_d}; theta_d:{theta_d}') # todo FINISHING CONDITION
                #y_d = 0
                #x_d = 0
                #theta_d = math.pi/2
                #if abs(x_d -x) < self.threshold and abs(y_d -y) < self.threshold and abs(theta_d-theta) < self.threshold:
                #index +=1
                print(index)
                v_d, omega_d = self._actions[index]

                #compute error
                x_e = (x_d-x)*cos(theta) + (y_d - y)*sin(theta)
                y_e = -(x_d - x)*sin(theta) + (y_d - y)*cos(theta)
                
                theta_e_org = theta_d - theta
                theta_e = atan2(sin(theta_d-theta), cos(theta_d-theta))
                print(f'Theta Error Original:{theta_e_org}, Theta_e_new:{theta_e}')
                print(f"Control Error: x:{x_e}, y:{y_e}, theta:{theta_e}")
                
                #compute unicycle-model control variables (forwards speed and rotational speed)
                v_ctrl = v_d*cos(theta_e) + self.K_x * x_e
                omega_ctrl = omega_d + v_d*(self.K_y*y_e + self.K_theta*sin(theta_e)) + self.K_theta*theta_e
                print(f"Control Actions: omega:{omega_ctrl}, v:{v_ctrl}")
                await asyncio.sleep(0)
                #for logging
                self._robot.state_estimator.last_v_ctrl = v_ctrl
                self._robot.state_estimator.last_omega_ctrl = omega_ctrl

                
                
                #transform unicycle-model variables v_ctrl and omega_ctrl to differential-drive
                #model control variables (angular speed of wheels) 
                u_L, u_R = self._robot.trsfm_ctrl_outputs(v_ctrl, omega_ctrl)
                #transform [rad/s] speed to a value the motors can understand (0-6000)
                u_L, u_R = self._robot.angular_speed_to_motor_speed(u_L), self._robot.angular_speed_to_motor_speed(u_R)
                #print(f"Motor Speed u_L:{u_L}, u_R:{u_R}")
                self._robot.motors.set_speeds(u_L, u_R)
                #print(f'Free Memory {gc.mem_free()}')
                await asyncio.sleep(0.00)
            except:
                print('invalid message received')
            if t % 0.2  < 0.2:
                pass
                #self._robot.state_estimator.past_states.append([x, y, theta, t])
                #self._robot.state_estimator.past_ctrl_actions.append([v_ctrl, omega_ctrl])  
                #self._robot.state_estimator.desired_values.append([self._states[index+1][0],self._states[index+1][1],self._states[index+1][2],self._actions[index][0],self._actions[index][1], t ]) #[x,y,theta,v_ctrl,omega_ctrl]
 

from uart import Uart
async def main():
    rob = Robot()
    with open("/config/config.json","r") as f:
        config = json.load(f)
    trajectory = config["trajectory"]
    with open("/trajectories/" + trajectory,"r") as f:
        data = json.load(f)
    states = data["result"]['states']
    ctrl_actions = data["result"]["actions"]
    gains = tuple((6.5,9.5,6.0))
    start_event = Event()
    first_message_event = Event()
    connection = Uart(first_message=first_message_event,event=start_event,baudrate=115200)
    control = Control(robot=rob,first_message=first_message_event, event=start_event, start_time=time.time_ns(),uart_handler=connection,states=states,actions=ctrl_actions,gains=gains)
    rob.state_estimator.update_logfile_traj(trajectory[:3])
    rob.state_estimator.create_csv()
    rob.state_estimator.save_gains(gains)
    while True:
        await asyncio.sleep(5)
        #print(rob.state_estimator.past_states)
        #print(rob.state_estimator.past_ctrl_actions)
        #rob.state_estimator.write_states_to_csv(gains=gains, traj="/trajectories/unicycle_flatness.json")
        #print('Collectiong Garbage')
        #gc.collect()
        print('allive')
        

        
asyncio.run(main())

