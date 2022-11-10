#This code takes an input file, which contains the strengths of the Bx, By, Bz, and Bmod fields and the time at which the data was taken at, and plots time against each of the field strengths (magnetic_field_plot_filename.png).
#To run this code, have your input file and code be in the same directory. Make sure you are in the same directory as the input file and code. Then, open a terminal window, and type python magnetic_field.py [name of input file] and hit return to run it
#Ex: if my input file is "file.txt", then I would type python magnetic_field-2d.py file.txt to run the code

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

input_file = sys.argv[1] #the name of the input file you specified
root = input_file[:-4]
root = root.replace(" ", "_")

t, bx, by, bz, bmod = np.loadtxt(input_file, skiprows=3, unpack=True) #loading in data

#assembling magnetic field data into a list
b_fields = [bx, by, bz, bmod]

#labels
b_field_names = ['$B_x$', '$B_y$', '$B_z$', '$B_{mod}$']
b_field_names_not_latex = ['Bx', 'By', 'Bz', 'Bmod']

#line styles for mean lines
b_styles = ['solid', 'dotted', 'dashed', 'dashdot']

#plotting each of the magnetic field data against time
for a in range(len(b_fields)):
    plt.plot(t, b_fields[a], label=b_field_names[a], linewidth=0.3)
#     plt.hlines(y=b_fields[a].mean(), xmin=np.min(t), xmax=np.max(t), linestyles='--')
 
#plotting averages of each magnetic field component. these are horizontal lines
for a in range(len(b_fields)):
    mean_list = np.linspace(b_fields[a].mean(), b_fields[a].mean(), len(t))
    plt.plot(t, mean_list, color='black', linestyle=b_styles[a])
    plt.text(((1.5*np.max(t)-np.max(t))/10) + np.max(t), b_fields[a].mean()-0.002, 'mean {} = {:.3f} ± {:.3f} mT'.format(b_field_names[a], b_fields[a].mean(), b_fields[a].std()), fontsize=6)

#miscellaneous plot labels
plt.title('Magnetic Field Components vs. Time, ' + root)
plt.xlabel('Time (s)')
plt.ylabel('Magnetic Field Strength (mT)')
plt.ylim(-0.1, 0.1)
plt.xlim(right=(1.5)*np.max(t))
plt.legend(ncol=len(b_fields)) #making legend horiztonal

#outputting plot
figname = 'magnetic_field_plot_' + root + '.png'
plt.savefig(figname, dpi=150)