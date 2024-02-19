from pymavlink import mavutil
import time
the_connection = mavutil.mavlink_connection('COM7')

# Wait for the first heartbeat 
#This sets the system and component ID of remote system for the link
the_connection.mav.heartbeat_send(mavutil.mavlink.MAV_TYPE_ONBOARD_CONTROLLER,mavutil.mavlink.MAV_AUTOPILOT_INVALID, 0, 0, 0)
the_connection.wait_heartbeat()
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 21196, 0, 0, 0, 0, 0)
# Once connected, use 'the_connection' to get and send messages

while 1:
    #msg0 = the_connection.recv_match(type ='BATTERY_STATUS',blocking=True).to_dict()
    msg1 = the_connection.recv_match(type ='ATTITUDE',blocking=True).to_dict()
    msg2 = the_connection.recv_match(type ='ALTITUDE',blocking=True).to_dict()
    #print(msg0['voltages'][0],msg1['yaw'],msg2['altitude_amsl'])
  
    #print('#####')
    if(msg1['yaw']>0) or (msg1['yaw']<0) :
        the_connection.mav.command_long_send(the_connection.target_system,the_connection.target_component,mavutil.mavlink.MAV_CMD_CONDITION_YAW,0,0,90,0,0,0,0,0)
    if(msg2['altitude_amsl']>60000):
        the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 21196, 0, 0, 0, 0, 0)
        time.sleep(2)

