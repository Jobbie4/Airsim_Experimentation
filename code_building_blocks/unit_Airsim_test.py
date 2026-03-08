import setup_path
import airsim

#Intended to test simple combinations of commands without injecting any thing else 

# connect to the AirSim simulator
client = airsim.MultirotorClient() 
client.confirmConnection()
client.enableApiControl(True)


client.reset()
client.armDisarm(False)

# that's enough fun for now. let's quit cleanly
client.enableApiControl(False)
