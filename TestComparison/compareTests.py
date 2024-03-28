import argparse
import pandas as pd
import matplotlib.pyplot as plt

# Accepting two files for comparison and interval to compare
parser  = argparse.ArgumentParser(description="Carve up and accept two csv files")
parser.add_argument("filename1")
parser.add_argument("filename2")
parser.add_argument("start_interval", type = int)
parser.add_argument("end_interval", type = int)
args = parser.parse_args()

# grabbing relevant cols from both files and cleaning unknown rows
df1 = pd.read_csv(args.filename1)
df1 = df1[df1["Interval|\"ms\"|0|0|1"] >= args.start_interval]
df1= df1[df1["Interval|\"ms\"|0|0|1"] <= args.end_interval]\
    .rename(columns={"Interval|\"ms\"|0|0|1" : "Interval (ms)",
                        "Speed|\"mph\"|0.0|150.0|25": "Speed",})

df2 = pd.read_csv(args.filename2)
df2 = df2[df2["Interval|\"ms\"|0|0|1"] >= args.start_interval]
df2 = df2[df2["Interval|\"ms\"|0|0|1"] <= args.end_interval]\
    .rename(columns={"Interval|\"ms\"|0|0|1" : "Interval (ms)",
                        "Speed|\"mph\"|0.0|150.0|25": "Speed",})

df1 = df1[["Speed"]]
df1.dropna(
    axis=0,
    how='any',
    subset=None,
    inplace=True
)

df2 = df2[["Speed"]]
df2.dropna(
    axis=0,
    how='any',
    subset=None,
    inplace=True
)
                      
speed1 = df1["Speed"]
speed2 = df2["Speed"]

fig,axs = plt.subplots(2,1)

plt.sca(axs[0])
plt.plot(speed1, color = 'g', linewidth = 2) # plotting noisy acceleration vals

plt.sca(axs[1])
plt.plot(speed2, color = 'r', linewidth = 2) # plotting noisy acceleration vals

plt.show()




