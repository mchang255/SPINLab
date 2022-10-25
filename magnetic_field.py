#This code takes an input file, which contains the strengths of the Bx, By, Bz, and Bmod fields and the time at which the data was taken at, and plots time against each of the field strengths (magnetic_field_plot.png). In addition, this code also takes the average of Bx, By, Bz, and Bmod field and outputs it to a separate file (b_average.txt)
#To run this code, have your input file and code be in the same directory. Make sure you are in the same directory as the input file and code. Then, open a terminal window, and type python magnetic_field.py [name of input file] and hit return to run it
#Ex: if my input file is "file.txt", then I would type python magnetic_field.py file.txt to run the code

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

input_file = sys.argv[1] #the name of the input file you specified

t, bx, by, bz, bmod = np.loadtxt(input_file, skiprows=3, unpack=True) #loading in data

#assembling magnetic field data into a list
b_fields = [bx, by, bz, bmod]

#labels
b_field_names = ['$B_x$', '$B_y$', '$B_z$', '$B_{mod}$']
b_field_names_not_latex = ['Bx', 'By', 'Bz', 'Bmod']

#plotting each of the magnetic field data against time
for a in range(len(b_fields)):
    plt.plot(t, b_fields[a], label=b_field_names[a])

#miscellaneous plot labels
plt.title('Magnetic Field Components vs. Time')
plt.xlabel('Time (s)')
plt.ylabel('Magnetic Field Strength (mT)')
plt.legend()

#outputting plot
plt.savefig('magnetic_field_plot.png', dpi=150)

#averaging components of magnetic field
b_average = []
for b in range(len(b_fields)):
    b_average.append(b_field_names_not_latex[b] + ' = ' + str(b_fields[b].mean()) + ' mT')

average_file = 'b_averages.txt'

#outputting file
np.savetxt(average_file, b_average, fmt='%s')
    
