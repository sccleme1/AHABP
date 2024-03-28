# Scott Clemens
# 26 March 2024
# Autonomous High-Altitude Balloon Payload
#
#
### TRACKING ###

import ephem
import cv2 as cv
import time
import datetime
import os
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy
from px4_msgs.msg import OffboardControlMode, TrajectorySetpoint, VehicleCommand, VehicleLocalPosition, VehicleStatus, VehicleAttitudeSetpoint # These are types of topics. Check 'dds_topics.yaml'


date = datetime.datetime.now()

# global variables
pi = 3.14159265358979323846

# camera servo angle limits
# +76 is maximum
# 0 is horizontal
# -28 is minimum
camera_angle = 0

# folder to store images within workspace
path = '/home/anyell/ahabp_v2_ws/Images'

# file to save log information to
data_file = 'launch_data.csv'
file = open(data_file, 'w')
file.write(f"Data log for {date}\n")
file.write(f"Time,Latitude,Longitude,Altitude,Zenith,Azimuth,Heading,Camera,Yaw,Pitch\n")
file.close()

# opencv object tracking stuff
capture = cv.VideoCapture(0)
cx = 320
cy = 240
horizontal_threshold = 100
vertical_threshold = 50
picture = 1
i = 0

print('##### Hi from ahabp_node_tracking_2.py #####')


def get_compass_direction(angle):
    ''' This converts degrees to cardinal directions for ease of reading '''
    
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    index = round(angle / (360. / len(directions))) % len(directions)
    
    return directions[index]


def sun_angle_and_direction(latitude, longitude, date):
    ''' This function calculates zenith, azimuth, and compass direction
    based on the GPS and date/time data '''
    
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)

    observer.date = date
    sun = ephem.Sun(observer)

    zenith_angle = 90 - sun.alt*180/pi
    azimuth_angle = (sun.az*180/pi) % 360
    compass_direction = get_compass_direction(azimuth_angle)

    return zenith_angle, azimuth_angle, compass_direction


def movement_needed(payload_heading, azimuth_angle, zenith_angle):
    ''' This function calculates yaw and pitch error '''
    
    yaw = round(azimuth_angle - payload_heading, 2)
    pitch = round(zenith_angle - camera_angle, 2)

    return yaw, pitch


def ephem_update():
    ''' This function calculates the zenith and azimuth of the Sun
        based on the real-time GPS and heading data from the payload '''

    latitude = 30.266666    # REAL-TIME
    longitude = -97.733330  # REAL-TIME
    altitude = 100          # REAL-TIME
    payload_heading = 88    # REAL-TIME

    date = datetime.datetime.now()
    zenith_angle, azimuth_angle, compass_direction = sun_angle_and_direction(latitude, longitude, date)
    yaw_ephem, pitch_ephem = movement_needed(payload_heading, azimuth_angle, zenith_angle)

    return yaw_ephem, pitch_ephem, latitude, longitude, altitude


def target(frame, minimum=250, cx=320, cy=240):
    ''' This function targets the centroid of a frame and outputs
        vector in x and y of the error between center of frame and the centroid
        
        Raspberry Pi Camera v2 the image size is:
        480 rows (vertical)
        640 columns (horizontal)
    '''
    
    # copy and convert image to grayscale then process
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    thresholding, thresh = cv.threshold(gray, minimum, 255, cv.THRESH_BINARY)   
    (minVal, maxVal, minLoc, maxLoc) = cv.minMaxLoc(gray)
    M = cv.moments(thresh)

    # calculate centroid
    targx = int(M["m10"] / (M["m00"]+1))
    targy = int(M["m01"] / (M["m00"]+1))

    # calculate direction vector from center to centroid
    yaw_target = targx - cx
    pitch_target = targy - cy

    # place vector arrow and label
    cv.putText(frame, "target", (targx - 45, targy + 45), cv.FONT_HERSHEY_SIMPLEX, 1, (25, 25, 255), 2)
    cv.circle(frame, [targx, targy], 25, (25, 25, 255), 2)
    cv.arrowedLine(frame, [cx, cy], [targx, targy], (25, 25, 255), 2) # center --> target

    return yaw_target, pitch_target, frame


class PID:
    def __init__(self, Kp, Ki, Kd, setpoint):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint  # heading
        self.prev_error = 0
        self.integral = 0

    def update(self, current_value):
        ''' This function calculates PID control '''
        #####################################################
        #####################################################
        #### SETPOINT IS A HEADING FROM 0 - 360 degrees  ####
        ####    EDGE CASE WHEN SETPOINT NEAR 0 OR 360    #### 
        error = self.setpoint - current_value

        # Proportional
        P = self.Kp * error

        # Integral
        self.integral += error
        I = self.Ki * self.integral

        # Derivative
        D = self.Kd * (error - self.prev_error)
        self.prev_error = error

        # PID output
        output = P + I + D

        ### output will be either positive or negative    ###
        ### we need to normalize this between -1 and 1,   ###
        ### where positive is one direction, and negative ###
        ### is the opposite direction                     ###
        return output


class GPSPublisher(Node):
    def __init__(self):
        super().__init__('gps_publisher') # This is the name of the node. It will appear as a oval in rqt's node graph.

        # Configure QoS profile for publishing and subscribing
        qos_profile = QoSProfile( # Relevant: https://answers.ros.org/question/332207/cant-receive-data-in-python-node/
            reliability = ReliabilityPolicy.BEST_EFFORT,
            durability  = DurabilityPolicy.TRANSIENT_LOCAL,
            history     = HistoryPolicy.KEEP_LAST,
            depth       = 10  # Adjust the queue size as needed
        )

        # Create subscribers
        self.vehicle_local_position_subscriber = self.create_subscription(
            VehicleLocalPosition, # px4_msg uORB message. Check 'pX4_msgs/msg'
            '/fmu/out/vehicle_local_position', # topic type. Check 'dds_topics.yaml'
            self.vehicle_local_position_callback, # Callback function
            qos_profile # QoS
        )

        # Initialize internal variables
        self.offboard_setpoint_counter = 0
        self.local_timestamp = 0
        self.picture = 0

        self.vehicle_local_position = VehicleLocalPosition()        

        # Create a timer to publish control commands
        self.timer = self.create_timer(.1, self.timer_callback) 


    # Callback function for vehicle_local_position topic subscriber.
    def vehicle_local_position_callback(self, vehicle_local_position):
        self.vehicle_local_position = vehicle_local_position


    # Callback function for the timer
    def timer_callback(self) -> None: # Needed for publishing rate
        print('In timer callback function: ', self.offboard_setpoint_counter)


        ################################################################################
        ################################################################################
        ### WHY IS THIS HERE? WE NEED THIS IN A WHILE LOOP FOR THE TRACKING TO WORK ####
        istrue, frame = capture.read()
        date = datetime.datetime.now()
        original = frame.copy()
        ################################################################################
        ################################################################################

        # error calculations
        # 'ephem' error is based on calculation with GPS/heading
        # 'target' error is based on what's in the camera frame
        yaw_ephem, pitch_ephem, latitude, longitude, altitude = ephem_update()
        yaw_target, pitch_target, targeted = target(frame)

        
        ### Output screens ###
        #cv.imshow('Output', thresh)
        #cv.imshow('Camera', frame)

        # This is where the actuator stuff goes
        if pitch_target > vertical_threshold:
            print("Vertical error:", pitch_target, "pitch DOWN")
            # PITCH DOWN
        elif pitch_target < -1*vertical_threshold:
            print("Vertical error:", pitch_target, "pitch UP")
            # PITCH UP

        if yaw_target > horizontal_threshold:
            # This is where the actuator stuff goes
            print("Horizontal error:", yaw_target - cx, "pitch LEFT")
            # PITCH DOWN
        elif yaw_target < -1*horizontal_threshold:
            print("Horizontal error:", yaw_target - cx, "pitch RIGHT")
            # PITCH UP

        # append the data to the log file
    #    with open(data_file, "a") as file:
    #        file.write(f"{date},{latitude},{longitude},{altitude},{zenith_angle},{azimuth_angle},{payload_heading},{camera_angle},{yaw_ephem},{pitch_ephem}\n")

        if self.offboard_setpoint_counter >= 300:
            # every 30 seconds, save the images
            cv.imwrite(os.path.join(path, "raw_" + str(self.picture) + "_" + str(datetime.datetime.now()) + ".jpg"), original)
            #cv.imwrite(os.path.join(path, "threshold_" + str(self.picture) + "_" + str(datetime.datetime.now()) + ".jpg"), thresholding)
            cv.imwrite(os.path.join(path, "targeted_" + str(self.picture) + "_" + str(datetime.datetime.now()) + ".jpg"), targeted)
            print(f"Saved picture {self.picture} at {date}")
            self.offboard_setpoint_counter = 0
            self.picture += 1
        
        #increment i
        self.offboard_setpoint_counter += 1

        # if self.offboard_setpoint_counter <= 10:
        #     self.offboard_setpoint_counter += 1

        # elif self.offboard_setpoint_counter > 10:
        #     print('Setpoint resetting...')
        #     self.offboard_setpoint_counter = 0

        print('Leaving timer callback...')


def main(args=None) -> None:
    rclpy.init(args=args) # Starts
    gps_pub = GPSPublisher() # Create a publisher for the OffboardControlMode message. Stays the majority in this function.
    rclpy.spin(gps_pub) # Keep the node alive until Ctrl+C is pressed
    capture.release()
    cv.destroyAllWindows
    gps_pub.destroy_node() # Kills all the nodes
    rclpy.shutdown() # End


if __name__ == '__main__':
    main()


