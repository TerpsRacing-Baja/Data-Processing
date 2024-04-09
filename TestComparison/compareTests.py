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
                        "Speed|\"mph\"|0.0|150.0|25": "Speed",
                         "Analog7|\"Volts\"|0.0|5.0|200": "CVT Temp",})

df2 = pd.read_csv(args.filename2)
df2 = df2.rename(columns={"Interval|\"ms\"|0|0|1" : "Interval (ms)",
                        "Speed|\"mph\"|0.0|150.0|25": "Speed",
                        "Analog7|\"Volts\"|0.0|5.0|200": "CVT Temp", })

df1 = df1[["Speed", "CVT Temp"]]
df1.dropna(
    axis=0,
    how='any',
    subset=None,
    inplace=True
)

df2 = df2[["Speed", "CVT Temp"]]
df2.dropna(
    axis=0,
    how='any',
    subset=None,
    inplace=True
)
                      
speed1 = df1["Speed"]
speed2 = df2["Speed"]

cvt1 = df1["CVT Temp"]
cvt1.transform(lambda x: -(100/209)*(100*x-298))
cvt2 = df2["CVT Temp"]
cvt2.transform(lambda x: -(100/209)*(100*x-298))

 




#plotting values on graph and displaying them
fig,axs = plt.subplots(2,2)


axs[0,0].plot(cvt1, color = 'g', linewidth = 2, label = "test1") 
axs[0,0].set_title('CVT Test 1')
axs[0,0].set_xlabel('time (ms)')

axs[0,1].plot(cvt2, color = 'r', linewidth = 2, label = "test1") 
axs[0,1].set_title('CVT Test 2')
axs[0,1].set_xlabel('time (ms)')

axs[1,0].plot(speed1, color = 'b', linewidth = 2, label = "test1") 
axs[1,0].set_title('Speed Test 1')
axs[1,0].set_xlabel('time (ms)')
axs[1,0].set_ylabel('speed(mph)')

axs[1,1].plot(speed2, color = 'y', linewidth = 2, label = "test1") 
axs[1,1].set_title('Speed Test 2')
axs[1,1].set_xlabel('time (ms)')
axs[1,1].set_ylabel('speed(mph)')







plt.show()




