import csv
import matplotlib.pyplot as plt

def plot_data(csv_file):
    # Lists to store data
    time_data = []
    rpm_data = []
    omega_data = []

    # Read CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        # Skip first two lines
        next(reader)
        next(reader)
        # Read each row
        for row in reader:
            # Extract data
            time_data.append(float(row[0]))
            rpm_data.append(float(row[1]))
            omega_data.append(float(row[2]))

    # Plotting
    plt.figure(1)
    plt.plot(time_data, rpm_data, label='RPM')
    
    plt.xlabel('Time [s]')
    plt.ylabel('RPMs')
    plt.title('RPMs vs Sleep Time')
    plt.legend()

    plt.figure(2)
    plt.plot(time_data, omega_data, label='omega')
    plt.xlabel('Time [s]')
    plt.ylabel('omega [rad/s]')
    plt.title('omega vs Sleep Time')
    plt.show()

# Example usage
csv_file = 'rpm_data.csv'  # Change this to your CSV file
plot_data(csv_file)
