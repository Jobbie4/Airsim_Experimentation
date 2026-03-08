
#Create pause events for simPause


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
from utils import RepeatThread_with_pause
import setup_path 


class ThreadPauseTest:
    def __init__(self):
        # connect to the AirSim simulator
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)
        self.data_dir= "C:/Users/ericu/Documents/GitHub/Airsim_Build/data"

    def execute(self):

        CameraLoop=RepeatThread_with_pause.Thread(self.data_dir)    
        CameraLoop.start_image_callback_thread()
        time.sleep(3)
        #Pauses Cameraloop function calls, does NOT pause thread
        CameraLoop.pause_image_callback_thread()
        self.client.simPause(True)
        time.sleep(3)
        #UnPauses Cameraloop function calls, does NOT pause thread
        CameraLoop.unpause_image_callback_thread()
        self.client.simPause(False)

        self.client.armDisarm(True)
        airsim.wait_key('Press any key to takeoff')
        self.client.takeoffAsync().join()
        self.client.moveToPositionAsync(-43.70, -47.20, -31.50, 10).join()
        self.client.hoverAsync() 
        time.sleep(5)
        
        CameraLoop.stop_image_callback_thread()
        
    def stop(self):
        airsim.wait_key('Press any key to reset to original state')

        self.client.armDisarm(False)
        self.client.reset()

        self.client.enableApiControl(False)
        print("Done!\n")
# main
if __name__ == "__main__":
    ThreadPause = ThreadPauseTest()

    #Is this a form of error handling?  it looks like it
    #try:
    ThreadPause.execute()
    #finally:
    #    ThreadPause.stop()