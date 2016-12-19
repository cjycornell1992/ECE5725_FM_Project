
ECE 5725 Final Project, RPi FM Radio Group 
==========================================================================

This is the code repository for ECE 5725 Final Project. RPi Fm Radio Group
We will use this repository to collaborate with group member. We are using
Raspberry Pi For our project.

### Usage

Note we use linux FIFO objects to communicate, so for the first time only,
FIFO object needs to be created before executing our main scripts. Under App
directory, run

* mkfifo main2Trans_fifo
* mkfifo Trans2main_fifo

Then go to the App directory, run:

* sudo python Transmission.py &
* sudo python main.py

### Progess

Progess: This repository has released the first version. Also, this repository is under maintanance.

Revision History: 

12/06/2016. Transmitter and app all have been released.
The transmitter is a software transmitter running at 99.9 MHz. The app is a
PiTFT based touchscreen GUI control panel on top of transmitter and receiver.

11/22/2016. SI4703 Controller minor fixes.
pygame based GUI is now released. Example script test.py is attached in
GUI directory.

11/17/2016. SI4703 Controller is now working in USA.
Example script test.py is attached in Si4703 directory.

                  
### Group Members

 * Junyin Chen    (jc2954)
 * Zhenchuan Pang (zp55)
 * Xiaokun Yu     (xy284)
