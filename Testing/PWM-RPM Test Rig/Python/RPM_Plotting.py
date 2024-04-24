# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 20:14:40 2023

@author: scott
"""

import numpy as np
import matplotlib.pyplot as plt

def omega_to_alpha(omega, time):
    alpha = []
    alpha.append( (omega[1] - omega[0]) / (time[1] - time[0]) )
    alpha.append( (omega[2] - omega[1]) / (time[2] - time[1]) )
    alpha.append( (omega[3] - omega[2]) / (time[3] - time[2]) )
    alpha.append( (omega[4] - omega[3]) / (time[4] - time[3]) )
    alpha.append( (omega[5] - omega[4]) / (time[5] - time[4]) )
    alpha.append( (omega[6] - omega[5]) / (time[6] - time[5]) )
    alpha.append( (omega[7] - omega[6]) / (time[7] - time[6]) )
    alpha.append( (omega[8] - omega[7]) / (time[8] - time[7]) )
    alpha.append( (omega[9] - omega[8]) / (time[9] - time[8]) )
    alpha.append( (omega[10] - omega[9]) / (time[10] - time[9]) )
    alpha.append( (omega[11] - omega[10]) / (time[11] - time[10]) )
    alpha = np.asarray(alpha)
    return alpha

##### Dimensions #####
Alum_Ring_OD = .095           # [m] Outer diameter of aluminum ring
Alum_Ring_ID = .008           # [m] Inner diameter of aluminum ring
Alum_Ring_Height = .00625     # [m] thickness of ring

SSPLA_Ring_OD = .095           # [m] Outer diameter of SSPLA ring
SSPLA_Ring_ID = .008           # [m] Inner diameter of SSPLA ring
SSPLA_Ring_Height = .003       # [m] thickness of ring

CF_Flywheel_OD = Alum_Ring_OD # [m] Should be the same ideally.
CF_Flywheel_ID = Alum_Ring_ID # [m] Should be same
CF_Flywheel_Height = 0.002    # [m]

##### Flywheel Assembly Data from SolidWorks #####
# Mass
CF_Flywheel_Mass = .01046          # [kg]
Alum_Ring_Mass = .03437            # [kg] 
SSPLA_Ring_Mass = 0.0115           # [kg]
Total_Flywheel_Mass = 0.04528      # [kg] 

# Moment of Inertia
CF_Flywheel_MOI = 7880.27*1e-9     # [kg*m^2] must convert from g*mm^2 to kg*m^2
Alum_Ring_MOI = 32064.58*1e-9      # [kg*m^2]
Total_Flywheel_MOI = 42395.10*1e-9 # [kg*m^2]

Payload_MOI =  4902907.93*1e-9     # [kg*m^2]

# PWM-RPM data
time = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0])
pwm3180 = np.array([0, 1200, 3000, 3600, 4800, 6000, 6000, 7200, 7200, 7200, 9600, 9120])
pwm3200 = np.array([0, 1920, 3360, 4800, 4320, 6240, 7200, 7680, 8160, 8640, 9600, 10080])
pwm3220 = np.array([0, 2400, 3840, 5280, 6000, 6240, 5760, 6720, 8640, 9120, 9600, 10080])
pwm3240 = np.array([0, 2880, 3840, 4800, 5280, 6240, 6720, 7680, 8640, 10080, 10560, 10560])
pwm3300 = np.array([0, 2400, 2400, 6000, 7200, 7680, 9120, 10080, 10320, 11040, 11520, 12480])
pwm3350 = np.array([0, 3360, 5280, 6720, 8400, 9120, 10080, 10080, 11520, 12000, 12480, 13440])
pwm3400 = np.array([0, 2400, 6240, 7680, 9120, 10080, 10560, 11520, 12000, 13440, 13440, 13920])

# Convert RPMs to angular velocity (rad/s)
omega3180 = pwm3180*(np.pi/30)
omega3200 = pwm3200*(np.pi/30)
omega3220 = pwm3220*(np.pi/30)
omega3240 = pwm3240*(np.pi/30)
omega3300 = pwm3300*(np.pi/30)
omega3350 = pwm3350*(np.pi/30)
omega3400 = pwm3400*(np.pi/30)

alpha3180 = omega_to_alpha(omega3180, time)
alpha3200 = omega_to_alpha(omega3200, time)
alpha3220 = omega_to_alpha(omega3220, time)
alpha3240 = omega_to_alpha(omega3240, time)
alpha3300 = omega_to_alpha(omega3300, time)
alpha3350 = omega_to_alpha(omega3350, time)
alpha3400 = omega_to_alpha(omega3400, time)
alpha_time = np.array([0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0])


# Plot PWM-RPMs
plt.figure(1)
plt.plot(time, pwm3180, ".--", label="3180", color="red")
plt.plot(time, pwm3200, ".--", label="3200", color="orange")
plt.plot(time, pwm3220, ".--", label="3220", color="yellow")
plt.plot(time, pwm3240, ".--", label="3240", color="green")
plt.plot(time, pwm3300, ".--", label="3300", color="blue")
plt.plot(time, pwm3350, ".--", label="3350", color="purple")
plt.plot(time, pwm3400, ".--", label="3400", color="brown")

plt.xlabel("Time [s]")
plt.ylabel("RPM(PWM)")
plt.title("RPMs Impulse Curve")
plt.legend()

# Plot alpha-time
plt.figure(2)
# a, b = np.polyfit(alpha_time, Total_Flywheel_MOI*alpha3180, 1)
# plt.scatter(alpha_time, Total_Flywheel_MOI*alpha3180)
# plt.plot(alpha_time, a*alpha_time+b)
plt.plot(alpha_time, Total_Flywheel_MOI*alpha3180, ".--", label="3180", color="red")
plt.plot(alpha_time, Total_Flywheel_MOI*alpha3200, ".--", label="3200", color="orange")
plt.plot(alpha_time, Total_Flywheel_MOI*alpha3220, ".--", label="3220", color="yellow")
plt.plot(alpha_time, Total_Flywheel_MOI*alpha3240, ".--", label="3240", color="green")
plt.plot(alpha_time, Total_Flywheel_MOI*alpha3300, ".--", label="3300", color="blue")
plt.plot(alpha_time, Total_Flywheel_MOI*alpha3350, ".--", label="3350", color="purple")
plt.plot(alpha_time, Total_Flywheel_MOI*alpha3400, ".--", label="3400", color="brown")

plt.ylim((-0.01,0.1))
plt.xlabel("Time [s]")
plt.ylabel(f"$\\tau$ [N*m]")
plt.title("Torque Impulse Curve")
plt.legend()

# Plot payload alpha-time
plt.figure(3)
plt.plot(alpha_time, (Total_Flywheel_MOI/Payload_MOI)*alpha3180, ".--", label="3180", color="red")
plt.plot(alpha_time, (Total_Flywheel_MOI/Payload_MOI)*alpha3200, ".--", label="3200", color="orange")
plt.plot(alpha_time, (Total_Flywheel_MOI/Payload_MOI)*alpha3220, ".--", label="3220", color="yellow")
plt.plot(alpha_time, (Total_Flywheel_MOI/Payload_MOI)*alpha3240, ".--", label="3240", color="green")
plt.plot(alpha_time, (Total_Flywheel_MOI/Payload_MOI)*alpha3300, ".--", label="3300", color="blue")
plt.plot(alpha_time, (Total_Flywheel_MOI/Payload_MOI)*alpha3350, ".--", label="3350", color="purple")
plt.plot(alpha_time, (Total_Flywheel_MOI/Payload_MOI)*alpha3400, ".--", label="3400", color="brown")

plt.ylim((-1, 10))
plt.xlabel("Time [s]")
plt.ylabel("$\\alpha$ [$rad/s^2$]")
plt.title("Angular Acceleration of Payload Curve")
plt.legend()

# Torque - Velocity
plt.figure(4)
plt.plot(omega3180[0:11], Total_Flywheel_MOI*alpha3180, ".--", label="3180", color="red")
plt.plot(omega3200[0:11], Total_Flywheel_MOI*alpha3200, ".--", label="3200", color="orange")
plt.plot(omega3220[0:11], Total_Flywheel_MOI*alpha3220, ".--", label="3220", color="yellow")
plt.plot(omega3240[0:11], Total_Flywheel_MOI*alpha3240, ".--", label="3240", color="green")
plt.plot(omega3300[0:11], Total_Flywheel_MOI*alpha3300, ".--", label="3300", color="blue")
plt.plot(omega3350[0:11], Total_Flywheel_MOI*alpha3350, ".--", label="3350", color="purple")
plt.plot(omega3400[0:11], Total_Flywheel_MOI*alpha3400, ".--", label="3400", color="brown")

plt.ylim((-0.01,0.1))
plt.xlabel(f"$\\omega$ [rad/s]")
plt.ylabel(f"$\\tau$ [N*m]")
plt.title("Torque-Velocity Curve")
plt.legend()