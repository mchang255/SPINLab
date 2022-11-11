# SPINLab

Welcome to the page where all the code that is used in UCLA's SPINLab is published! Very subject to changes.

Description of programs in the repository:
CURRENT
magnetic_field-3d.py - This code takes This code takes an input file, which contains the strengths of the Bx, By, Bz, and Bmod fields and the time at which the data was taken at, and specifically for the Bx and By fields, they plotted and fitted with sine curve. We use the following equation to fit the curve:

$B = A \sin{(\omega t - \phi} + C$

The parameter C is very important. This represents the vertical offset of the data. We subtract the offsets for Bx and By from our averaged Bx and By data respectively. Then we plot a vector of Bx, By, Bz representing the lab data and a vector from NOAA IGRFP representing the real life data in 3D. NOTE: This data is not generalized, meaning it only works for specific file inputs. We might try to generalize it in the future

magnetic_field.py - This code takes an input file, which contains the strengths of the Bx, By, Bz, and Bmod fields and the time at which the data was taken at, and plots time against each of the field strengths (magnetic_field_plot.png). In addition, this code also takes the averages of Bx, By, Bz, and Bmod fields and outputs them to a separate file (b_average.txt). WHY THIS CODE IS IMPORTANT: It is used for measuring the three-axis magnetic field in our experiments (see link below for more on what SPINLab does). We also use this code to cancel out the background field, so that we know what magnetic field we have generated in our experiments.

data.txt - the input file that is mentioned in the magnetic_field.py description.

To run all Python programs, open a terminal window and type "python name_of_program.py name_of_input_file.txt."

For more info: https://spinlab.epss.ucla.edu/
