import pigpio
import multiplexer
import buzzer
from time import sleep
import numpy as np


class ChessTutor:
    # Switches
    ON_OFF_PIN = 13
    USER_PIN = 19

    # LED Strip
    LED_DATA_PIN = 0

    defaultBoardState = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1]
    ])
    previousBoardState = np.zeros((8, 8)) # store previous state
    p1turn = 0
    p2turn = 0
    checkMate = 0

    pi = pigpio.pi() # initialize gpio lib
    MX = multiplexer.Muxer(24, 25, 23, 1, [17, 27, 22, 5, 6, 13, 19, 26]) # Initialize muxer
    BZ = buzzer.Buzzer() # initialize buzzer
    

    def __init__ (self):
        """
        """
        self.SetupIO() #initialize and set up I/O
        self.BZ.PlaySound("startup")
        self.PickandPlace() # start pick and place mode
        

    def SetupIO(self):
        """
        """
        self.pi.set_mode(self.ON_OFF_PIN, pigpio.INPUT) # set pin as output and pull down
        self.pi.set_pull_up_down(self.ON_OFF_PIN, pigpio.PUD_DOWN)
        
        self.pi.set_mode(self.USER_PIN, pigpio.INPUT)
        self.pi.set_pull_up_down(self.USER_PIN, pigpio.PUD_DOWN)

    def PickandPlace(self):
        """
        """
        ###### LED Sequence light up sequence and delay
 
        currentBoardState = self.MX.GetMatrix()  # get current board state
        
        while not np.array_equal(currentBoardState, self.defaultBoardState):
            # Loop over every position (i, j) in an 8x8 matrix
            for i in range(8):
                for j in range(8):
                    # Check if the LED square is in the default state
                    if currentBoardState[i][j] == self.defaultBoardState[i][j]:
                        print("na")
                    else:
                        # Highlight the LED square
                        print("highlighted")
        
            # Get the updated board state
            currentBoardState = self.MX.GetMatrix()

        print("board setup complete!")
        self.BZ.PlaySound("startup")
        ###### LED Sequence and delay

        # wait for user pin to toggle (must always be toggled)
        currentUserPinState = self.pi.read(self.USER_PIN)
        while (currentUserPinState == self.pi.read(self.USER_PIN)):
            currentUserPinState = self.pi.read(self.USER_PIN)

        # LED Sequence and delay

    def Game(self):
        """
        """

        while not (checkMate):
            p1turn = 1
            self.P1move()
            

    def P1move(self):
        currentBoardState = self.MX.GetMatrix();

    #def P2move():    

    def CompareBoardStates(self, arr1, arr2):
        """
        """
        # find the indices where the two arrays differ
        index = np.where(arr1 != arr2)
        return index
        
CT = ChessTutor()
