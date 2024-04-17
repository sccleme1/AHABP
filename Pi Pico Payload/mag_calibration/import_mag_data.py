import csv
import matplotlib.pyplot as plt
import numpy as np
import datetime
from scipy.optimize import curve_fit


def ellipse(x, h, k, a, b):
    return ((x[0] - h) ** 2 / a ** 2 + (x[1] - k) ** 2 / b ** 2 - 1)


def import_data_from_csv(file_path):
    mx = []
    my = []
    mz = []
    heading1 = []
    heading2 = []
    heading3 = []
    time = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header line
        for row in reader:
            if len(row) == 7:
                try:
                    mx.append(float(row[0]))
                    my.append(float(row[1]))
                    mz.append(float(row[2]))
                    heading1.append(float(row[3]))
                    heading2.append(float(row[4]))
                    heading3.append(float(row[5]))
                    time.append(float(row[6]))
                except ValueError:
                    print("Error: Invalid data format in the CSV file")
                    return None, None
##            else:
##                print("Error: Invalid number of columns in the CSV file")
##                return None, None
    return mx, my, mz, heading1, heading2, heading3, time

mx, my, mz, heading1, heading2, heading3, time = import_data_from_csv('mag_data.csv')

# Maximum/Minimum/Average values
max_x = max(mx)
min_x = min(mx)
avg_x = sum(mx) / len(mx)
range_x = max_x - min_x
print(f"X data\tmax = {round(max_x, 3)}\tmin = {round(min_x, 3)}\trange = {round(range_x, 3)}\taverage = {round(avg_x, 3)}")

max_y = max(my)
min_y = min(my)
avg_y = sum(my) / len(my)
range_y = max_y - min_y
print(f"Y data\tmax = {round(max_y, 3)}\tmin = {round(min_y, 3)}\trange = {round(range_y, 3)}\taverage = {round(avg_y, 3)}")

max_z = max(mz)
min_z = min(mz)
avg_z = sum(mz) / len(mz)
range_z = max_z - min_z
print(f"Z data\tmax = {round(max_z, 3)}\tmin = {round(min_z, 3)}\trange = {round(range_z, 3)}\taverage = {round(avg_z, 3)}")
date = datetime.datetime.now()


### Initial guess for parameters (center and axes lengths)
##initial_guess_xy = [avg_x, avg_y, range_x/2, range_y/2]
##params_xy, covariance_xy = curve_fit(ellipse, (mx, my), np.ones(len(mx)), p0=initial_guess_xy)
##h_xy, k_xy, a_xy, b_xy = params_xy
##print(f"X-Y data\th = {round(h_xy, 3)}\tk = {round(k_xy, 3)}\ta = {round(a_xy, 3)}\tb = {round(b_xy, 3)}\ta/b = {round(a_xy/b_xy, 3)}")
##
##initial_guess_yz = [avg_y, avg_z, range_y/2, range_z/2]
##params_yz, covariance_yz = curve_fit(ellipse, (my, mz), np.ones(len(my)), p0=initial_guess_yz)
##h_yz, k_yz, a_yz, b_yz = params_yz
##print(f"Y-Z data\th = {round(h_yz, 3)}\tk = {round(k_yz, 3)}\ta = {round(a_yz, 3)}\tb = {round(b_yz, 3)}\ta/b = {round(a_yz/b_yz, 3)}")
##
##initial_guess_zx = [avg_z, avg_x, range_z/2, range_x/2]
##params_zx, covariance_zx = curve_fit(ellipse, (mz, mx), np.ones(len(mz)), p0=initial_guess_zx)
##h_zx, k_zx, a_zx, b_zx = params_zx
##print(f"Z-X data\th = {round(h_zx, 3)}\tk = {round(k_zx, 3)}\ta = {round(a_zx, 3)}\tb = {round(b_zx, 3)}\ta/b = {round(a_zx/b_zx, 3)}")


plt.figure(1)
plt.plot(mx, my, "r.", alpha=0.5, label="x-y")
plt.plot(my, mz, "g.", alpha=0.5, label="y-z")
plt.plot(mz, mx, "b.", alpha=0.5, label="z-x")
plt.plot(0, 0, "ko")
plt.title(f"Magnetometer Values\n{date}")
plt.xlabel("Magnetometer")
plt.ylabel("Magnetometer")
plt.legend()
plt.axis('square')
plt.grid(True, which='both', axis='both', linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
plt.savefig("Mag.png")

plt.figure(2)
plt.plot(mx, my, "r.", alpha=0.5, label="x-y")
plt.plot(0, 0, "ko")
plt.title(f"Magnetometer X-Y Values\n{date}")
plt.xlabel("Magnetometer X")
plt.ylabel("Magnetometer Y")
plt.legend()
plt.axis('square')
plt.grid(True, which='both', axis='both', linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
plt.savefig("MagXY.png")

plt.figure(3)
plt.plot(my, mz, "g.", alpha=0.5, label="y-z")
plt.plot(0, 0, "ko")
plt.title(f"Magnetometer Y-Z Values\n{date}")
plt.xlabel("Magnetometer Y")
plt.ylabel("Magnetometer Z")
plt.legend()
plt.axis('square')
plt.grid(True, which='both', axis='both', linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
plt.savefig("MagYZ.png")

plt.figure(4)
plt.plot(mz, mx, "b.", alpha=0.5, label="z-x")
plt.plot(0, 0, "ko")
plt.title(f"Magnetometer Z-X Values\n{date}")
plt.xlabel("Magnetometer Z")
plt.ylabel("Magnetometer X")
plt.legend()
plt.axis('square')
plt.grid(True, which='both', axis='both', linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
plt.savefig("MagZX.png")

plt.figure(5)
plt.plot(time, heading1, "r.-", alpha=0.5, label="xy Heading")
plt.plot(time, heading2, "g.-", alpha=0.5, label="yz Heading")
plt.plot(time, heading3, "b.-", alpha=0.5, label="zx Heading")
plt.title(f"Heading Values\n{date}")
plt.ylabel("Heading [deg]")
plt.xlabel("Time [s]")
plt.legend()
plt.grid(True, which='both', axis='both', linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
plt.savefig("Heading.png")

plt.figure(6)
plt.plot(time, heading1, "r.-", alpha=0.5, label="xy Heading")
plt.title(f"X-Y Heading Values\n{date}")
plt.ylabel("Heading [deg]")
plt.xlabel("Time [s]")
plt.legend()
plt.grid(True, which='both', axis='both', linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
plt.savefig("HeadingXY.png")

plt.figure(7)
plt.plot(time, heading2, "g.-", alpha=0.5, label="yz Heading")
plt.title(f"Y-Z Heading Values\n{date}")
plt.ylabel("Heading [deg]")
plt.xlabel("Time [s]")
plt.legend()
plt.grid(True, which='both', axis='both', linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
plt.savefig("HeadingYZ.png")

plt.figure(8)
plt.plot(time, heading3, "b.-", alpha=0.5, label="zx Heading")
plt.title(f"Z-X Heading Values\n{date}")
plt.ylabel("Heading [deg]")
plt.xlabel("Time [s]")
plt.legend()
plt.grid(True, which='both', axis='both', linestyle='--', color='gray', linewidth=0.5, alpha=0.5)
plt.savefig("HeadingZX.png")

plt.show()
