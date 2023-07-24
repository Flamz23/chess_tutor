"""

Making sound with PWM

Dependencies:
  pip3 install pigpio rtttl
"""
import pigpio
from time import sleep
from rtttl import parse_rtttl

class Buzzer:

    BUZZER_GPIO = 12  # Hardware PWM Channel GPIO.
    duty_cycle_pc = 50 # >0% to <100%
    duty_cycle = (int)(1000000 * (duty_cycle_pc / 100))


    def __init__(self):
        print("Started rtttl buzzer")

    def PlaySound(self, notes):
        pi = pigpio.pi()

        if notes == "pick":
            rtttl_score = parse_rtttl("pick:d=4,o=5,b=100:16e4,16e5")
        elif notes == "place":
            rtttl_score = parse_rtttl("place:d=4,o=5,b=100:16e5,16e4")
        elif notes == "startup":
            rtttl_score = parse_rtttl("startup:d=4,o=5,b=100:16f4,16f4,16f5,16f4")
        elif notes == "check":
            rtttl_score = parse_rtttl("check:d=4,o=5,b=100:16e5,16e5")
        
        try:   
            for note in rtttl_score['notes']:                                                             # (2)
                frequency = int(note['frequency']) # hardware_PWM() expects an integer parameter.
                duration = note['duration'] # Milliseconds
                pi.hardware_PWM(self.BUZZER_GPIO, frequency, self.duty_cycle)                                       # (3)
                sleep(duration/1000)
        
        except:
            print("sound parse failed")
        
        finally:
            pi.hardware_PWM(self.BUZZER_GPIO, 0, 0) # Buzzer Off
            #self.pi.stop() # PiGPIO Cleanup
        
#BZ = Buzzer()

#BZ.PlaySound("pick")
#sleep(2)
#BZ.PlaySound("place")
#sleep(2)
#BZ.PlaySound("check")
#sleep(2)
#BZ.PlaySound("startup")   
    
