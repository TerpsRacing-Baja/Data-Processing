import imufusion
import matplotlib.pyplot as pyplot
import numpy as np
import pandas as pd
import sys
import os
import argparse

# define command line arguments
parser = argparse.ArgumentParser(description="Carve up RaceCapture CSV files")
parser.add_argument('filename')
parser.add_argument('-s', '--show', type=bool, default=False)
args = parser.parse_args()

# ERIC XU CODE STARTS -------------------------------------------
# Import sensor data
data = np.genfromtxt(args.filename, delimiter=",", skip_header=1)

idx = data[:, 0]
t = idx - idx.min() # normalize indices to zero
t = t / 1000.0 # convert to float seconds (gross)
g = data[:, 14:17]
a = data[:, 11:14]

# Create and apply boolean masks to filter out NaN values
g_mask = ~np.isnan(g).any(axis=1)
a_mask = ~np.isnan(a).any(axis=1)
idx = idx[g_mask]
timestamp = t[g_mask]
gyroscope = g[g_mask]
accelerometer = a[a_mask]

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