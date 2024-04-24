import csv
import matplotlib.pyplot as plt

def import_data_from_csv(file_path):
    a = []
    ax = []
    ay = []
    az = []
    t = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header line
        for row in reader:
            if len(row) == 5:
                try:
                    t.append(float(row[0]))
                    a.append(float(row[1]))
                    ax.append(float(row[2]))
                    ay.append(float(row[3]))
                    az.append(float(row[4]))
            
                except ValueError:
                    print("Error: Invalid data format in the CSV file")
                    return None, None
            else:
                print("Error: Invalid number of columns in the CSV file")
                return None, None
    return a, ax, ay, az, t

# Example usage:
file_path = 'v3_loaded_imu_data.csv'  # Change this to your CSV file path
a, ax, ay, az, t = import_data_from_csv(file_path)


plt.plot(t, a, label="|a|")
plt.plot(t, ax, label="ax")
plt.plot(t, ay, label="ay")
plt.plot(t, az, label="az")
plt.legend()
plt.title("IMU Data for HAABP Drop Test\n15 March 2024")
plt.ylabel("Acceleration [G]")
plt.xlabel("Time [s]")
plt.savefig('IMU_Plot.png')
plt.show()
