import csv
import matplotlib.pyplot as plt


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

# Example usage:
file_path = 'rpm_data.csv'  # Change this to your CSV file path
time, rpm = import_data_from_csv(file_path)


plt.plot(time, rpm)
plt.title("RPM Data for PWM = 2044 us\n22 March 2024")
plt.ylabel("RPMS")
plt.xlabel("Time [s]")
plt.savefig('RPM_Plot.png')
plt.show()
