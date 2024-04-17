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
    PID = []
    integral = []
    setpoint = []
    error = []
    heading = []
    heading2 = []
    heading3 = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header line
        for row in reader:
            if len(row) == 14:
                try:
                    time.append(float(row[0]))
                    hx.append(float(row[1]))
                    hy.append(float(row[2]))
                    hz.append(float(row[3]))
                    ax.append(float(row[4]))
                    ay.append(float(row[5]))
                    az.append(float(row[6]))
                    PID.append(float(row[7]))
                    integral.append(float(row[8]))
                    setpoint.append(float(row[9]))
                    error.append(float(row[10]))
                    heading.append(float(row[11]))
                    heading2.append(float(row[12]))
                    heading3.append(float(row[13]))
                except ValueError:
                    print("Error: Invalid data format in the CSV file")
                    return None, None
##            else:
##                print("Error: Invalid number of columns in the CSV file")
##                return None, None
    return time, hx, hy, hz, ax, ay, az, integral, setpoint, PID, error, heading, heading2, heading3

time, hx, hy, hz, ax, ay, az, integral, setpoint, PID, error, heading, heading2, heading3 = import_data_from_csv('run_log.csv')

# Maximum/Minimum/Average values
max_x = max(hx)
min_x = min(hx)
range_x = max_x - min_x
avg_x = round((max_x + min_x) / 2, 3)
print(f"X data\tmax = {round(max_x, 3)}\tmin = {round(min_x, 3)}\trange = {round(range_x, 3)}\taverage = {round(avg_x, 3)}")

max_y = max(hy)
min_y = min(hy)
avg_y = round((max_y + min_y) / 2, 3)
range_y = max_y - min_y
print(f"Y data\tmax = {round(max_y, 3)}\tmin = {round(min_y, 3)}\trange = {round(range_y, 3)}\taverage = {round(avg_y, 3)}")

max_z = max(hz)
min_z = min(hz)
avg_z = round((max_z + min_z) / 2, 3)
range_z = max_z - min_z
print(f"Z data\tmax = {round(max_z, 3)}\tmin = {round(min_z, 3)}\trange = {round(range_z, 3)}")

r_xy = round((range_x + range_y)/4, 3)
#print(f"XY Heading: (x - {avg_x})^2 + (y - {avg_y})^2 = {r_xy}^2")
print(f"Calibration:")
print(f"r = {r_xy}")
print(f"(h, k) = ({avg_x}, {avg_y})")

todays_date = datetime.datetime.now()
date = todays_date.strftime("%d %b %Y %H:%M:%S")

# plot RPM-time data
plt.figure(1)
plt.plot(hx, hy, "r.", alpha=0.5, label="x-y")
plt.plot(hy, hz, "g.", alpha=0.5, label="y-z")
plt.plot(hz, hx, "b.", alpha=0.5, label="z-x")
plt.plot(0, 0, "ko")
plt.title(f"Magnetometer Values\n{date}")
plt.ylabel("Magnetometer")
plt.xlabel("Magnetometer")
plt.axis('square')
plt.legend()
plt.grid(True, which='both', axis='both', linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
plt.savefig("Mag.png")

plt.figure(2)
plt.plot(time, ax, "r.-", alpha=0.7, label="ax")
plt.plot(time, ay, "g.-", alpha=0.7, label="ay")
plt.plot(time, az, "b.-", alpha=0.7, label="az")
plt.title(f"Acceleration Values\n{date}")
plt.ylabel("Acceleration [G]")
plt.xlabel("Time [s]")
plt.legend()
plt.grid(True, which='both', axis='both', linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
plt.savefig("Accel.png")

plt.figure(3)
plt.plot(time, heading, "r.-", alpha=0.7, label="Heading")
plt.plot(time, setpoint, "g.-", alpha=0.7, label="Setpoint")
plt.title(f"Payload Heading\n{date}")
plt.ylabel("Heading [deg]")
plt.xlabel("Time [s]")
plt.legend()
plt.grid(True, which='both', axis='both', linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
plt.savefig("Heading.png")

plt.figure(4)
plt.plot(time, PID, "g.-", alpha=0.7, label="PID Output")
plt.plot(time, error, "r.-", alpha=0.7, label="Error")
#plt.plot(time, integral, "b.-", alpha=0.7, label="Integral")
plt.title(f"Integral\n{date}")
plt.ylabel("Integral")
plt.xlabel("Time [s]")
plt.legend()
plt.grid(True, which='both', axis='both', linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
plt.savefig("PID.png")

plt.figure(5)
plt.plot(time, heading, "r.-", alpha=0.5, label="xy Heading")
plt.plot(time, heading2, "g.-", alpha=0.5, label="yz Heading")
plt.plot(time, heading3, "b.-", alpha=0.5, label="zx Heading")
plt.title(f"Heading Values\n{date}")
plt.ylabel("Heading [deg]")
plt.xlabel("Time [s]")
plt.legend()
plt.grid(True, which='both', axis='both', linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
plt.savefig("Heading.png")

plt.show()
