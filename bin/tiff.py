#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 16:56:39 2023

@author: renettej
"""
# https://gis.stackexchange.com/questions/66367/display-a-georeferenced-dem-surface-in-3d-matplotlib
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
#from matplotlib.mlab import griddata
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from scipy.interpolate import griddata
from matplotlib import cm

import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.interpolate import griddata


# define a function
def func(x, y):
    return (x**2+y**2+(x*y)**2)**2


# generate grid data using mgrid
grid_x, grid_y = np.mgrid[0:1:1000j, 0:1:2000j]

# generate random points
rng = np.random.default_rng()
points = rng.random((1000, 2))
print(points.shape)


# generate values from the points generated above
values = func(points[:, 0], points[:, 1])

# generate grid data using the points and values above
grid_a = griddata(points, values, (grid_x, grid_y), method='cubic')

grid_b = griddata(points, values, (grid_x, grid_y), method='linear')

grid_c = griddata(points, values, (grid_x, grid_y), method='nearest')

'''
#visualizations
fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(func(grid_x,grid_y))
axs[0, 0].set_title("main")
axs[1, 0].plot(grid_a)
axs[1, 0].set_title("cubic")
axs[0, 1].plot(grid_b)
axs[0, 1].set_title("linear")
axs[1, 1].plot(grid_c)
axs[1, 1].set_title("nearest")
fig.tight_layout()

plt.savefig('graph.png')
#matplotlib.use('Agg')
#matplotlib.use('Qt5Agg')
'''
# Need to rerun testpegagus to verify this
filename = 'elevation_grid.csv'
dataset = pd.read_csv(filename, index_col=None,
                      names=['X', 'Y', 'Z'])
print(type(dataset))
print(dataset.head)
print(dataset.dtypes)

x = dataset['X'].to_numpy().reshape(-1, 1)
print(type(x))
print('x.shape: ', x.shape)
#x = np.float(x)
print(np.min(x))
print(np.max(x))
print(x[1] - x[0])
print(x[2] - x[1])



y = dataset['Y'].to_numpy().reshape(-1, 1)
print('y.shape: ', y.shape)
#y = np.float(y)
print(np.min(y))
print(np.max(y))
print(y[1] - y[0])
print(y[2] - y[1])

#z = dataset['Z'].to_numpy().astype(np.float).reshape(-1, 1)
z = dataset['Z'].to_numpy().reshape(-1, 1)
print('z.shape: ', z.shape)
count = 0
for i in range(z.shape[0]) :
    try:
        zint = int(z[i])
    except:
        z[i] = 0.0
        #print (i, x[i], y[i], z[i])
        count = count + 1
z = z.astype(float)
print (count)
#print(z[1] - z[0])
#print(z[2] - z[1])

xx = x[0]
count = 1
counts = []
for i in range(1, x.shape[0]):
    if x[i] == xx:
        counts.append(count)
        #print (i, count)
        xx = x[i]
        count = 1
    else:
        count += 1
counts.append(count)
print (len(counts))
print (np.unique(np.array(counts)))
print (len(counts)*np.unique(np.array(counts)))    

yy = y[0]
count = 1
counts = []
for i in range(1, y.shape[0]):
    if y[i] != yy:
        counts.append(count)
        #print (i, count)
        yy = y[i]
        count = 1
    else:
        count += 1
counts.append(count)
print (len(counts))
print (np.unique(np.array(counts)))     
print (len(counts)*np.unique(np.array(counts))) 

gridx = len(counts)
gridy = counts[0] 

xxx = x.reshape(gridx,gridy)
print ('xxx.shape: ', xxx.shape)
yyy = y.reshape(gridx,gridy)
zzz = z.reshape(gridx,gridy)

Nx = xxx.shape[0]
Ny = xxx.shape[1]

maxN = 64
step = int(np.maximum(1.0, np.maximum(np.floor(Nx/maxN), np.floor(Nx/maxN))))
print ('step: ', step)

# numpy slicing, start:stop:step
xxxx = xxx[1::step, 1::step][0:maxN,0:maxN]
print ('xxxx.shape: ', xxxx.shape)
yyyy = yyy[1::step, 1::step][0:maxN,0:maxN]
print ('yyyy.shape: ', yyyy.shape)
zzzz = zzz[1::step, 1::step][0:maxN,0:maxN]
print ('zzzz.shape: ', zzzz.shape)

grad = np.array(np.gradient(zzzz))
print ('grad.shape: ', grad.shape)
hpot = np.hypot(grad[0,:,:], grad[1,:,:])
slopes_angle = np.degrees(np.arctan(hpot))
print ('slope_angle.shape: ', slopes_angle.shape)


x = xxxx
y = yyyy
z = zzzz

fig = plt.figure()
ax = plt.figure().add_subplot(projection='3d')

u = grad[0,:,:]
v = grad[1,:,:]
#w = slopes_angle
w = np.ma.masked_where(slopes_angle >= 80.0, slopes_angle)

ax.quiver(x, y, z, u, v, w, length=.5, normalize=False)

plt.show()
plt.savefig('quiver.png')
