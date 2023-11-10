# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 20:14:40 2023

@author: scott
"""

import matplotlib.pyplot as plt

time = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 7.0]
pwm3180 = [0, 1200, 3000, 3600, 4800, 6000, 6000, 7200, 7200, 7200, 9600, 9120]
pwm3200 = [0, 1920, 3360, 4800, 4320, 6240, 7200, 7680, 8160, 8640, 9600, 10080]
pwm3220 = [0, 2400, 3840, 5280, 6000, 6240, 5760, 6720, 8640, 9120, 9600, 10080]
pwm3240 = [0, 2880, 3840, 4800, 5280, 6240, 6720, 7680, 8640, 10080, 10560, 10560]
pwm3300 = [0, 2400, 2400, 6000, 7200, 7680, 9120, 10080, 10320, 11040, 11520, 12480]
pwm3350 = [0, 3360, 5280, 6720, 8400, 9120, 10080, 10080, 11520, 12000, 12480, 13440]
pwm3400 = [0, 2400, 6240, 7680, 9120, 10080, 10560, 11520, 12000, 13440, 13440, 13920]


plt.plot(time, pwm3180, label="3180", color="red")
plt.plot(time, pwm3200, label="3200", color="orange")
plt.plot(time, pwm3220, label="3220", color="yellow")
plt.plot(time, pwm3240, label="3240", color="green")
plt.plot(time, pwm3300, label="3300", color="blue")
plt.plot(time, pwm3350, label="3350", color="purple")
plt.plot(time, pwm3400, label="3400", color="brown")

plt.xlabel("Time [s]")
plt.ylabel("RPMs")
plt.title("PWM-RPMs Curve")
plt.legend()