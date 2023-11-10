#from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import pandas as pd
import csv
import time as time
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
xdata = [] 
yawdata = []
rolldata = []
pitchdata = []
axdata = []
aydata = []
azdata = []
with open('C:/Users/farme/OneDrive/Documents/TerpsRacingRaceCaptureData/rc_1.csv','r') as csvfile: 
    plots = csv.reader(csvfile, delimiter = ',') 
    for row in plots: 
        #next(plots)
        if row[4] == '' or row[5] == '' or row[6] == '' or row[8] == '' or row[9] == '' or row[10] == '' or row[8] == 'Yaw|"Deg/Sec"|-120|120|50' or row[8] == 'Pitch|"Deg/Sec"|-120|120|50' or row[8] == 'Roll|"Deg/Sec"|-120|120|50':
            pass
        else: 
            xdata.append(float(row[0]))
            #aydata.append(float(row[4]))
            #azdata.append(float(row[5]))
            #axdata.append(float(row[6]))
            yawdata.append(float(row[8]))
            pitchdata.append(float(row[9])) 
            rolldata.append(float(row[10])) 

#CONVERT TO RADIANS
yawdata = [x * np.pi/180 for x in yawdata]
rolldata = [x * np.pi/180 for x in rolldata]
pitchdata = [x * np.pi/180 for x in pitchdata]
'''
lenpitch = len(pitchdata)
lenpitch1 = (np.linspace(0,1297,num = 1298))/16
print(lenpitch)
print(len(lenpitch1))
plt.plot(lenpitch1,pitchdata)
plt.show()
'''
#CREATES DATAFRAMES
dfax = pd.DataFrame(axdata)
dfay = pd.DataFrame(aydata)
dfaz = pd.DataFrame(azdata)  
dfx = pd.DataFrame(xdata) 
dfyaw = pd.DataFrame(yawdata) 
dfroll = pd.DataFrame(rolldata) 
dfpitch = pd.DataFrame(pitchdata) 


#INITIAL POINT
point = np.array([0, 4, 0]) #blue vector
back = np.array([0,-2,0])
pointr = np.array([2,0,0])
backr = np.array([-1,0,0])
pointg = np.array([0,0,2])
backg = np.array([0,0,-1])
N = len(rolldata)

plt.ion()
    

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
#ax.quiver(v[0],v[1],v[2],v[3],v[4],v[5],color = "g")
graph = ax.quiver(back[0],back[1],back[2],point[0],point[1],point[2],color = "b")
#graph = ax.quiver(new_back[0],new_back[1],new_back[2],new_point[0],new_point[1],new_point[2],color = "red")

ax.set_xlabel('roll')
ax.set_ylabel('yaw')
ax.set_zlabel('pitch')
ax.set_xlim([-3,3])
ax.set_ylim([-3,3])
ax.set_zlim([-3,3])

###PLOTTING GYROSCOPE------------------------------------------------------------------------
for i in range(N):
    ax = fig.add_subplot(projection='3d')
    plt.title("Gyroscope data")
    ax.set_xlabel('roll')
    ax.set_ylabel('yaw')
    ax.set_zlabel('pitch')
    ax.set_xlim([-3,3])
    ax.set_ylim([-3,3])
    ax.set_zlim([-3,3])

    yaw = yawdata[i]
    roll = rolldata[i]
    pitch = pitchdata[i]
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
    time.sleep(0.0013)
    fig.delaxes(ax)
plt.show()

#print out values of each angle
