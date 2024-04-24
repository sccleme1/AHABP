import csv
import matplotlib.pyplot as plt
import numpy as np

pi = 3.141592653589793

# Data of flywheel with mass ring attached
diameter = 0.095     # m
radius = diameter/2  # m
mass = 23.26 * 1e-3  # kg
I = 40077.65*1e-9    # kg*m^2
I_payload = 2*1476019.48*1e-9

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
    # calculating torque using formula T = I * alpha
    #   I = moment of inertia in kg*m^2
    #   alpha = domega/dt
    #   omega = 2pi * RPMs/60
    dt = np.diff(time)
    omega = 2*pi*np.array(rpm_duty)/60
    alpha = np.diff(omega) / dt
    torque = I * alpha
    
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
plt.plot(time, rpm_duty_1953, "r--", alpha=0.7, label="Duty 1953 us")
plt.plot(time, rpm_duty_1968, "y--", alpha=0.7, label="Duty 1968 us")
plt.plot(time, rpm_duty_1998, "g--", alpha=0.7, label="Duty 1998 us")
plt.plot(time, rpm_duty_2014, "c--", alpha=0.7, label="Duty 2014 us")
plt.plot(time, rpm_duty_2029, "b--", alpha=0.7, label="Duty 2029 us")
plt.plot(time, rpm_duty_2044, "m--", alpha=0.7, label="Duty 2044 us")
plt.plot(time, rpm_duty_2059, "k--", alpha=0.7, label="Duty 2059 us")

plt.figure(1)
plt.title("RPMs from PWM Duty (Square Wave)\n800 KV Motor with v3 Flywheel")
plt.ylabel("RPMs")
plt.xlabel("Time [s]")
plt.legend()
plt.savefig('RPM_Plot.png')


omega_1953, alpha_1953, torque_1953 = torque(time, rpm_duty_1953)
omega_1968, alpha_1968, torque_1968 = torque(time, rpm_duty_1968)
omega_1998, alpha_1998, torque_1998 = torque(time, rpm_duty_1998)
omega_2014, alpha_2014, torque_2014 = torque(time, rpm_duty_2014)
omega_2029, alpha_2029, torque_2029 = torque(time, rpm_duty_2029)
omega_2044, alpha_2044, torque_2044 = torque(time, rpm_duty_2044)
omega_2059, alpha_2059, torque_2059 = torque(time, rpm_duty_2059)


plt.figure(2)
##plt.plot(omega_1953[0:50], torque_1953, "r--", label="Duty 1953 us")
##plt.plot(omega_1968[0:50], torque_1968, "y--", label="Duty 1968 us")
##plt.plot(omega_1998[0:50], torque_1998, "g--", label="Duty 1998 us")
##plt.plot(omega_2014[0:50], torque_2014, "c--", label="Duty 2014 us")
##plt.plot(omega_2029[0:50], torque_2029, "b--", label="Duty 2029 us")
##plt.plot(omega_2044[0:50], torque_2044, "m--", label="Duty 2044 us")
##plt.plot(omega_2059[0:50], torque_2059, "k--", label="Duty 2059 us")

plt.plot(time[0:50], torque_1953, "r--", alpha=0.7, label="Duty 1953 us")
plt.plot(time[0:50], torque_1968, "y--", alpha=0.7, label="Duty 1968 us")
plt.plot(time[0:50], torque_1998, "g--", alpha=0.7, label="Duty 1998 us")
plt.plot(time[0:50], torque_2014, "c--", alpha=0.7, label="Duty 2014 us")
plt.plot(time[0:50], torque_2029, "b--", alpha=0.7, label="Duty 2029 us")
plt.plot(time[0:50], torque_2044, "m--", alpha=0.7, label="Duty 2044 us")
plt.plot(time[0:50], torque_2059, "k--", alpha=0.7, label="Duty 2059 us")
plt.title("Calculated Torque\n800 KV Motor with v3 Flywheel")
plt.ylabel("Torque [N-m]")
plt.xlabel("Time [s]")
plt.legend()
plt.savefig('RPM_Torque_Plot.png')


plt.figure(3)
plt.plot(time[0:50], torque_1953/I_payload, "r--", alpha=0.7, label="Duty 1953 us")
plt.plot(time[0:50], torque_1968/I_payload, "y--", alpha=0.7, label="Duty 1968 us")
plt.plot(time[0:50], torque_1998/I_payload, "g--", alpha=0.7, label="Duty 1998 us")
plt.plot(time[0:50], torque_2014/I_payload, "c--", alpha=0.7, label="Duty 2014 us")
plt.plot(time[0:50], torque_2029/I_payload, "b--", alpha=0.7, label="Duty 2029 us")
plt.plot(time[0:50], torque_2044/I_payload, "m--", alpha=0.7, label="Duty 2044 us")
plt.plot(time[0:50], torque_2059/I_payload, "k--", alpha=0.7, label="Duty 2059 us")
plt.title("Theoretical Angular Acceleration of Payload\n800 KV Motor with v3 Flywheel")
plt.ylabel("Angular Acceleration [rad/s/s]")
plt.xlabel("Time [s]")
plt.legend()
plt.savefig('RPM_Alpha_Plot.png')


plt.show()
