"""
Scans the reed switch matrix with the 74HC595 shift register.

Dependencies:
    pip3 install pigpio
    
Built and tested with Python 3.7 on Raspberry pi U Model B
"""

import pigpio
from time import sleep
import numpy as np

class Muxer:
    LATCH_PIN = 0
    CLOCK_PIN = 0
    DATA_PIN = 0
    CLR_PIN = 0

    columnPins = [0, 0, 0, 0, 0, 0, 0, 0]
    muxSequence = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]

    matrix = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ])

    pi = pigpio.pi() # intitialize gpio lib

    def __init__ (self, latch, clk, data, clr, colPins):
        self.LATCH_PIN = latch
        self.CLOCK_PIN = clk
        self.DATA_PIN = data
        self.CLR_PIN = clr
        self.columnPins = colPins

        self.SetupIO() # initialize and set up I/O
        print("I/O setup done!")

    def SetupIO(self):
        for i in range(len(self.columnPins)):
            self.pi.set_mode(self.columnPins[i], pigpio.INPUT) # set pins as input
            self.pi.set_pull_up_down(self.columnPins[i], pigpio.PUD_DOWN) # enable pull up

        self.pi.set_mode(self.LATCH_PIN, pigpio.OUTPUT)
        self.pi.set_mode(self.CLOCK_PIN, pigpio.OUTPUT)
        self.pi.set_mode(self.DATA_PIN, pigpio.OUTPUT)

    def SendData(self, data):
        """
            Sends a 2-byte hex value to the 74hc595 shift register.          
            Args:
                data: A 2-byte hex value to send to the shift register.           
            Returns:
                None
        """

        # Set latch pin low to prepare for data transfer
        self.pi.write(self.LATCH_PIN, 0)

        # Loop through each bit in the data value
        for i in range(7, -1, -1):

            # Shift out the current bit
            bit = (data >> i) & 1
            self.pi.write(self.DATA_PIN, bit)

            # Pulse the clock pin to latch in the bit
            self.pi.write(self.CLOCK_PIN, 1)
            self.pi.write(self.CLOCK_PIN, 0)

        # Set latch pin high to transfer data to the shift register's output pins
        self.pi.write(self.LATCH_PIN, 1)

    def ScanMatrix(self):
        """
            Polls each row and reads a switch close
            Args:
                None
            Returns:
                None
        """
    
        for i in range(8):
            self.SendData(self.muxSequence[i]) # poll board row
     
            for j in range(8):
                pinState = self.pi.read(self.columnPins[j])
                sleep(0.0001)
                pinState = self.pi.read(self.columnPins[j])
                 
                if (pinState == 1):
                    self.matrix[i][j] = 1
                else:
                    self.matrix[i][j] = 0
                sleep(0.005)
                             
            sleep(0.01)

    def GetMatrix(self):
        """
            Prints and returns the virtual matrix
            Args:
                None
            Returns:
                None
        """
               
        self.ScanMatrix() # update 2D matrix array

        print("start:")
        for i in range(8):
            print(f"{self.matrix[i]},") 
        return self.matrix
        
 
    
MX = Muxer(24,25, 23, 1, [17, 27, 22, 5, 6, 13, 19, 26])

while(1):
    MX.GetMatrix()
