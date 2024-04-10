import csv
import matplotlib.pyplot as plt
import numpy as np
import datetime

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
    error = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header line
        for row in reader:
            if len(row) == 12:
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
                    error.append(float(row[11]))
                except ValueError:
                    print("Error: Invalid data format in the CSV file")
                    return None, None
##            else:
##                print("Error: Invalid number of columns in the CSV file")
##                return None, None
    return time, hx, hy, hz, ax, ay, az, heading, integral, setpoint, PID, error


time, hx, hy, hz, ax, ay, az, heading, integral, setpoint, PID, error = import_data_from_csv('run_log.csv')


date = datetime.datetime.now()

# plot RPM-time data
plt.figure(1)
plt.plot(time, hx, "r.-", alpha=0.7, label="x")
plt.plot(time, hy, "g.-", alpha=0.7, label="y")
plt.plot(time, hz, "b.-", alpha=0.7, label="z")
plt.title(f"Magnetometer Values\n{date}")
plt.ylabel("Magnetometer")
plt.xlabel("Time [s]")
plt.legend()
plt.savefig("Mag.png")

plt.figure(2)
plt.plot(time, ax, "r.-", alpha=0.7, label="ax")
plt.plot(time, ay, "g.-", alpha=0.7, label="ay")
plt.plot(time, az, "b.-", alpha=0.7, label="az")
plt.title(f"Acceleration Values\n{date}")
plt.ylabel("Acceleration [G]")
plt.xlabel("Time [s]")
plt.legend()
plt.savefig("Accel.png")

plt.figure(3)
plt.plot(time, heading, "r.-", alpha=0.7, label="Heading")
plt.plot(time, setpoint, "g.-", alpha=0.7, label="Setpoint")
plt.title(f"Payload Heading\n{date}")
plt.ylabel("Heading [deg]")
plt.xlabel("Time [s]")
plt.legend()
plt.savefig("Heading.png")

plt.figure(4)
plt.plot(time, PID, "g.-", alpha=0.7, label="PID Output")
plt.plot(time, error, "r.-", alpha=0.7, label="Error")
plt.plot(time, integral, "b.-", alpha=0.7, label="Integral")
plt.title(f"Integral\n{date}")
plt.ylabel("Integral")
plt.xlabel("Time [s]")
plt.legend()
plt.savefig("PID.png")

plt.show()
