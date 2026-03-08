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

class Thread:
    def __init__(self,dirname):

        #Clean up clients such that only one is created and the functions them selves are self contained independent of callback name, likely requires logic
        self.image_client = airsim.MultirotorClient()
        self.image_client.confirmConnection()
        self.image_client.enableApiControl(True)

        self.odometry_client = airsim.MultirotorClient()
        self.odometry_client.confirmConnection()
        self.odometry_client.enableApiControl(True)

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

        #user defined at call
        self.dirname=dirname

        self.is_image_thread_paused =False
        self.is_odometry_thread_paused =False

    def repeat_timer_image_callback(self, task, period):
        while self.is_image_thread_active:
            if not self.is_image_thread_paused:
                task()
                time.sleep(period)

    def repeat_timer_odometry_callback(self, task, period):
        while self.is_odometry_thread_active:
             if not self.is_odometry_thread_paused:
                task()
                time.sleep(period)

    def image_callback(self):

        #print("called image function") #suppressed log function
        
        responses = self.image_client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene)]) #scene vision image in png format
        
        #print('Retrieved images: %d' % len(responses))  #suppressed log function
        dir = self.dirname
        #print ("Saving images to %s" % tmp_dir)  #suppressed log function
        try:
            os.makedirs(dir)
        except OSError:
            if not os.path.isdir(dir):
                raise
        for idx, response in enumerate(responses):
            filename = os.path.join(dir, time.strftime("%a_%d_%b_%Y_%H_%M_%S"))
            #print("Type %d, size %d" % (response.image_type, len(response.image_data_uint8))) #suppressed log function
            airsim.write_file(os.path.normpath(filename + '.png'), response.image_data_uint8)

    def odometry_callback(self):
        dir = self.dirname
        print("called odometry function") #suprressed log function
        try:
            os.makedirs(dir)
        except OSError:
            if not os.path.isdir(dir):
                raise
        filename = os.path.join(dir, "IMUdata.txt") #move this function out to the user
        imu_data = self.odometry_client.getImuData()
        acc = pprint.pformat(imu_data)
        #print("imu_data: %s" % acc) #suprressed log function
        with open(filename, "a") as myfile:
            #myfile.write(acc)
            myfile.write(pprint.pformat(imu_data.angular_velocity))
            myfile.write(pprint.pformat(imu_data.linear_acceleration))
            myfile.write(pprint.pformat(imu_data.orientation))
            myfile.write(pprint.pformat(imu_data.time_stamp))
            myfile.write("\n")
            myfile.write(time.strftime("%a_%d_%b_%Y_%H_%M_%S"))
            myfile.write("\n")
        
        #Add cleanup function to avoid unclean datasets
         
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
    
    def pause_image_callback_thread(self):
        self.is_image_thread_paused = True
        print("Paused image callback thread.")

    def unpause_image_callback_thread(self):
        self.is_image_thread_paused = False
        print("Unpaused image callback thread.")

    def pause_odometry_callback_thread(self):
        self.is_odometry_thread_paused = True
        print("Paused odometry callback thread.")

    def unpause_odometry_callback_thread(self):
        self.is_odometry_thread_paused = False
        print("Unpaused odometry callback thread.")