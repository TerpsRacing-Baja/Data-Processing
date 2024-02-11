#from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import pandas as pd
import csv
import time as time
#Author: Daniel Hancock
'''
WHAT TO DO NEXT:

- pull in data from accelerometer, long/lat/altitude, throttle switch
- make plot to visualize accelerometer data
- make plot to visualize positional(long/lat/alt), 3d if possible. for 3d follow code below, "quiver" function is not needed for this, quiver was to
        make a vector showing the gyroscope direction. Try to make a plot that generally draws out the graph if possible.
- Steps to pull data are written out below in line 55
- WHEN CHANGING WHICH FILE YOU ARE READING, YOU MUST CHANGE THE FILE NAME IN LINES 96 AND 97, THIS IS UNIQUE TO MY COMPUTER
- if you have any questions ask jason/current subteam leader or if need be contact me. Daniel Hancock- 443-796-6902

'''
#DO NOT TOUCH THESE, FOR GYROSCOPE ONLY
def unit_vector(vector):
    """ Returns the unit vector of the vector."""
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """Finds angle between two vectors"""
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def x_rotation(vector,theta):
    """Rotates 3-D vector around x-axis"""
    R = np.array([[1,0,0],[0,np.cos(theta),-np.sin(theta)],[0, np.sin(theta), np.cos(theta)]])
    return np.dot(R,vector)

def y_rotation(vector,theta):
    """Rotates 3-D vector around y-axis"""
    R = np.array([[np.cos(theta),0,np.sin(theta)],[0,1,0],[-np.sin(theta), 0, np.cos(theta)]])
    return np.dot(R,vector)

def z_rotation(vector,theta):
    """Rotates 3-D vector around z-axis"""
    R = np.array([[np.cos(theta), -np.sin(theta),0],[np.sin(theta), np.cos(theta),0],[0,0,1]])
    return np.dot(R,vector)

def update(back, point,xrot, yrot, zrot,graph):
    new_point = x_rotation(point, np.pi/3)
    new_back = x_rotation(back, np.pi/3)
    new_point = y_rotation(point, np.pi/3)
    new_back = y_rotation(back, np.pi/3)
    new_point = z_rotation(point, np.pi/3)
    new_back = z_rotation(back, np.pi/3)
    #graph.set_data(new_back[0],new_back[1],new_back[2],new_point[0],new_point[1],new_point[2])
    #graph.set_3d_properties(new_back[0],new_back[1],new_back[2],new_point[0],new_point[1],new_point[2])

#STEPS TO ADD MORE SENSORS FOR PROCESSING
'''
    FIRST:
        create array:
            ARRAYNAME = []
    
    SECOND:
        create if statement to pull info from racecapture csv file. PUT THIS IF STATEMENT IN   "for col in datalabels:" LOOP BELOW
    
        if 'BASIC NAME HERE(example: Analog1)' in col:
            NAME-list = datalabels['FULL COLUMN HEADDER HERE'].tolist()
            for i in NAME-list:
                change = str(i)
                if change == 'nan' or change == 'FULL COLUMN NAME HERE':
                    pass
                else:
                    ARRAYNAME.append(float(change))
    
        names to change in code above: (BASIC NAME HERE), (FULL COLUMN NAME HERE), (NAME-list), (ARRAYNAME)

    THIRD:
        convert data to desired unit
            HOW:    ARRAYNAME = [ (CONVERSION HERE) for x in ARRAYNAME]
'''
#DATA FRAMES TO COLLECT DATA FROM FILES
xdata = [] 
yawdata = []; rolldata = []; pitchdata = []
axdata = []; aydata = []; azdata = []
pitchlist = []; yawlist = []; rolllist = []
shaftrpm = []
fullThrottle = []
engineRPM = []
cvt_temp = []
SteerAngle = []
timeint = []

datalabels = pd.read_csv('C:/Users/farme/OneDrive/Documents/TerpsRacingRaceCaptureData/rc_4.csv')
dfdata = pd.read_csv('C:/Users/farme/OneDrive/Documents/TerpsRacingRaceCaptureData/rc_1.csv', header = 0)

for col in datalabels:
    #NOTE: interval loop takes in EVERY interval data point, not the interval between each data collection
    if 'Interval'in col:
        TIMELIST = datalabels['Interval|"ms"|0|0|1'].tolist()
        for i in TIMELIST:
            change = str(i)
            if change == 'nan' or change == 'Interval|"ms"|0|0|1':
                pass
            else:
                timeint.append(float(change))
    if 'Pitch'in col:
        PITCHLIST = datalabels['Pitch|"Deg/Sec"|-120|120|50'].tolist()
        for i in PITCHLIST:
            change = str(i)
            if change == 'nan' or change == 'Pitch|"Deg/Sec"|-120|120|50':
                pass
            else:
                pitchlist.append(float(change))


    if 'Yaw'in col:
        YAWLIST = datalabels['Yaw|"Deg/Sec"|-120|120|50'].tolist()
        for i in YAWLIST:
            change = str(i)
            if change == 'nan' or change == 'Yaw|"Deg/Sec"|-120|120|50':
                pass
            else:
                yawlist.append(float(change))
    if 'Roll'in col:
        ROLLLIST = datalabels['Roll|"Deg/Sec"|-120|120|50'].tolist()
        for i in ROLLLIST:
            change = str(i)
            if change == 'nan' or change == 'Roll|"Deg/Sec"|-120|120|50':
                pass
            else:
                rolllist.append(float(change))
    if 'Analog0' in col:
        throttlelist = datalabels['Analog0|""|0|5|50'].tolist()
        for i in throttlelist:
            print(i)
            change = str(i)
            if change == 'nan' or change == 'Analog0|""|0|5|50':
                pass
            else:
                fullThrottle.append(float(change))
    if 'Analog1' in col:
        shaftrpmlist = datalabels['Analog1|""|0|5|50'].tolist()
        for i in shaftrpmlist:
            change = str(i)
            if change == 'nan'or change == 'Analog1|""|0|5|50':
                pass
            else:
                shaftrpm.append(float(change))
    if 'Analog2' in col:
        cvttemplist = datalabels['Analog2|""|0|5|50'].tolist()
        for i in cvttemplist:
            change = str(i)
            if change == 'nan' or change == 'Analog2|""|0|5|50':
                pass
            else:
                cvt_temp.append(float(change))
    if 'Analog3' in col:
        steeranglelist = datalabels['Analog3|""|0|5|50'].tolist()
        for i in steeranglelist:
            change = str(i)
            if change == 'nan' or change == 'Analog3|""|0|5|50':
                pass
            else:
                SteerAngle.append(float(change))
    if 'RPM1' in col:
        engineRPMlist = datalabels['RPM3|""|0.0|10000.0|50'].tolist()
        for i in engineRPMlist:
            change = str(i)
            if change == 'nan' or change == 'RPM3|""|0.0|10000.0|50':
                pass
            else:
                engineRPM.append(float(change))  

print('Interval')
print(len(timeint))
print('pitch')
print(len(pitchlist))
#CONVERT TO RADIANS
yawlist = [x * np.pi/180 for x in yawlist]
rolllist = [x * np.pi/180 for x in rolllist]
pitchlist = [x * np.pi/180 for x in pitchlist]

#Equation below is derrived from testing the thermistor in a controlled enviroment
try:
    '''This try function checks if shaftrpm has any data values, if it is empty it will not graph, but continue the code'''
    shaftmph = [6.0213858333*x for x in shaftrpm] #CIRCUMFERENCE*ROTATIONS/SEC

    plt.figure()
    plt.plot(shaftmph, engineRPM)
    plt.title('CVT Efficiency Curve')
    plt.xlabel('Vehicle speed (MPH)')
    plt.ylabel('Engine Output RPM')
except:
    pass

try:
    '''This try function checks if cvt_temp has any data values, if it is empty it will not graph, but continue the code'''
        #Equation below is derrived from testing the thermistor in a controlled enviroment 
    cvt_temp = [ -(100/209)(100*x-298) for x in cvt_temp]

    plt.figure()
    plt.plot(timeint, cvt_temp)
    plt.title('CVT Temperature over Time')
    plt.xlabel('Tempurature (C)')
    plt.ylabel('Time (ms)')
except:
    pass


#GRAPHS ONLY PITCH
'''
NOTE: the length is hardcoded to match the number of data points
lenyaw = len(yawlist)
lenyaw1 = (np.linspace(0,1297,num = 1298))/16
print(lenyaw)
print(len(lenyaw1))
plt.plot(lenyaw1,yawdata)
plt.show()
'''



#PLOTS GYROSCOPE IN 3D GRAPH IN NEAR-REAL TIME

#INITIAL POINT
point = np.array([0, 4, 0]) #blue vector
back = np.array([0,-2,0])
pointr = np.array([2,0,0])
backr = np.array([-1,0,0])
pointg = np.array([0,0,2])
backg = np.array([0,0,-1])
N = len(rolllist)

plt.ion()
    
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
graph = ax.quiver(back[0],back[1],back[2],point[0],point[1],point[2],color = "b")

ax.set_xlabel('roll')
ax.set_ylabel('yaw')
ax.set_zlabel('pitch')
ax.set_xlim([-3,3])
ax.set_ylim([-3,3])
ax.set_zlim([-3,3])

###PLOTTING GYROSCOPE------------------------------------------------------------------------
'''NOTE:
    this plot is set up such that it simply replots every time, so as of right now you cannot change the angle at which you look at the graph'''
for i in range(N):
    ax = fig.add_subplot(projection='3d')
    plt.title("Gyroscope data")
    ax.set_xlabel('roll')
    ax.set_ylabel('yaw')
    ax.set_zlabel('pitch')
    ax.set_xlim([-3,3])
    ax.set_ylim([-3,3])
    ax.set_zlim([-3,3])

    yaw = yawlist[i]
    roll = rolllist[i]
    pitch = pitchlist[i]
    if (i == 0):
        #DIRECTION OF VEHICLE=================================
        pointx = x_rotation(point,yaw)
        pointy = y_rotation(pointx,roll)
        newpoint = z_rotation(pointy, pitch)
        backx = x_rotation(back,yaw)
        backy = y_rotation(back,roll)
        newback = z_rotation(backy, pitch)
        #LEFT TO RIGHT DIRECTION ============================================
        pointxr = x_rotation(pointr,yaw)
        pointyr = y_rotation(pointxr,roll)
        newpointr = z_rotation(pointyr, pitch)
        backxr = x_rotation(backr,yaw)
        backyr = y_rotation(backxr,roll)
        newbackr = z_rotation(backyr, pitch)
        #UP DOWN DIRECTION================================================
        pointxg = x_rotation(pointg,yaw)
        pointyg = y_rotation(pointxg,roll)
        newpointg = z_rotation(pointyg, pitch)
        backxg = x_rotation(backg,yaw)
        backyg = y_rotation(backxg,roll)
        newbackg = z_rotation(backyg, pitch)
    else:
        #DIRECTION OF VEHICLE=================================
        pointx = x_rotation(newpoint,yaw)
        pointy = y_rotation(pointx,roll)
        newpoint = z_rotation(pointy, pitch)
        backx = x_rotation(newback,yaw)
        backy = y_rotation(backx,roll)
        newback = z_rotation(backy, pitch)
        #LEFT TO RIGHT DIRECTION ============================================
        pointxr = x_rotation(newpointr,yaw)
        pointyr = y_rotation(pointxr,roll)
        newpointr = z_rotation(pointyr, pitch)
        backxr = x_rotation(newbackr,yaw)
        backyr = y_rotation(backxr,roll)
        newbackr = z_rotation(backyr, pitch)
        #UP DOWN DIRECTION================================================
        pointxg = x_rotation(newpointg,yaw)
        pointyg = y_rotation(pointxg,roll)
        newpointg = z_rotation(pointyg, pitch)
        backxg = x_rotation(newbackg,yaw)
        backyg = y_rotation(backxg,roll)
        newbackg = z_rotation(backyg, pitch)
    

    graphB = ax.quiver(newback[0],newback[1],newback[2],newpoint[0],newpoint[1],newpoint[2],color = "b")
    graphR = ax.quiver(newbackr[0],newbackr[1],newbackr[2],newpointr[0],newpointr[1],newpointr[2],color = "r")
    graphG = ax.quiver(newbackg[0],newbackg[1],newbackg[2],newpointg[0],newpointg[1],newpointg[2],color = "g")

    fig.canvas.flush_events()
    fig.show()
    time.sleep(0.013)
    fig.delaxes(ax)
plt.show()
fig.delaxes(ax)
plt.show()

