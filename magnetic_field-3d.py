import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from tabulate import tabulate
import sys

def mag_curves(time, w, phi, a, offset): 
    y = a*np.sin(w*time - phi) + offset
    return y

def mag_func(w, phi, a, offset, func, times):
    guesses = [w, phi, a, offset]
    print(guesses)
    params_out, covar_out = opt.curve_fit(mag_curves, times, func, p0 = guesses) 
    return params_out, covar_out

input_file = sys.argv[1] #the name of the input file you specified
root = input_file[:-4]
root = root.replace(" ", "_")

t, bx, by, bz, bmod = np.loadtxt(input_file, skiprows=3, unpack=True) #loading in data

offset_mags = [bx, by] #fields that have offsets to them
titles = ['B_x', 'B_y']

for b in range(len(offset_mags)):
    params, covar = opt.curve_fit(mag_curves, t, offset_mags[b])
    
    w = params[0]
    phi = params[1]
    a = params[2]
    offset = params[3]
    
    if titles[b] == 'B_x':
        offset_x = offset
    elif titles[b] == 'B_y':
        offset_y = offset
    
    plt.figure(figsize=(10,8))
    
    plt.plot(t, offset_mags[b], label='Raw Data')
    plt.plot(t, mag_curves(t, *params), label='Fit Line (${} = {:.3f}\sin({:.3f}t - {:.3f}) + {:.3f}$)'.format(titles[b], a, w, phi, offset))
    
    plt.title('${}$'.format(titles[b]))
    plt.xlabel('Time (s)')
    plt.ylabel('Field Strength (mT)')
    plt.legend()
    
    plt.savefig(titles[b] + '_fit.png', dpi=150)
    
t_nogauss, bx_nogauss, by_nogauss, bz_nogauss, bmod_nogauss = np.loadtxt('tanksetup_magdown_Nov1st.txt', skiprows=3, unpack=True)

true_bx = bx_nogauss.mean() - offset_x
true_by = by_nogauss.mean() - offset_y
true_bz = bz_nogauss.mean()

#for 11/1/22
#23,488.6 nT, 4,848.1 nT, 39,655.5 nT, IGRF2020
earth_actual_x_igrf = 23488.6 * (1e-6)
earth_actual_y_igrf = 4848.1 * (1e-6)
earth_actual_z_igrf = -39655.5 * (1e-6)

fig = plt.figure(figsize=(12, 10))

ax = plt.axes(projection = '3d')

#setting axis limits
ax.set_xlim3d(0, 0.025)
ax.set_ylim3d(0, 0.01)
ax.set_zlim3d(0, -0.1)

#plotting vectors
ax.quiver(0, 0, 0, true_bx, true_by, true_bz, color='red', arrow_length_ratio=0.05, label='Lab') #lab
ax.quiver(0, 0, 0, earth_actual_x_igrf, earth_actual_y_igrf, earth_actual_z_igrf, color='green', arrow_length_ratio=0.05, label='Earth, IGRF') #igrf

#plotting a line in the z-direction so it will be easier to see how much in the z-direction the arrow extends to
ax.plot([true_bx, true_bx], [true_by, true_by], [0, true_bz], color='red', linestyle='--')
ax.plot([earth_actual_x_igrf, earth_actual_x_igrf], [earth_actual_y_igrf, earth_actual_y_igrf], [0, earth_actual_z_igrf], color='green', linestyle='--')

#writing the coordinates of the vector next to the arrowhead for each vector
ax.text(true_bx, true_by, true_bz, '({:.3f}, {:.3f}, {:.3f})'.format(true_bx, true_by, true_bz), fontsize=9, color='red')
ax.text(earth_actual_x_igrf, earth_actual_y_igrf, earth_actual_z_igrf, '({:.3f}, {:.3f}, {:.3f})'.format(earth_actual_x_igrf, earth_actual_y_igrf, earth_actual_z_igrf), fontsize=9, color='green')

#labels
ax.set_title('Earth\'s Magnetic Field, Nov. 1')
ax.set_xlabel('$B_x$ (mT), +N | -S', labelpad=10)
ax.set_ylabel('$B_y$ (mT), +E | -W', labelpad=10)
ax.set_zlabel('$B_z$ (mT), +D | -U', labelpad=10)
ax.legend()

plt.savefig('mag_field_3d_vector.png', dpi=150)

#outputting data to table
with open('earth-lab_comparison.txt', 'w') as f:
    f.write(tabulate([['Lab-Measured', true_bx, true_by, true_bz], ['Actual, IGRF', earth_actual_x_igrf, earth_actual_y_igrf, earth_actual_z_igrf]], headers=['Magnetic Field (Nov 1.)', 'B_x (mT)', 'B_y (mT)', 'B_z (mT)']))