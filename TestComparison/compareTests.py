import argparse
import pandas as pd
import matplotlib.pyplot as plt

# Accepting two files for comparison and interval to compare
parser  = argparse.ArgumentParser(description="Carve up and accept two csv files")
parser.add_argument("filename1")
parser.add_argument("filename2")
args = parser.parse_args()

# grabbing relevant cols from both files and cleaning unknown rows
df1 = pd.read_csv(args.filename1)
df1= df1.rename(columns={"Interval|\"ms\"|0|0|1" : "Interval (ms)",
                        "Speed|\"mph\"|0.0|150.0|25": "Speed",})

df2 = pd.read_csv(args.filename2)
df2 = df2.rename(columns={"Interval|\"ms\"|0|0|1" : "Interval (ms)",
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

#plotting values on graph and displaying them
fig,axs = plt.subplots(2,1)

plt.sca(axs[0])
plt.plot(speed1, color = 'g', linewidth = 2, label = "test1") 
plt.xlabel("Time (ms)")
plt.ylabel("Speed (mph)")
plt.title("Test1")


plt.sca(axs[1])
plt.plot(speed2, color = 'r', linewidth = 2, label = "test2") 
plt.xlabel("Time (ms)")
plt.ylabel("Speed (mph)")
plt.title("Test2")


plt.show()




