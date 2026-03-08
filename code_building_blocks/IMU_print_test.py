import airsim

import numpy as np
import os
import tempfile
import pprint
import cv2
import time
import pandas as pd

# connect to the AirSim simulator
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

client.simPause(True)
airsim.wait_key('Press any key to takeoff')
client.simPause(False)

print("Taking off...")
client.armDisarm(True)
client.takeoffAsync().join()

#formatting as dict is probably best based on the formatting stuff you get for free



imu_time=[]
image_time=[]
omega_x=[]
omega_y=[]
omega_z=[]

a_x=[]
a_y=[]
a_z=[]

quat_w=[]
quat_x=[]
quat_y=[]
quat_z=[]

for item in range(0,10):
    print(item)
    imu_data = client.getImuData()
    print(pprint.pformat(imu_data))
   
    
    imu_time.append(imu_data.time_stamp)
    image_time.append(time.strftime("%a_%d_%b_%Y_%H_%M_%S"))
                      
    omega_x.append(imu_data.angular_velocity.x_val)
    omega_y.append(imu_data.angular_velocity.y_val)
    omega_z.append(imu_data.angular_velocity.z_val)

    a_x.append(imu_data.linear_acceleration.x_val)
    a_y.append(imu_data.linear_acceleration.y_val)
    a_z.append(imu_data.linear_acceleration.z_val)

    quat_w.append(imu_data.orientation.w_val)
    quat_x.append(imu_data.orientation.x_val)
    quat_y.append(imu_data.orientation.y_val)
    quat_z.append(imu_data.orientation.z_val)
    client.moveToPositionAsync(-10, 10, -10, 5).join()
log=np.empty([len(imu_time),11])
log[:,0]= imu_time
log[:,1]= omega_x
log[:,2]= omega_y
log[:,3]= omega_z
log[:,4]= a_x
log[:,5]= a_y
log[:,6]= a_z
log[:,7]= quat_w
log[:,8]= quat_x
log[:,9]= quat_y
log[:,10]= quat_z

print(log)
print("\n")
print(time.strftime("%a_%d_%b_%Y_%H_%M_%S"))
print("\n")
#create a list iteratively first, THEN create a dataframe from the list, as suspected
#log[:,1]= image_time #append in strings
df = pd.DataFrame(data=log,columns=["imu_time",
                                    "omega_x","omega_y","omega_z",
                                    "a_x","a_y","a_z",
                                    "quat_w","quat_x","quat_y","quat_z"])
df.insert(1,"image_time",image_time)
print(df)
df.to_csv('out.csv', index=False) 

airsim.wait_key('Press any key to reset to original state')
client.simPause(False)

client.reset()
client.armDisarm(False)

# that's enough fun for now. let's quit cleanly
client.enableApiControl(False)
