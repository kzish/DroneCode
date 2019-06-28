from __future__ import print_function
from dronekit import connect
import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
import paho.mqtt.client as mqtt
import json

#mqtt
topic_to_server   = "drone_web_console_server"# when sending data to the server
topic_from_server = "mavlink_drone_commands"# when recieving data from the server to seismic sensor 1
server_url        = "192.168.138.1"
server_port       = 1883



# mqtt on connect callback
def on_connect(client, userdata, flags, rc):
    print("Mqtt connected with result code "+str(rc))
    client.subscribe(topic_from_server)#listen for messages from the server
    print("mqtt connected")

# mqtt onmessage recieved
def on_message(client, userdata, msg):
    command = str(msg.payload,'utf-8')
    print(command)
    if command == "func_arm_and_takeoff":
       print(command)
       func_arm_and_takeoff(10)
       
    if command == "func_home_drone":
       print(command)
       func_home_drone()
       
    if command == "func_reboot_vehicle":
       print(command)
       func_reboot_vehicle()
       




#mqtt client setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(server_url, server_port, 60)


use_sitl = False
sitl = None


# Start SITL if no connection string specified
if  use_sitl:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()





vehicle = connect('/dev/serial0', wait_ready=True,baud=57600)
print("Mode: %s" % vehicle.mode.name)

#reboot the vehicle
def func_reboot_vehicle():
    vehicle.reboot()
    vehicle = connect('/dev/serial0', wait_ready=True,baud=57600)
    print("Mode: %s" % vehicle.mode.name)



def func_arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)  # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto
    #  (otherwise the command after Vehicle.simple_takeoff will execute
    #   immediately).
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)
        
    print("Set default/target airspeed to 3")
    vehicle.airspeed = 3

    print("Going towards first point for 5 seconds ...")
    point1 = LocationGlobalRelative(-35.361354, 149.165218, 20)
    vehicle.simple_goto(point1)

    # sleep so we can see the change in map
    time.sleep(5)

    print("Going towards second point for 5 seconds (groundspeed set to 10 m/s) ...")
    point2 = LocationGlobalRelative(-35.363244, 149.168801, 20)
    vehicle.simple_goto(point2, groundspeed=10)

    # sleep so we can see the change in map
    time.sleep(5)

    print("Returning to Launch")
    vehicle.mode = VehicleMode("RTL")

    # Shut down simulator if it was started.
    if sitl:
       sitl.stop()

def func_home_drone():
	#bring the drone back home
	print("Returning to Launch")
	vehicle.mode = VehicleMode("RTL")
	# Close vehicle object before exiting script
	print("Close vehicle object")
	vehicle.close()
	# Shut down simulator if it was started.
	if sitl:
	    sitl.stop()






#mqtt loop
client.loop_forever() 
