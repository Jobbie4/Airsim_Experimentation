import setup_path 
import airsim

import math
import os
import pprint
import sys
import time
import tempfile
import argparse
import threading

class RepeatThread:
    def __init__(self):
        self.image_client = airsim.MultirotorClient()
        self.image_client.confirmConnection()
        self.image_client.enableApiControl(True)

        self.image_callback_thread = threading.Thread(
            target=self.repeat_timer_image_callback, 
            args=(self.image_callback, 1),
        )
        self.odometry_callback_thread = threading.Thread(
            target=self.repeat_timer_odometry_callback,
            args=(self.odometry_callback, 0.5),
        )
        self.is_image_thread_active = False
        self.is_odometry_thread_active = False

    def repeat_timer_image_callback(self, task, period):
        while self.is_image_thread_active:
            task()
            time.sleep(period)

    def repeat_timer_odometry_callback(self, task, period):
        while self.is_odometry_thread_active:
            task()
            time.sleep(period)

    def image_callback(self):
        # get uncompressed fpv cam image
        print("called image function")
        # get camera images from the drone
        #airsim.wait_key('Press any key to take images')
        responses = self.image_client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene)]) #scene vision image in png format
        print('Retrieved images: %d' % len(responses))
        tmp_dir = os.path.join(tempfile.gettempdir(), "airsim_drone")
        print ("Saving images to %s" % tmp_dir)
        try:
            os.makedirs(tmp_dir)
        except OSError:
            if not os.path.isdir(tmp_dir):
                raise
        for idx, response in enumerate(responses):
            filename = os.path.join(tmp_dir, time.strftime("%a_%d_%b_%Y_%H_%M_%S"))
            print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8)))
            airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)

    def odometry_callback(self):
        print("called odometry function")
    
    def start_image_callback_thread(self):
        if not self.is_image_thread_active:
            self.is_image_thread_active = True
            self.image_callback_thread.start()
            print("Started image callback thread")

    def stop_image_callback_thread(self):
        if self.is_image_thread_active:
            self.is_image_thread_active = False
            self.image_callback_thread.join()
            print("Stopped image callback thread.")

    def start_odometry_callback_thread(self):
        if not self.is_odometry_thread_active:
            self.is_odometry_thread_active = True
            self.odometry_callback_thread.start()
            print("Started odometry callback thread")

    def stop_odometry_callback_thread(self):
        if self.is_odometry_thread_active:
            self.is_odometry_thread_active = False
            self.odometry_callback_thread.join()
            print("Stopped odometry callback thread.")


# Makes the drone fly and get Lidar data
class Drone_FTP_Cam_loop:

    def __init__(self):

        # connect to the AirSim simulator
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()
        self.client.enableApiControl(True)

    def execute(self):
        print("arming the drone...")
        self.client.armDisarm(True)

        #Begin Camera Loop ...success, now, take out the join 
        TestThread=RepeatThread()
        airsim.wait_key('Press any key to take images')
        TestThread.start_image_callback_thread()
        #time.sleep(5)
      
        #airsim.wait_key('Press any key to takeoff')
        self.client.takeoffAsync().join()
        #Flies in a box and ends at the vertex the box starts on
        #Ascend 
        #Pauses inserted to ensure proper sim operation
        self.client.simPause(True)
        #airsim.wait_key('Press any key to move vehicle Up to  (0, 0, 31.5m) at 5 m/s')
        #time.sleep(2) #paused
        self.client.simPause(False)
        self.client.moveToPositionAsync(0, 0, -31.5, 10)

       
        #Begin Racetrack
        airsim.wait_key('Press any key Begin prescribed Racetrack pattern at 5 m/s')
        #self.client.simPause(True)
       # time.sleep(2) #paused
       # self.client.simPause(False)
        self.client.moveToPositionAsync(-43.70, -47.20, -31.50, 10).join()
        self.client.hoverAsync() #testing if this will override wait , it doesn't
        self.client.moveToPositionAsync(48.30, -47.20, -31.50, 10).join()
        self.client.hoverAsync().join()
        self.client.moveToPositionAsync(48.30, 40.50, -31.50, 10).join()
        self.client.hoverAsync().join()
        self.client.moveToPositionAsync(-43.70, 40.50, -31.50, 10).join()
        self.client.hoverAsync().join()
        self.client.moveToPositionAsync(-43.70, -47.20, -31.50, 10).join()
        
        TestThread.stop_image_callback_thread()
          
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

    arg_parser = argparse.ArgumentParser("drone_FTP_Cam_loop.py makes drone fly a prescribed path and take pictures on that prescribed path")

    arg_parser.add_argument('-save-to-disk', type=bool, help="Not used", default=False)
  
    args = arg_parser.parse_args(args)    
    FTP_Cam_loop = Drone_FTP_Cam_loop()
    try:
        FTP_Cam_loop.execute()
    finally:
        FTP_Cam_loop.stop()
