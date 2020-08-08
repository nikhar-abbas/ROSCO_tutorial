
# Python Modules
import os
import matplotlib.pyplot as plt 
import glob
# ROSCO toolbox modules 
from ROSCO_toolbox import utilities

# Instantiate fast_IO and FAST_Plots
fast_io = utilities.FAST_IO()
fast_pl = utilities.FAST_Plots()

# Define openfast directory and output filenames
openfast_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'BAR_00')
filenames = glob.glob(os.path.join(openfast_dir, '*.outb'))
outfiles = []
outfiles = [os.path.split(fname)[-1:][0] for fname in filenames]
print('Plotting results from {}'.format(outfiles[::-1]))

# Load output info and data
fast_out = fast_io.load_FAST_out(filenames[::-1], tmin=30)

#  Define Plot cases 
#  --- Comment,uncomment, create, and change these as desired...
cases = {}
cases['Baseline'] = ['Wind1VelX', 'BldPitch1', 'GenTq', 'RotSpeed', 'GenPwr', 'TwrBsMyt']

# Plot, woohoo!
fig, ax = fast_pl.plot_fast_out(cases, fast_out)
fig[0].tight_layout()
plt.show()