# Python client example to get Lidar data from a drone
#

import airsim

import sys
import math
import time
import argparse
import pprint
import numpy

# Makes the drone fly and get Lidar data
#class FTP:
class BankAngle:
    def __init__(self):

        # connect to the AirSim simulator
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

    def execute(self):
        #always want to do this at start anyway
        print("arming the drone...")
        self.client.armDisarm(True)
        self.client.takeoffAsync().join()
        #Assume drone is already flying
        #Give user authority to initiate FTP
        airsim.wait_key('Press any key to move vehicle to (-10, 10, -10) at 5 m/s')
        #Flies in a box and ends at the vertex the box starts on
        self.client.moveToPositionAsync(-10, 10, -10, 5).join()
        self.client.hoverAsync().join()
        time.sleep(2)
        self.client.moveByRollPitchYawThrottleAsync(0.5, 0, 0, 1, 2, )
    def stop(self):

        airsim.wait_key('Press any key to reset to original state')
        self.client.armDisarm(False)
        self.client.reset()
    

        self.client.enableApiControl(False)
        print("Done!\n")

#main
if __name__ == "__main__":
    BankTest=BankAngle()
    try:
        BankTest.execute()
    finally:
        BankTest.stop()
