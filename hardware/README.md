This folder documents the work on the top attachment for the 3pi+.  <br />
This attachment is a platform that serves two purposes : hold the nrf52840 radio dongle in place and hold a vertical stick for Akmaral's motion planning experiments. It is 3d printed in two parts, which are then screwed together on top of the 3pi+.
The two parts are the "base", which has 4 mounting holes for the screws and a slot for the nrf dongle, and the "holder" which has two mounting holes and a tube with 2 other holes to hold the stick in place. (Holder should be mounted on the bottom side of the screen for stability purposes).
&nbsp;
I have used the free softwares Freecad to design the pieces and SuperSlicer to "slice" them in g-code. The parts are designed in .FCstd files. When they're finished, I export them as .stl files to be able to open it in SuperSlicer. With SuperSlicer I create a g-code file which is machine instructions for the 3d printer. Then you simply need to upload the g-code file on the 3d printer and start the print (for more detailed instructions on the last steps, check https://github.com/IMRCLab/3dprinting/blob/main/docs/print.md )<br />

In this folder you will find the .FCstd and .stl files of each part, as well as one g-code file for printing both parts at the same time. If you don't use Freecad, I have also included a .stp version of the parts, which is readable by all CAD software. <br />
&nbsp;
&nbsp;
To mount the whole assembly, you need (in addition to the complete 3pi+) : <br />
- 2x  M2x6+6mm standoffs <br />
- 2x  M2x16mm screws <br />
- 4x  M2x20mm screws <br />
- 4x  M2 nuts <br />
(NB if you don't intend on attaching a stick on top, you can only mount the base for the dongle and not the holder. In this case, you can ignore the M2x20mm screws and use two M2 nuts only, but need 4 M2x16mm screws instead of 2) <br />
(NBB all of these parts are in the "fasteners" box in the flight space, but we are runnning low on appropriate standoffs so we may need to order more) <br />

All holes are for M2 screws, meaning they have a diameter of 2.4mm. The bamboo stick must also be drilled at the same/similar diameter. <br />
&nbsp;

Schematics of the GPIO headers and board dimensions  can be found in the Pololu 3pi+ 2040 user guide (https://www.pololu.com/docs/0J86/all#6.11) in the sections 6.8 and 6.11 respectively. <br />
The 3pi+ has also been modified by adding header pins to the GPIO pins 28 and 29 (for UART communication) as well as 3V3 and GND pins of the right side port (to power the dongle). <br />
&nbsp;
&nbsp;
ABOUT POWERING THE NRF52840 DONGLE : <br />
The dongle is by default powered through its USB port, but can also be powered from an externally regulated source (1.8-3.6 V, 50mA max) through its VDD OUT and GND pins. But to do this you need to physically modify the dongle, and you cannot have both methods allowed at the same time. As documented here (https://infocenter.nordicsemi.com/index.jsp?topic=%2Fug_nrf52840_dongle%2FUG%2Fnrf52840_Dongle%2Fhw_description.html and https://infocenter.nordicsemi.com/index.jsp?topic=%2Fug_nrf52840_dongle%2FUG%2Fnrf52840_Dongle%2Fhw_description.html), you need to solder the SB1 pad and cut the SB2 trace to enable powering from an external source. [ask Max for help if needed]


