from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

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

#plt.set_data_3d(x, y, z)

point = np.array([0, 4, 0]) #blue vector
back = np.array([0,-2,0])
v = np.array([0,-2,0,0,4,0])
new_point = z_rotation(point, np.pi/3)
new_back = z_rotation(back, np.pi/3)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
plt.figure(1)
#ax.quiver(v[0],v[1],v[2],v[3],v[4],v[5],color = "g")
ax.quiver(back[0],back[1],back[2],point[0],point[1],point[2],color = "b")
ax.quiver(new_back[0],new_back[1],new_back[2],new_point[0],new_point[1],new_point[2],color = "red")

ax.set_xlabel('roll')
ax.set_ylabel('yaw')
ax.set_zlabel('pitch')
ax.set_xlim([-3,3])
ax.set_ylim([-3,3])
ax.set_zlim([-3,3])

plt.show()

