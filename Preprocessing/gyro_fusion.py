import imufusion
import matplotlib.pyplot as pyplot
import numpy as np
import pandas as pd
import sys
import os
import argparse

# define command line arguments
# expected format: python gyro_fusion.py WITH-sway-bar-accel-both-wheels-1.csv 14 11 -s
# first number represents the column position of gyroscopic data starting at 0
# the second represets the column position of acceleration data starting at 0
parser = argparse.ArgumentParser(description="Carve up RaceCapture CSV files")
parser.add_argument('filename')
parser.add_argument('gyro_data', type=int, default=-1)  # reminder the columns start at 0
parser.add_argument('accel_data', type=int, default=-1)
parser.add_argument('-s', '--show', action='store_true')  # Use action='store_true' for boolean flags
args = parser.parse_args()

if(args.gyro_data == -1 or args.accel_data == -1):
    print("Uh oh spagetti-o, you are missing arguments for gyro and/or accel data columns")
    exit


# ERIC XU CODE STARTS -------------------------------------------
data = np.genfromtxt(args.filename, delimiter=",", skip_header=1)

idx = data[:, 0]
timestamp_raw = idx - idx.min() # normalize indices to zero
timestamp_raw = timestamp_raw / 1000.0 # convert to float seconds (gross)
gyro_data_raw = data[:, args.gyro_data:args.gyro_data+3]
acceleration_data_raw = data[:, args.accel_data:args.accel_data+3]
# acceleration_data_raw[:, 2] -= 1

# Create and apply boolean masks to filter out NaN values
g_mask = ~np.isnan(gyro_data_raw).any(axis=1)
a_mask = ~np.isnan(acceleration_data_raw).any(axis=1)
idx = idx[g_mask]
timestamp = timestamp_raw[g_mask]
gyroscope = gyro_data_raw[g_mask]
accelerometer = acceleration_data_raw[a_mask]

# Plot sensor data
_, axes = pyplot.subplots(nrows=3, sharex=True)

axes[0].plot(timestamp, gyroscope[:, 0], "tab:red", label="X")
axes[0].plot(timestamp, gyroscope[:, 1], "tab:green", label="Y")
axes[0].plot(timestamp, gyroscope[:, 2], "tab:blue", label="Z")
axes[0].set_title("Gyroscope")
axes[0].set_ylabel("Degrees/s")
axes[0].grid()
axes[0].legend()

axes[1].plot(timestamp, accelerometer[:, 0], "tab:red", label="X")
axes[1].plot(timestamp, accelerometer[:, 1], "tab:green", label="Y")
axes[1].plot(timestamp, accelerometer[:, 2], "tab:blue", label="Z")
axes[1].set_title("Accelerometer")
axes[1].set_ylabel("g")
axes[1].grid()
axes[1].legend()

# Process sensor data
ahrs = imufusion.Ahrs()
euler = np.empty((len(timestamp), 3))

for index in range(len(timestamp)):
    ahrs.update_no_magnetometer(gyroscope[index], accelerometer[index], 1 / 100)  # 100 Hz sample rate
    euler[index] = ahrs.quaternion.to_euler()

# Plot Euler angles
axes[2].plot(timestamp, euler[:, 0], "tab:red", label="Roll")
axes[2].plot(timestamp, euler[:, 1], "tab:green", label="Pitch")
axes[2].plot(timestamp, euler[:, 2], "tab:blue", label="Yaw")
axes[2].set_title("Euler angles")
axes[2].set_xlabel("Seconds")
axes[2].set_ylabel("Degrees")
axes[2].grid()
axes[2].legend()

if (args.show):
    pyplot.show(block="no_block" not in sys.argv)  # don't block when script run by CI

# ERIC XU CODE ENDS ---------------------------------------------

# merge euler angles into original CSV and save
new_data = pd.DataFrame({"Interval|\"ms\"|0|0|1": list([int(x) for x in idx]),
                         'Euler Roll': list(euler[:, 0]),
                         'Euler Pitch': list(euler[:, 1]),
                         'Euler Yaw': list(euler[:, 2])},
                         columns = ["Interval|\"ms\"|0|0|1", 'Euler Roll', 'Euler Pitch', 'Euler Yaw'])
df = pd.read_csv(args.filename)
df = df.merge(new_data, how = 'left', on = "Interval|\"ms\"|0|0|1")
write_name = str(os.path.basename(args.filename) + '_' + 'withEULER.csv')
df.to_csv(write_name)