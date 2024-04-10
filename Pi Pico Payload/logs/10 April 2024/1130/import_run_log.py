import csv
import matplotlib.pyplot as plt
import numpy as np

def import_data_from_csv(file_path):
    time = []
    hx = []
    hy = []
    hz = []
    ax = []
    ay = []
    az = []
    heading = []
    PID = []
    integral = []
    setpoint = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header line
        for row in reader:
            if len(row) == 11:
                try:
                    time.append(float(row[0]))
                    hx.append(float(row[1]))
                    hy.append(float(row[2]))
                    hz.append(float(row[3]))
                    ax.append(float(row[4]))
                    ay.append(float(row[5]))
                    az.append(float(row[6]))
                    heading.append(float(row[7]))
                    PID.append(float(row[8]))
                    integral.append(float(row[9]))
                    setpoint.append(float(row[10]))
                except ValueError:
                    print("Error: Invalid data format in the CSV file")
                    return None, None
##            else:
##                print("Error: Invalid number of columns in the CSV file")
##                return None, None
    return time, hx, hy, hz, ax, ay, az, heading, integral, setpoint, PID


time, hx, hy, hz, ax, ay, az, heading, integral, setpoint, PID = import_data_from_csv('run_log.csv')


# plot RPM-time data
plt.figure(1)
plt.plot(time, hx, "r.-", alpha=0.7, label="x")
plt.plot(time, hy, "g.-", alpha=0.7, label="y")
plt.plot(time, hz, "b.-", alpha=0.7, label="z")
plt.title("Magnetometer Values\n9 April 2024")
plt.ylabel("Magnetometer")
plt.xlabel("Time [s]")
plt.legend()

plt.figure(2)
plt.plot(time, ax, "r.-", alpha=0.7, label="ax")
plt.plot(time, ay, "g.-", alpha=0.7, label="ay")
plt.plot(time, az, "b.-", alpha=0.7, label="az")
plt.title("Acceleration Values\n9 April 2024")
plt.ylabel("Acceleration [G]")
plt.xlabel("Time [s]")
plt.legend()

plt.figure(3)
plt.plot(time, heading, "r.-", alpha=0.7, label="Heading")
plt.plot(time, setpoint, "g.-", alpha=0.7, label="Setpoint")
plt.title("Payload Heading\n9 April 2024")
plt.ylabel("Heading [deg]")
plt.xlabel("Time [s]")
plt.legend()

plt.figure(4)
plt.plot(time, PID, "g.-", alpha=0.7, label="PID Output")
plt.plot(time, integral, "b.-", alpha=0.7, label="Integral")
plt.title("Integral\n9 April 2024")
plt.ylabel("Integral")
plt.xlabel("Time [s]")
plt.legend()

plt.show()
