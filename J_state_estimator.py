import time   #is this precise enough or should I use some time module of the 3pi+ #answer : it wasn't. we need ticks
from math import sin, cos, pi
from J_maths_module import *
from machine import Timer
import random

class State_Estimator():
    def __init__(self, robot): 
        self.state = [0,0,0]   # [x, y, theta(radians)]
        self.theta_easy = 0 #theta for dummies : in degrees, from -180 to +180
        self.starttime = 0 # Not cool because you cant subtract  variables of type None
        self.last_estimation = 0 #time of the last state estimation (in regards to starttime)
        self.last_oR = robot.encoders.get_counts()[0] #last value given by the right quadrature encoder (odometry sensor)
        self.last_oL = robot.encoders.get_counts()[1] #last value given by the left quadrature encoder (odometry sensor)
        self.timer = Timer(-1)
        #self.timer.init(mode=Timer.PERIODIC, period=1, callback=self.state_estimate)
        
        #initialize the state estimator for this specific instance of robot
        self.robot = robot  #so that State_Estimator has access to some necessary attributes and methods of the Robot class
        self.L = self.robot.L
        self.r = self.robot.r

        #for logging
        """
        self.past_states = [] #list of past states of robot, along with time [x,y,theta,t]
        self.past_estimations = [] #list of values calculated in past state_estimate calls [uL,uR,t]
        self.past_ctrl_actions= []
        self.desired_values = []
        """
        self.last_v_ctrl = 0
        self.last_omega_ctrl = 0
        self.past_values = []
        ###for testing
        self.estimation_counter = 0
        self.logfile = self.create_filename('logging')

    def create_logging_file(self,traj:str,gains:tuple)-> None:
        self.logfile = str(self.logfile[:6] + traj[:3] + '_' + self.logfile[6:])
        header = ["T","X", 'Y', "Theta","V_ctrl", "Omega_ctrl", "Index"]
        line = ','.join(map(str, gains))  # Convert tuple to CSV line
        with open(self.logfile, 'w') as file:
            file.write("Trajectory File" + '\n')
            file.write(traj + '\n')
            # Write the headers
            file.write('gains' + '\n')
            file.write(line + '\n')  # Write the line with a newline
            file.write(str(header)+ '\n')
        

    def create_filename(self, file_type:str) -> str:
        localtime = time.localtime()
        h,m,s = localtime[3],localtime[4],localtime[5]
        run_name = f"{file_type}_{h}_{m}_{s}_{random.randint(0,1000)}"
        #logfile = "/recordings/" + run_name
        return "/logs/" + run_name + '.txt'
    
        #prints information about the state on the display of the robot    
    def display_state(self):
        x,y,rad = self.state
        theta = self.theta_easy
        t = self.last_estimation - self.starttime
        to_display = [f"x: {x}", f"y: {y}", f"deg: {theta}", f"rad: {rad} ",f"t {t / (10**9)}"]
        #print(to_display)
        self.robot.displaylist(to_display)  

    #writes the recorded states and control actions, as well as the used trajectory & gains in a file of the log folder
    #the file's name reflects the trajectory and the time where it was executed
    def write_past_values(self):
        with open(self.logfile, 'a') as file:
            file.write(str(self.past_values))
            
            #for row in self.past_values:
            #    file.write(','.join(map(str, row)) + '\n')

        self.past_values = list()

    """
    def update_logfile_traj(self, traj:str) -> None:
        self.logfile_actions = str(self.logfile_actions[:6] + traj + '_' + self.logfile_actions[6:])
        self.logfile_states = str(self.logfile_states[:6] + traj + '_' + self.logfile_states[6:])
        self.logfile_desired = str(self.logfile_desired[:6] + traj + '_' + self.logfile_desired[6:])
    """
    """
    def save_gains(self,gains:tuple) -> None:
        with open(self.logfile, 'a') as file:
            # Write the headers
            line = ','.join(map(str, gains))  # Convert tuple to CSV line
            file.write('gains' + '\n')
            file.write(line + '\n')  # Write the line with a newline
    """
    
    """
    def create_csv(self) -> None:
        header_actions = ['v_ctrl','omega_ctrl']
        print(self.logfile_actions)
        with open(self.logfile_actions, 'w+') as file:
            # Write the headers
            file.write(','.join(header_actions) + '\n')
        header_states = ['x','y','theta','t']
        print(self.logfile_states)
        with open(self.logfile_states, 'w+') as file:
            # Write the headers
            file.write(','.join(header_states) + '\n')
        header_desired = ["x_d",'y_d','theta_d', "v_ctrl_d",'omega_ctrl_d','t']
        print(self.logfile_desired)
        with open(self.logfile_desired, 'w+') as file:
            # Write the headers
            file.write(','.join(header_desired) + '\n')
    """



        

    """
    #according to the Timer API, the callback function MUST take an argument for the timer
    #even if it is not used
    def state_estimate(self, timerobject=None):
        
        currtime = time.time_ns()
        
        #if first call of state estimation, return [0,0,0]
        if self.starttime == 0:
            self.starttime = currtime
            self.last_estimation = 0
            self.state = [0.,0.,0.]
            return (self.state, self.last_estimation)
            
        t = currtime - self.starttime
        oL, oR = self.robot.encoders.get_counts() #get reading from odometry (183 increments per revolution)
        #normalize to radian and change the sign because encoders count negative when 3pi+ goes forward
        oL, oR= -oL*2*pi/183, -oR*2*pi/183  

        dt = t - self.last_estimation
        deltaL = oL - self.last_oL
        deltaR = oR - self.last_oR
        
 
        uL = deltaL / dt
        uR = deltaR / dt
        x,y,theta = self.state[0], self.state[1], self.state[2]
        x_dot = self.r/2 * (uL + uR) * cos(theta)
        y_dot = self.r/2 * (uL + uR) * sin(theta)
        theta_dot = self.r / self.L * (uR - uL)
        x_new = x + x_dot*dt 
        y_new = y + y_dot*dt
        theta_new = theta + theta_dot * dt

        #update state and other relevant variables
        self.state = [x_new, y_new, theta_new]
        self.last_estimation = currtime  
        self.last_oL = oL
        self.last_oR = oR
        #transform theta in degrees
        theta_deg = (self.state[2]*180/pi)
        #normalize to always indicate from +180 to -180 degrees
        self.theta_easy = (theta_deg + 180) % 360 - 180 

        #every 100 calls of the state_estimator, we save the current state. NB you can choose any number other than 100
        self.estimation_counter += 1
        if self.estimation_counter % 100 == 0:
            #print("logging")
            self.past_states.append([x_new, y_new, theta_new, t])
            self.past_ctrl_actions.append([self.last_v_ctrl, self.last_omega_ctrl])
         
        return (self.state, t)
    """



    
    """
    def start(self, turn_on):
        if turn_on == True :
            self.starttime = time.time_ns()
            self.timer.init(mode=Timer.PERIODIC, period=1, callback=self.state_estimate)
        if turn_on == False:
            self.timer.deinit()
    """

    
#a few lines to test the basic functionality of odometry state estimation   
#NB "if name == main" will only run if you run it from a terminal. Selecting the program from the screen of the 3pi+ will NOT run this code. If you want to run it from the control screen of the 3pi+,
#comment out if name==main and unindent to run it as a script. But be careful because this will then also run every time this file is imported. So keep the if clause there unless testing smth specific
#if __name__ == "__main__":

