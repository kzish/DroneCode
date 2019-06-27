import pymavlink
import time
from pymavlink import mavutil



master = mavutil.mavlink_connection('udpin:127.0.0.1:14550')
master.wait_heartbeat()

master.mav.command_long_send( master.target_system,   master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0, 1, 0, 0, 0, 0, 0, 0)

time.sleep(5)

master.mav.command_long_send( master.target_system,  master.target_component,
    mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
    0, 0, 0, 0, 0, 0, 0,
    50)