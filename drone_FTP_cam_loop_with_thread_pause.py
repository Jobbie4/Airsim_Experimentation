#pip loaded calls (will be listed in env.yml)
import airsim
import math
import os
import pprint
import sys
import time
import tempfile
import argparse
import threading

#locally defined packages
import utils 
from utils import RepeatThread
import setup_path 

# Makes the drone fly and get Lidar data
class Drone_FTP_Cam_loop:

    def __init__(self):

        # connect to the AirSim simulator
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.data_dir= "C:/Users/ericu/Documents/GitHub/Airsim_Build/data"
        
    def execute(self):
        #Start thread processes that use a separate airsim client at the beginning of the run to avoid resets
        CameraLoop=RepeatThread.Thread(self.data_dir) 

        #Arm Drone and Takeoff
        print("arming the drone...")
        self.client.armDisarm(True)
        airsim.wait_key('Press any key to takeoff')
        self.client.takeoffAsync().join()

        #Begin Camera Loop using Thread Class
        #I want the timing on this to be configurable by input file
        #verify pausing stops camera loop ...it doesn't.
        
        airsim.wait_key('Press any key to take images')
        CameraLoop.start_image_callback_thread()
        #Create pause events for simPause
       
        #Ascend 
        #Pauses inserted to ensure proper sim operation

        #CameraLoop.stop_image_callback_thread() #Replace with pause function once you've developed it
        

        airsim.wait_key('Press any key to move vehicle Up to  (0, 0, 31.5m) at 5 m/s')
        CameraLoop.pause_image_callback_thread()
        self.client.simPause(True)
        time.sleep(2) #paused
        CameraLoop.unpause_image_callback_thread()
        self.client.simPause(False) 
        #CameraLoop.start_image_callback_thread() #Replace with pause function once you've developed it
        self.client.moveToPositionAsync(8.35, 0, -10, 5)

       
        #Execute Racetrack
        #CameraLoop.stop_image_callback_thread() #Replace with pause function once you've developed it
       
        airsim.wait_key('Press any key Begin prescribed Racetrack pattern at 5 m/s')
        CameraLoop.pause_image_callback_thread()
        self.client.simPause(True)
        time.sleep(2) #paused
        CameraLoop.unpause_image_callback_thread()
        self.client.simPause(False) 
        #CameraLoop.start_image_callback_thread() #Replace with pause function once you've developed it

        self.client.moveToPositionAsync(-43.70, -47.20, -31.50, 10).join()
        self.client.hoverAsync() 
        self.client.moveToPositionAsync(48.30, -47.20, -31.50, 10).join()
        self.client.hoverAsync().join()
        self.client.moveToPositionAsync(48.30, 40.50, -31.50, 10).join()
        self.client.hoverAsync().join()
        self.client.moveToPositionAsync(-43.70, 40.50, -31.50, 10).join()
        self.client.hoverAsync().join()
        self.client.moveToPositionAsync(-43.70, -47.20, -31.50, 10).join()

        #stop Camera Loop
        CameraLoop.stop_image_callback_thread()
          
    def stop(self):

        airsim.wait_key('Press any key to reset to original state')

        self.client.armDisarm(False)
        self.client.reset()

        self.client.enableApiControl(False)
        print("Done!\n")


# main
if __name__ == "__main__":
    args = sys.argv
    args.pop(0)

    arg_parser = argparse.ArgumentParser("drone_FTP_cam_loop.py makes drone fly a prescribed path and take pictures on a loop")

    arg_parser.add_argument('-save-to-disk', type=bool, help="Not used", default=False)
  
    args = arg_parser.parse_args(args)    
    FTP_Cam_loop = Drone_FTP_Cam_loop()

    #Is this a form of error handling?  it looks like it
    try:
        FTP_Cam_loop.execute()
    finally:
        FTP_Cam_loop.stop()
