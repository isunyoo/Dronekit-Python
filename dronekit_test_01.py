## $ python dronekit_test_01.py --connect udp:127.0.0.1:14551

import time, math
from dronekit import connect, VehicleMode, LocationGlobalRelative, Command
from pymavlink import mavutil

# Set up option parsing to get connection string
import argparse  
parser = argparse.ArgumentParser(description='Print out vehicle state information. Connects to SITL on local PC by default.')
parser.add_argument('--connect', default='127.0.0.1:14551', help="vehicle connection target. Default '127.0.0.1:14551'")
args = parser.parse_args()

# Connect to the Vehicle
print('Connecting to vehicle on: %s' %args.connect)
vehicle = connect(args.connect, wait_ready=True)

# Define the function for takeoff
def arm_and_takeoff(tgt_altitude):
	print("Arming motors")

	# Don't let the user try to arm until autopilot is ready
	while not vehicle.is_armable:    	
		time.sleep(1)
		print("Waiting for vehicle to initialise...")
	
    # Copter should arm in GUIDED mode
	print("Arming motors")
	vehicle.mode = VehicleMode("GUIDED")
	vehicle.armed = True

	while not vehicle.armed:
		time.sleep(1)
		print("Waiting for arming...")

	print("Takeoff")
	vehicle.simple_takeoff(tgt_altitude)

	# Wait to reach the target altitude
	while True:
		altitude = vehicle.location.global_relative_frame.alt

		if altitude >= tgt_altitude-1:
			print("Altitude reached")
			break 

		time.sleep(1)

# Main Program
arm_and_takeoff(10)

# Set the default speed
vehicle.airspeed = 7

# Go to wp1
print("Go to wp1")
wp1 = LocationGlobalRelative(1.371882, 103.946889, 10)

vehicle.simple_goto(wp1)
time.sleep(30)

# Coming back
print("Coming back")
vehicle.mode = VehicleMode("RTL")
time.sleep(20)

# Close Connection
vehicle.close()



