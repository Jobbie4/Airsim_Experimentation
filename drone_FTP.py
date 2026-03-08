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

def __init__(self):

    # connect to the AirSim simulator
    self.client = airsim.MultirotorClient()
    self.client.confirmConnection()
    self.client.enableApiControl(True)

#    def execute(self):
#always want to do this at start anyway
print("arming the drone...")
self.client.armDisarm(True)

#Assume drone is already flying
#Give user authority to initiate FTP
airsim.wait_key('Press any key to move vehicle to (-10, 10, -10) at 5 m/s')
#Flies in a box and ends at the vertex the box starts on
self.client.moveToPositionAsync(-10, 10, -10, 5).join()
self.client.hoverAsync().join()
self.client.moveToPositionAsync(10, 10, -10, 5).join()
self.client.hoverAsync().join()
self.client.moveToPositionAsync(10, -10, -10, 5).join()
self.client.hoverAsync().join()
self.client.moveToPositionAsync(-10, -10, -10, 5).join()
self.client.hoverAsync().join()
self.client.moveToPositionAsync(-10, 10, -10, 5).join()
        
    #retained, useful function
    #def stop(self):

     #   airsim.wait_key('Press any key to reset to original state')

     #  self.client.armDisarm(False)
     #   self.client.reset()

     #   self.client.enableApiControl(False)
     #   print("Done!\n")
# main
#if __name__ == "__main__":
#    args = sys.argv
#    args.pop(0)


#    arg_parser = argparse.ArgumentParser("FTP.py makes drone fly a prescribed path")
#    args = arg_parser.parse_args(args)    
#    ftp= FTP()
#    try:
#        ftp.execute()
#    finally:
#        ftp.stop()
