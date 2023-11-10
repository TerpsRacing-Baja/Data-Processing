
import matplotlib.pyplot as plt
import pandas as pd
import csv

#gyrodata = pd.read_csv('E:/rc_4.csv')
#df = gyrodata[['Yaw|"Deg/Sec"|-120|120|50', 'Pitch|"Deg/Sec"|-120|120|50', 'Roll|"Deg/Sec"|-120|120|50']]
#rolldata = df[2]
#yawdata = df[2]
#pitchdata = df[3]
#plt.plot(rolldata)
#plt.plot(yawdata)
#plt.plot(pitchdata)

xdata = [] 
yawdata = []
rolldata = []
pitchdata = []
axdata = []
aydata = []
azdata = []
with open('C:/Users/farme/OneDrive/Documents/TerpsRacingRaceCaptureData/rc_4.csv','r') as csvfile: 
    plots = csv.reader(csvfile, delimiter = ',') 
    for row in plots: 
        next(plots)
        if row[4] == '' or row[5] == '' or row[6] == '' or row[7] == '' or row[8] == '' or row[9] == '' or row[7] == 'Yaw|"Deg/Sec"|-120|120|50':
            pass
        else: 
            xdata.append(float(row[0]))
            aydata.append(float(row[4]))
            azdata.append(float(row[5]))
            axdata.append(float(row[6]))
            yawdata.append(float(row[7]))
            rolldata.append(float(row[8])) 
            pitchdata.append(float(row[9])) 

dfax = pd.DataFrame(axdata)
dfay = pd.DataFrame(aydata)
dfaz = pd.DataFrame(azdata)  
dfx = pd.DataFrame(xdata) 
dfyaw = pd.DataFrame(yawdata) 
dfroll = pd.DataFrame(rolldata) 
dfpitch = pd.DataFrame(pitchdata) 

#yaw.plot(kind='line', 
#        color='red')
#roll.plot(kind='line', 
#        color='green')
#pitch.plot(kind='line', 
#        color='blue')
plt.figure(1)
plt.plot(yawdata, label='yaw',color='red')
plt.plot( rolldata, label='roll',color='green')
plt.plot(pitchdata, label='yaw',color='blue')
plt.title('Yaw, Roll, and Pitch over Time')
plt.xlabel('Time')
plt.ylabel('Degrees')
plt.legend()

plt.figure(2)
plt.plot(dfax, label='Accel x',color='red')
plt.plot(dfay, label='Accel y',color='green')
plt.plot(dfaz, label='Accel y',color='blue')
plt.title('X, Y, and Z acceleration over Time')
plt.xlabel('Time')
plt.ylabel('unknown measurement unit')
plt.legend()
plt.show()
#plt.title('Yaw')
#print(dfx)