from math import atan2, sqrt, sin, cos
from J_maths_module import *
from J_robot import Robot

class Control():
    def __init__(self, gains, t_start_traj) -> None:
        self.K_x, self.K_y, self.K_theta = gains
        self.t_start_traj = t_start_traj
        

    def control_from_json(self, rob:Robot, states, actions) -> bool :
        state, t_ns = rob.state_estimator.state_estimate()
        t = t_ns - self.t_start_traj #time.ticks_diff(t_us, t_start_traj)
        t *= (10**-9) #convert to seconds
        x,y,theta = state
        #define gains
        
        
        #get the index corresponding to the time we are at
        #for actions we round down, for states we round up (=round down + 1)
        #we round to the nearest decimal since the timestep is 0.1s
        index_action = int(round_down(t,1) * 10)
        index_state = index_action + 1
        print(t)
        print(f"action i {index_action} ; state i {index_state}")
        
        #get desired state and velocities
        if index_action >= len(actions):
            print("no more action left : goal should be reached")
            rob.motors.off()
            return False
        
        #get desired state and velocities
        x_d, y_d, theta_d = states[index_state]
        v_d, omega_d = actions[index_action]

        
        #compute error
        x_e = (x_d-x)*cos(theta) + (y_d - y)*sin(theta)
        y_e = -(x_d - x)*sin(theta) + (y_d - y)*cos(theta)
        theta_e = theta_d - theta
        
        
        #compute unicycle-model control variables (forwards speed and rotational speed)
        v_ctrl = v_d*cos(theta_e) + self.K_x * x_e
        omega_ctrl = omega_d + v_d*(self.K_y*y_e + self.K_theta*sin(theta_e)) + self.K_theta*theta_e
        
        #for logging
        rob.state_estimator.last_v_ctrl = v_ctrl
        rob.state_estimator.last_omega_ctrl = omega_ctrl
        
        #transform unicycle-model variables v_ctrl and omega_ctrl to differential-drive
        #model control variables (angular speed of wheels) 
        u_L, u_R = rob.trsfm_ctrl_outputs(v_ctrl, omega_ctrl)
        #transform [rad/s] speed to a value the motors can understand (0-6000)
        u_L, u_R = rob.angular_speed_to_motor_speed(u_L), rob.angular_speed_to_motor_speed(u_R)
        rob.motors.set_speeds(u_L, u_R)
        return True

    def control_from_uart(self, rob:Robot, state_desired, actions) -> bool:
        """
        where does the states come from ?
        DO I have to calculate the real ones or do they come from the camera 
        Do I only get actions for the movent or also desired states 
            Does this work with the Communication Protocoll ?
        When do I stop
        
        """


        state, t_ns = rob.state_estimator.state_estimate()
        x,y,theta = state
        #get desired state and velocities
        x_d, y_d, theta_d = state_desired
        v_d, omega_d = actions
        
        #compute error
        x_e = (x_d-x)*cos(theta) + (y_d - y)*sin(theta)
        y_e = -(x_d - x)*sin(theta) + (y_d - y)*cos(theta)
        theta_e = theta_d - theta
        
        
        #compute unicycle-model control variables (forwards speed and rotational speed)
        v_ctrl = v_d*cos(theta_e) + self.K_x * x_e
        omega_ctrl = omega_d + v_d*(self.K_y*y_e + self.K_theta*sin(theta_e)) + self.K_theta*theta_e
        
        #for logging
        rob.state_estimator.last_v_ctrl = v_ctrl
        rob.state_estimator.last_omega_ctrl = omega_ctrl
        
        #transform unicycle-model variables v_ctrl and omega_ctrl to differential-drive
        #model control variables (angular speed of wheels) 
        u_L, u_R = rob.trsfm_ctrl_outputs(v_ctrl, omega_ctrl)
        #transform [rad/s] speed to a value the motors can understand (0-6000)
        u_L, u_R = rob.angular_speed_to_motor_speed(u_L), rob.angular_speed_to_motor_speed(u_R)
        rob.motors.set_speeds(u_L, u_R)
        return True