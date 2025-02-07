# Pololu 3pi+ RP2040 Robot Development Repository

This repository contains code and resources for the Pololu 3pi+ RP2040 Robot, powered by the Raspberry Pi RP2040 microcontroller. The robot is a versatile platform for experimentation and learning, featuring motor drivers, sensors, and support for various programming configurations.
Repository Structure

- **config/**: Contains configuration files that define various operational parameters for the robot. These configurations influence how different operational modes in the robot's control system behave.
- **trajectories/** : Contains the trajectory files in .json format
- **Dongle Software/**: Contains the build application for the nrf52840 Dongle

- **control.py**: A core script that manages different operational modes for the robot. This script allows the robot to switch between distinct behaviors depending on user input or pre-defined conditions.

## Configuration

### 1. Setup Instructions

- Connect the Pololu 3pi+ RP2040 to your computer.

- But the Robot into bootloader mode restarting it and pressing the b button

- Download the newest version of the Pololu firmware and load it on to the device

  - Further Instructions https://www.pololu.com/docs/0J86/all#5.1

  - Firmware Versions : https://github.com/pololu/micropython-build/releases

- Delete all of the contents from the Micropython folder

- Pull from https://github.com/IMRCLab/Pololu_3pi-.git 0xe7

### 2. Configuration

Modify the configuration files in the config/ folder to customize parameters for different operational modes. Ensure that the JSON syntax is correct to prevent runtime errors.

Customize the following values

- ID
  - The ID of the robot, usually at the bottom of the frame
- trajectory
  - The name of the trajectory file
- Logging
  - *1* for Logging *0* for not Logging

There are more values that can be customized but dont need to be for stable performance. They are the following:

- gains
  - a Tuple with he gains of the robot 
  - [K<sub>X</sub>,K<sub>Y</sub>,K<sub>Theta</sub>]
- Logging Time
  - The difference between saves
- Logging Intervall
  - The Interval between saved States
- Max Speed
  - max RPM

## Running a Trajectory

To run a trajectory one just needs to start the robot and ensure that the launch script is running that is responsible for the communication with the MoCap.
The robots running sequence can be divided into the following segments:

### Start

Is the state right after the start of the robot. In this mode the screen should be black. All of the processes are being initialized. The robot is waiting for position information from the robot.

### Ready

In this mode positional information already has been received, the robot is ready and waiting for the start signal.

Display Output :

```

READY
  ______
 /|_||_\`.__
(   _    _ _\ 
=`-(_)--(_)-'
-- --- --- --- -
READY

```

### Driving

The robot received the start signal and starts driving.

```

DRIVING...
  ______
 /|_||_\`.__
(   _    _ _\ 
=`-(_)--(_)-'
-- --- --- --- -
DRIVING...

```

### Done Driving

The trajectory is completed, the projected time of the trajectory has been reached.

```

----------------
|  ______      |
| /|_||_\`.__  |
|( _ _ _     \ |
|=`-(_)--(_)-' |
----------------
DONE DRIVING
```

### Done Saving

If Logging is enabled, all available data has been saved to the drive

```

----------------
|  ______      |
| /|_||_\`.__  |
|( _ _ _     \ |
|=`-(_)--(_)-' |
----------------
DONE SAVING
```

## Usage of multiple robots

It is recommended to use a 50Hz update rate in the MoCap software, higher frequencies might also work, but have not been tested.

## Development

A common tool for debugging is the [Thonny](https://thonny.org/) ide. It allows for a [simple connection](https://www.pololu.com/docs/0J86/all#5.3) to the MCU on the RP2040 and allows to run programms in the console. For the rest of the development VSC with [MicroPico](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) was used, because of the many usefull tools it has to offer, like code suggestions and git integration.  

## Common Issues

### Pololu Drive in Read Only mode

A quick way to fix this issue is to update the firmware and install the software again.

### Pololu is in Driving Mode but doesnt drive

This usually means that the incoming messages are either decoded incorrectly.

### Pololu stops mid execution with memory issues

The robot stops because it tries to allocate to much data. To solve this issue one can increase Logging Interval or decrease the Logging Time.

## Details

The controller is based on the Collective Intelligence from a Synthetic and Biological Perspective Summer School of which Prof. W. Hönig was one of the organizers. For more information about the differential drive controller
check out the [/collision_avoidance/slides.pdf](http://modelai.gettysburg.edu/2024/collective/slides/slides.zip) of the slides available on the website.

## Radio Receiver

The code for the  nrf Dongle can be found [here](https://github.com/polyblank-5/esb_prx). The compiled file can be found in the Dongle Software folder.

## References 
Collective Intelligence from a Synthetic and Biological Perspective Summer School : http://modelai.gettysburg.edu/2024/collective/

Pololu 3pi+ 2040 User guide : https://www.pololu.com/docs/0J86/all

Dynobench : https://github.com/quimortiz/dynobench/tree/05bafb374e5b00e858d351e2e89d8f4b409f56ab 

<!---
This repository contains code for the 3pi+ 2040 Pololu Ground Robot (written for Hyper edition, but should work for all), as well as some 3d printable files and instructions for attaching and connecting the nrf52840 radio dongle onto it. <br /> 
The code contains a simple state estimator based on odometry readings and a simple differential drive controler. To make gain tuning easier, you can choose a trajectory from a selection of three(straight line, pure rotation, slightly wavy diagonal)
and adjust the gains (Kx, Ky, Ktheta) you want to use directly with the robot buttons. (These two options are enabled by default). The state estimator logs some data of interest and there is also a script which plots this into neatly readable graphs.
This code was written for the IMRC Lab of TU Berlin. It is also based on the Collective Intelligence from a Synthetic and Biological Perspective Summer School of which Prof Hönig (IMRC head) was one of the organizers. For more information about the differential drive controler
check out the /collision_avoidance/slides.pdf of the slides available on the website.

To start using my code, simply paste the files "J_controler.py" "J_state_estimator.py" "J_robot.py" "J_maths_module.py", as well as the trajectories folder and the logs folder in the root directory of your 3pi+ robot, alongside all software pre-installed by Pololu.
(NB in the repo the logs folder contains three examples of data log files and the corresponding pdf containing the plots. These files are not needed for the robot to work, you can delete them. The trajectories folder MUST contain the 3 pre-programmed trajectories though).
When you turn on your 3pi+ robot, simply select the "J_controler.py" program on the display screen and follow the instructions. (I use Kx = 1, Ky = 3, Ktheta = 3 for my gains).

The three pre-programmed trajectories are stored in a .json format. They were generated with an unycicle-model planner Quim Ortiz' Dynobench repo. from  They contain a dictionary with lots of mostly useless info. The only two important items of the this dict are "states" and "actions" (if you want to modify or create your own trajectories, you can get rid of all the other items).
states : list of states the robots has to pass through during the trajectory. Each state is [x position, y position, angle theta]. A 0.1 sec interval is assumed between each state, meaning state 38 corresponds to 3.8 sec after the start of the trajectory.
actions : list of control actions that are needed by the controler

After a trajectory is executed, the data will automatically be saved in a .json file in the logs folder with an appropriate name. (NB sometimes the logfile doesn't show up immediately. Try restarting the robot). 

To plot the data, you can use the script "Plot_Pololu.py". The function plot_all() will automatically create the PDFs of all the logfiles in the logs folder, plotting them in regards to the correct ideal trajectory and naming the resulting PDF following the model of trajectoryname_Kx_Ky_Ktheta.pdf 
If a PDF with this name already exists (because for example there are multiple runs with the same trajectory and gains) it will a B at the end, as many times as needed. 
Just make sure to adjust the path given to plot_all() so that it points to the good directory.

Encountered issues during the project:

If the robot has very weird behavior (sudden acceleration in the wrong direction, not following the desired trajectory at all, moving erratically) one possible issue can be that the motor leads have been soldered the wrong way around. This causes positive speeds given to the motors to turn the motors in the negative direction
(meaning the controler wants the robot to move forward but it's actually driving backward). No panic though, the Pololu engineers thought about the issue : just open the file "Micropython/pololu_3pi_2040_robot/motors.py" and modify the attributes "self._flip_left_motor" and/or "self.flip_right_motor" until it works 
(ie until giving a positive speed to the motors makes the robot go in the direction where his bumpers are, not his USB port).

It happened two times that 3pi+ suddenly locked up its permissions and didn't allow me to modify, delete or add files (no write access). Using chmod command did not work as I got the response "read-only filesystem". The solution I found was updating the MicroPython firmware again (see 3pi+ 2040 user guide ; careful this will delete all custom files on the 3pi+) and then I could do chmod to get write access

References : <br />
-->