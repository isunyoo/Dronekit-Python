## $ python dronekit_test_connectino.py --connect udp:127.0.0.1:14551

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

cmds = vehicle.commands
cmds.download()
#cmds.wait_valid()

print("About to test clear")
vehicle.commands.clear()
vehicle.flush()
print("Clear succeeded")
