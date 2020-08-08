'''
This script is used to to demonstrate some of the primary functionalities of the ROSCO toolchain. 
All of these abilities are also shown in the Examples folder of the ROSCO toolbox.
'''

import os
import platform
import yaml
from ROSCO_toolbox import utilities, turbine, controller


# Command line call to run openfast or path to openfast 
if platform.system() == 'Windows':
    if platform.architecture()[0] == '32bit':
        openfast_call = os.path.join( os.path.dirname(os.path.realpath(__file__)), 'OpenFAST_executables', 'openfast_Win32.exe')
    else:
        openfast_call = os.path.join( os.path.dirname(os.path.realpath(__file__)), 'OpenFAST_executables', 'openfast_x64.exe')
elif platform.system() == 'Darwin':
    openfast_call = 'openfast'

# Load yaml file
parameter_filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'BAR_00', 'ServoData', 'BAR_00.yaml')
inps = yaml.safe_load(open(parameter_filename))
path_params = inps['path_params']
turbine_params = inps['turbine_params']
controller_params = inps['controller_params']

# Instantiate turbine, controller, and file processing classes
turb = turbine.Turbine(turbine_params)
cont = controller.Controller(controller_params)
file_processing = utilities.FileProcessing()
fast_io = utilities.FAST_IO()

# Load turbine data from OpenFAST and rotor performance text file
turb.load_from_fast(path_params['FAST_InputFile'], path_params['FAST_directory'], dev_branch=True)

# Tune controller
cont.tune_controller(turb)

# Write parameter input file
param_filename = 'OpenFAST_BAR_00_DISCON.IN'
param_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'BAR_00', param_filename)
file_processing.write_DISCON(turb, cont, param_file=param_file,
                             txt_filename=path_params['rotor_performance_filename'])

# Run OpenFAST
# --- May need to change openfast_call to use your desired openfast version
fast_io.run_openfast(path_params['FAST_directory'], fastcall=openfast_call,
                     fastfile=path_params['FAST_InputFile'], chdir=True)
