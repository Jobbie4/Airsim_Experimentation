import setup_path
import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2
import time

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

#get ground truth data
#state = client.getMultirotorState()
#s = pprint.pformat(state)
#print("ground truth state: %s" % s)
#

#get GPS data
#gps_data = client.getGpsData()
#s = pprint.pformat(gps_data)
#print("gps_data: %s" % s)

#get IMU data
imu_data = client.getImuData()
acc = pprint.pformat(imu_data)
print("imu_data: %s" % acc)
dir="C:/Users/ericu/Documents/GitHub/Airsim_Build/data"
filename = os.path.join(dir, "IMUdata.txt")
imu_data = client.getImuData()
acc = pprint.pformat(imu_data)
print("imu_data: %s" % acc)
with open(filename, "a") as myfile:
    myfile.write(acc)
    myfile.write("\n")
    myfile.write(time.strftime("%a_%d_%b_%Y_%H_%M_%S"))

#Add cleanup function to avoid unclean datasets

# that's enough fun for now. let's quit cleanly
client.enableApiControl(False)
