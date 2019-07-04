from dronekit import connect, VehicleMode
import time

#vehicle=connect('/dev/ttyUSB0', baud=57600)

# Set up option parsing to get connection string
## $ python dronekit_test_02.py --connect udp:127.0.0.1:14551
import argparse  
parser = argparse.ArgumentParser(description='Print out vehicle state information. Connects to SITL on local PC by default.')
parser.add_argument('--connect', default='127.0.0.1:14551', help="vehicle connection target. Default '127.0.0.1:14551'")
args = parser.parse_args()

# Connect to the Vehicle
print('Connecting to vehicle on: %s' %args.connect)
vehicle = connect(args.connect, wait_ready=True)


def arm_and_takeoff(aTargetAltitude):

    print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    while not vehicle.is_armable:
        print("Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode    = VehicleMode("GUIDED")
    vehicle.armed   = True

    while not vehicle.armed:
        print("Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    # after Vehicle.simple_takeoff will execute immediately).
    while True:
        print("Altitude: ", vehicle.location.global_relative_frame.alt)
        #Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

arm_and_takeoff(5)