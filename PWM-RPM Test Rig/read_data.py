import csv
import matplotlib.pyplot as plt
import numpy as np

pi = 3.141592653589793

# Data of flywheel with mass ring attached
diameter = 0.095     # m
radius = diameter/2  # m
mass = 23.26 * 1e-3  # kg
I = 40077.65*1e-9  # kg*m^2


def import_data_from_csv(file_path):
    time = []
    rpm = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header line
        for row in reader:
            if len(row) == 2:
                try:
                    time.append(float(row[0]))
                    rpm.append(float(row[1]))
            
                except ValueError:
                    print("Error: Invalid data format in the CSV file")
                    return None, None
            else:
                print("Error: Invalid number of columns in the CSV file")
                return None, None
    return time, rpm


def torque(time, rpm_duty):
    # calculating torque using formula T = I * alpha^2
    #   I = moment of inertia in
    #   alpha = domega/dt
    #   omega = 2pi * RPMs/60
    dt = np.diff(time)
    omega = 2*pi*np.array(rpm_duty)/60
    alpha = np.diff(omega) / dt
    torque = I * alpha * alpha
    
    return omega, alpha, torque


time, rpm_duty_1953 = import_data_from_csv('rpm_data_duty_1953.csv')
_, rpm_duty_1953 = import_data_from_csv('rpm_data_duty_1953.csv')
_, rpm_duty_1968 = import_data_from_csv('rpm_data_duty_1968.csv')
_, rpm_duty_1998 = import_data_from_csv('rpm_data_duty_1998.csv')
_, rpm_duty_2014 = import_data_from_csv('rpm_data_duty_2014.csv')
_, rpm_duty_2029 = import_data_from_csv('rpm_data_duty_2029.csv')
_, rpm_duty_2044 = import_data_from_csv('rpm_data_duty_2044.csv')
_, rpm_duty_2059 = import_data_from_csv('rpm_data_duty_2059.csv')

# plot RPM-time data
plt.plot(time, rpm_duty_1953, "r--", label="Duty 1953 us")
plt.plot(time, rpm_duty_1968, "y--", label="Duty 1968 us")
plt.plot(time, rpm_duty_1998, "g--", label="Duty 1998 us")
plt.plot(time, rpm_duty_2014, "c--", label="Duty 2014 us")
plt.plot(time, rpm_duty_2029, "b--", label="Duty 2029 us")
plt.plot(time, rpm_duty_2044, "m--", label="Duty 2044 us")
plt.plot(time, rpm_duty_2059, "k--", label="Duty 2059 us")

plt.figure(1)
plt.title("RPM Data for 800 KV motors\n27 March 2024")
plt.ylabel("RPMs")
plt.xlabel("Time [s]")
plt.legend()
plt.savefig('RPM_Plot.png')
#plt.show()

omega_1953, alpha_1953, torque_1953 = torque(time, rpm_duty_1953)

plt.figure(2)
#plt.plot(time, omega_1953)
plt.plot(time[0:50], alpha_1953)
#plt.plot(time, torque_1953)
plt.title("Angular velocity vs Time")
plt.ylabel("omega [rad/s]")
plt.xlabel("Time [s]")
plt.show()
