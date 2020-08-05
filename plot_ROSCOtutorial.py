
# Python Modules
import os
import matplotlib.pyplot as plt 
# ROSCO toolbox modules 
from ROSCO_toolbox import utilities

# Instantiate fast_IO
fast_io = utilities.FAST_IO()
fast_pl = utilities.FAST_Plots()

# Define openfast output filenames
# filenames = ["../Test_Cases/5MW_Land/5MW_Land.outb"]

# ---- Note: Could plot multiple cases, textfiles, and binaries...
openfast_dir = os.path.join(os.getcwd(), 'IEA-15-240-RWT', 'OpenFAST','IEA-15-240-RWT-Monopile')

filenames = [glob.glob(os.path.join(openfast_dir, '*.outb'))]

# Load output info and data
fast_out = fast_io.load_FAST_out(filenames)

#  Define Plot cases 
#  --- Comment,uncomment, create, and change these as desired...
cases = {}
cases['Baseline'] = ['Wind1VelX', 'BldPitch1', 'GenTq', 'RotSpeed', 'GenPwr']
cases['Rotor Performance'] = ['RtVAvgxh', 'RtTSR', 'RtAeroCp']

# Plot, woohoo!
fig, ax = fast_pl.plot_fast_out(cases, fast_out)
plt.show()
