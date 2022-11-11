from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import os

names = np.loadtxt('list_of_files.txt', dtype=str, unpack=True) #unpacking names of files from list

times = []
bx_gauss = []
by_gauss = []
bz_gauss = []
bmod_gauss = []

bx_no_gauss = []
by_no_gauss = []
bz_no_gauss = []
bmod_no_gauss = []

for a in range(len(names)): #loading in files from list
    if 'gauss' in names[a]: #gauss chamber files
        t, bx, by, bz, bmod = np.loadtxt(names[a], skiprows=3, unpack=True)
        bx_gauss.append(bx)
        by_gauss.append(by)
        bz_gauss.append(bz)
        bmod_gauss.append(bmod)
        if a == 0:
            times.append(t)
    else: #no gauss chamber file
        t, bx, by, bz, bmod = np.loadtxt(names[a], skiprows=3, unpack=True)
        bx_no_gauss.append(bx)
        by_no_gauss.append(by)
        bz_no_gauss.append(bz)
        bmod_no_gauss.append(bmod)
        if a == 0:
            times.append(t)
        
bx_gauss = np.array(bx_gauss)
by_gauss = np.array(by_gauss)
bz_gauss = np.array(bz_gauss)

#averaging the gauss files as there are multiple of them
bx_gauss_avg = np.average(bx_gauss, axis=0)
by_gauss_avg = np.average(by_gauss, axis=0)
bz_gauss_avg = np.average(bz_gauss, axis=0)

#averaging gauss files to a single value
bx_gauss_mean = bx_gauss_avg.mean()
by_gauss_mean = by_gauss_avg.mean()
bz_gauss_mean = bz_gauss_avg.mean()

#averaging no gauss chamber files to a single value
bx_no_gauss_mean = np.array(bx_no_gauss).mean()
by_no_gauss_mean = np.array(by_no_gauss).mean()
bz_no_gauss_mean = np.array(bz_no_gauss).mean()

#getting Earth's magnetic field by subtracting out the average probe data in the gauss chamber from the average no gauss values
bx_earth = bx_no_gauss_mean - bx_gauss_mean
by_earth = by_no_gauss_mean - by_gauss_mean
bz_earth = bz_no_gauss_mean - bz_gauss_mean

#plotting figure in 3D
#y is facing west, x is facing north, z is vertical

#23,490.8 nT (N-W), 4,843.0 nT (E-W), 39,634.4 nT (D-U), for 10/27/22, wmm
# earth_actual_x = 23490.8 * (1e-6)
# earth_actual_y = 4843.0 * (1e-6)
# earth_actual_z = -39634.4  * (1e-6)

#for 11/1/22
#23,490.2 nT, 4,842.4 nT, 39,633.2 nT, wmm
earth_actual_x_wmm = 23490.2 * (1e-6)
earth_actual_y_wmm = 4842.4 * (1e-6)
earth_actual_z_wmm = -39633.2 * (1e-6)

#23,488.6 nT, 4,848.1 nT, 39,655.5 nT, IGRF2020
earth_actual_x_igrf = 23488.6 * (1e-6)
earth_actual_y_igrf = 4848.1 * (1e-6)
earth_actual_z_igrf = -39655.5 * (1e-6)

print('B_y is {}'.format(by_no_gauss_mean))
print('The background noise for B_y is {}'.format(by_gauss_mean))

fig = plt.figure()

ax = plt.axes(projection = '3d')

#setting axis limits
x_fields = abs(np.array([bx_earth, earth_actual_x_wmm, earth_actual_x_igrf]))
y_fields = abs(np.array([by_earth, earth_actual_y_wmm, earth_actual_y_igrf]))
z_fields = abs(np.array([bz_earth, earth_actual_z_wmm, earth_actual_z_igrf]))

ax.set_xlim3d(0, np.max(x_fields))
ax.set_ylim3d(0, np.max(y_fields))
ax.set_zlim3d(0, -np.max(z_fields))

# ax.set_xlim3d(0, bx_earth)
# ax.set_ylim3d(0, by_earth)
# ax.set_zlim3d(0, bz_earth)
# ax.set_xlim3d(0, earth_actual_x)
# ax.set_ylim3d(0, earth_actual_y)
# ax.set_zlim3d(0, earth_actual_z)

# if abs(bx_earth) >= abs(earth_actual_x):
#     ax.set_xlim3d(0, bx_earth)
# else:
#     ax.set_xlim3d(0, earth_actual_x)
    
# if abs(by_earth) >= abs(earth_actual_y):
#     ax.set_ylim3d(0, by_earth)
# else:
#     ax.set_ylim3d(0, earth_actual_y)
    
# if abs(bz_earth) >= abs(earth_actual_z):
#     ax.set_zlim3d(0, bz_earth)
# else:
#     ax.set_zlim3d(0, earth_actual_z)
    
# ax.set_xlim3d(0, 1)
# ax.set_ylim3d(0, 1)
# ax.set_zlim3d(0, 1)

#plotting vectors
ax.quiver(0, 0, 0, bx_earth, by_earth, bz_earth, color='red', arrow_length_ratio=0.05, label='Lab')
ax.quiver(0, 0, 0, earth_actual_x_wmm, earth_actual_y_wmm, earth_actual_z_wmm, arrow_length_ratio=0.05, label='Earth, WMM')
ax.quiver(0, 0, 0, earth_actual_x_igrf, earth_actual_y_igrf, earth_actual_z_igrf, color='green', arrow_length_ratio=0.05, label='Earth, IGRF')

#plotting a line in the z-direction so it will be easier to see how much in the z-direction the arrow extends to
ax.plot([bx_earth, bx_earth], [by_earth, by_earth], [0, bz_earth], color='red', linestyle='--')
ax.plot([earth_actual_x_wmm, earth_actual_x_wmm], [earth_actual_y_wmm, earth_actual_y_wmm], [0, earth_actual_z_wmm], color='steelblue', linestyle='--')
ax.plot([earth_actual_x_igrf, earth_actual_x_igrf], [earth_actual_y_igrf, earth_actual_y_igrf], [0, earth_actual_z_igrf], color='green', linestyle='--')

ax.set_title('Earth\'s Magnetic Field')
ax.set_xlabel('$B_x$ (mT)', labelpad=10)
ax.set_ylabel('$B_y$ (mT)', labelpad=10)
ax.set_zlabel('$B_z$ (mT)', labelpad=10)
ax.legend()

plt.savefig('mag_field_3d_vector.png', dpi=150)

# earth = [earth_actual_x, earth_actual_y, earth_actual_z]
# lab = [bx_earth, by_earth, bz_earth]

# data = list(zip(earth, lab))

# top='Actual Earth Magnetic Field, Lab-Measured Magnetic Field'
# np.savetxt('earth-lab_comparison.txt', data, delimiter=', ', header=top, fmt='%s')

#outputting data into a table
from tabulate import tabulate

with open('earth-lab_comparison.txt', 'w') as f:
    f.write(tabulate([['Lab-Measured', bx_earth, by_earth, bz_earth], ['Actual, WMM', earth_actual_x_wmm, earth_actual_y_wmm, earth_actual_z_wmm], ['Actual, IGRF', earth_actual_x_igrf, earth_actual_y_igrf, earth_actual_z_igrf]], headers=['Magnetic Field', 'B_x (mT)', 'B_y (mT)', 'B_z (mT)']))


#Fourier transform (still figuring this part out)
#fft
# all_files = os.listdir()
# for b in range(len(all_files)):
#     if 'rotation' in all_files[b]:
#         t, bx, by, bz, bmod = np.loadtxt(all_files[b], skiprows=3, unpack=True)
#         bx_net = np.array(bx) - bx_earth
#         by_net = np.array(by) - by_earth
#         bz_net = np.array(bz) - bz_earth
        
#         freq = np.fft.fft(bx_net)
        
#         plt.plot(bx_net, freq)
        
# t, bx, by, bz, bmod = np.loadtxt('tanksetup_rotation_10rpm_01_0deg.txt', skiprows=3, unpack=True)
# bx_net = np.array(bx) - bx_earth
# by_net = np.array(by) - by_earth
# bz_net = np.array(bz) - bz_earth

# freq_bx = np.fft.fft(bx_net)
# freq_by = np.fft.fft(by_net)
# freq_bz = np.fft.fft(bz_net)

# fig = plt.figure()

# plt.plot(t, freq_bx)
# plt.plot(t, freq_by)
# plt.plot(t, freq_bz)

# plt.show()
