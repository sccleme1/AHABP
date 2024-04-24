# Title: Autonomous High-Altitude Payload Torque Calculations
# Name: Bryan, Anyell, Scott
# Date: 11/11/23
# Description: This code will calculate the torque from Scott's reaction wheel.

import numpy as np
import matplotlib.pyplot as plt

##### Dimensions #####
Alum_Ring_OD = .095           # [m] Outer diameter of aluminum ring
Alum_Ring_ID = .008           # [m] Inner diameter of aluminum ring
Alum_Ring_Height = .00625     # [m] thickness of ring

CF_Flywheel_OD = Alum_Ring_OD # [m] Should be the same ideally.
CF_Flywheel_ID = Alum_Ring_ID # [m] Should be same
CF_Flywheel_Height = 0.002    # [m]

##### Flywheel Assembly Data from SolidWorks #####
# Mass
CF_Flywheel_Mass = .01046          # [kg]
Alum_Ring_Mass = .03437            # [kg] 
Total_Flywheel_Mass = 0.04528      # [kg] 

# Moment of Inertia
CF_Flywheel_MOI = 7880.27*1e-9     # [kg*m^2] must convert from g*mm^2 to kg*m^2
Alum_Ring_MOI = 32064.58*1e-9      # [kg*m^2]
Total_Flywheel_MOI = 42395.10*1e-9 # [kg*m^2]

RPM1 = 9120 # [RPM] Based on PWM-RPMs test. Using 3 second ramp-up time from 3300 microsecond PWM value curve b/c it has somewhat linear slope.
omega1 = (RPM1*np.pi)/30 # [rad/s] rpms to rad/s


print("CF Flywheel MOI:\t", round(CF_Flywheel_MOI, 9), "kg*m^2 (z-axis only)")
print("Aluminum Ring MOI:\t", round(Alum_Ring_MOI, 9), "kg*m^2 (z-axis only)")
print("Flywheel MOI:\t\t", round(Total_Flywheel_MOI, 9), "kg*m^2 (z-axis only)")
print("% MOI is Aluminum:\t", round(100*Alum_Ring_MOI/Total_Flywheel_MOI, 2), "%")
print()
print(f"At {RPM1} RPMs, omega = {round(RPM1*np.pi/30, 2)} rad/s")

