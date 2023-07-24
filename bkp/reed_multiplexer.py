"""
Scans the reed switch matrix with the 74HC595 shift register.

Dependencies:
    pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""

import pigpio
from time import sleep

# input pins
columnPins = [17, 27, 22, 5, 6, 13, 19, 26]
muxSequence = [0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01]

LATCH_PIN = 24
CLOCK_PIN = 25
DATA_PIN = 23
CLEAR_PIN = 1
# virtual python board
#virtualBoard = [
#[R, N, B, K, Q, B, N, R],
#[P, P, P, P, P, P, P, P],
#[-, -, -, -, -, -, -, -],
#[-, -, -, -, -, -, -, -],
#[-, -, -, -, -, -, -, -],
#[-, -, -, -, -, -, -, -],
#[p, p, p, p, p, p, p, p],
#[r, n, b, k, q, b, n, r]
#]

pi = pigpio.pi()


def Setup():
    for i in range(8):
        pi.set_mode(columnPins[i], pigpio.INPUT) # set pins as input
        #pi.set_pull_up_down(columnPins[i], pigpio.PUD_UP) # enable pull up

    pi.set_mode(LATCH_PIN, pigpio.OUTPUT)
    pi.set_mode(CLOCK_PIN, pigpio.OUTPUT)
    pi.set_mode(DATA_PIN, pigpio.OUTPUT)

def SendData(data):
    """
        Sends a 2-byte hex value to the 74hc595 shift register.
    
        Args:
            data: A 2-byte hex value to send to the shift register.
    
        Returns:
            None
    """
    # Set latch pin low to prepare for data transfer
    pi.write(LATCH_PIN, 0)

    # Loop through each bit in the data value
    for i in range(7, -1, -1):

        # Shift out the current bit
        bit = (data >> i) & 1
        pi.write(DATA_PIN, bit)

        # Pulse the clock pin to latch in the bit
        pi.write(CLOCK_PIN, 1)
        pi.write(CLOCK_PIN, 0)

    # Set latch pin high to transfer data to the shift register's output pins
    pi.write(LATCH_PIN, 1)

def ScanMatrix():
    for i in range(8):
        SendData(muxSequence[i]) # poll board row

        for j in range(8):
            pinState = pi.read(columnPins[j])
            sleep(0.02)
            pinState = pi.read(columnPins[j])
            
            if pinState == 0:
                print(f"Row: {i} column {j} state: {pinState}")
            sleep(0.1)
                        
        sleep(0.1)

Setup()
    
while(1):
    ScanMatrix()
 
