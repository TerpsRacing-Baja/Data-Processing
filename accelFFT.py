import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

# accepting filename and interval as arguments, carving up cut CSV file for further processing. 
parser = argparse.ArgumentParser(description="Carve up RaceCapture CSV files")
parser.add_argument('filename')
parser.add_argument('start_interval', type=int)
parser.add_argument('end_interval', type=int)
parser.add_argument('accelComponent')
args = parser.parse_args()



# grabbing relevant cols on interval and cleaning unknown rows
df = pd.read_csv(args.filename)
df = df[df["Interval|\"ms\"|0|0|1"] >= args.start_interval]
df = df[df["Interval|\"ms\"|0|0|1"] <= args.end_interval]\
    .rename(columns={   "AccelX|\"G\"|-3.0|3.0|200": "AccelX",
                        "AccelY|\"G\"|-3.0|3.0|200": "AccelY",
                        "AccelZ|\"G\"|-3.0|3.0|200": "AccelZ",
                        })

df = df[["AccelX", "AccelY", "AccelZ"]]
df.dropna(
    axis=0,
    how='any',
    subset=None,
    inplace=True
)

# pulling out acceleration dataframes
accelX = df["AccelX"]
accelY = df["AccelY"]
accelZ = df["AccelZ"]

if args.accelComponent == 'x':
    arr = accelX.to_numpy()
if args.accelComponent == 'y':
    arr = accelY.to_numpy()
if args.accelComponent == 'z':
    arr = accelZ.to_numpy()

dt = 1                   # time step of 1
t = np.arange(0,len(arr), dt)   # Creating an array of time values 

fig,axs = plt.subplots(2,1) 
fig2 = plt.figure()

plt.sca(axs[0])
plt.plot(t, arr, color = 'g', linewidth = 2, label = 'Noisy') # plotting noisy acceleration vals
plt.ylim(min(arr),max(arr))
plt.legend()


n = len(t)
arrHat = np.fft.fft(arr, n)             # applying fourier transform on accelerations vals
PSD = arrHat * np.conj(arrHat) / n      # creating array of power values for y axis
freq = np.fft.fftfreq(len(arr), .005)   # creating frequency values for x axis

plt.sca(axs[1])
plt.stem(freq, PSD, label ='Noisy')     # plotting fourier transformed acceleration values on stem plot
plt.legend()


filterVal = float(input("Enter a filter value: "))  # Asking user for filter value and if they want a low or high pass filter. 
highOrLow = input("h for high pass, l for low pass: ")
if highOrLow == "h":
    indices = PSD > filterVal
if highOrLow == "l":
    indices = PSD < filterVal                
PSDclean = PSD * indices                # zeroing out values not in filter
arrHat = indices * arrHat               # zero out small fourier coeff in Y
ffilt = np.fft.ifft(arrHat)             # applying inverse FFT

plt.figure(fig2.number)
plt.plot(t, ffilt, color ='k', linewidth = 2, label = 'Filtered')     # plotting filtered data
plt.ylim(min(arr), max(arr))
plt.legend()
plt.show()







    










