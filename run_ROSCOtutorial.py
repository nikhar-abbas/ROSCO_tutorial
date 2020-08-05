'''
This script is used to to demonstrate some of the primary functionalities of the ROSCO toolchain. 
All of these abilities are also shown in the Examples folder of the ROSCO toolbox.
'''

import os
import yaml
from ROSCO_toolbox import utilities, turbine, controller


# Local definitions
openfast_call   = 'openfast_master' # Command line call to run openfast or path to openfast (e.g. '/Users/nabbas/Documents/openfast/install/bin/openfast')
dev_branch      = True              # Are you on the dev branch of OpenFAST?         


## -------------------------------------------- ##
#   Nothing should need to change from here on  ##
## -------------------------------------------- ##

# Define model paths
model_path = os.path.join(os.getcwd(), 'OpenFAST', 'IEA-15-240-RWT-Monopile')
model_fst = 'IEA-15-240-RWT-Monopile.fst'
rotperf_file = os.path.join(os.getcwd(), 'IEA-15-240-RWT', 'OpenFAST',
                            'IEA-15-240-RWT', 'Cp_Ct_Cq.IEA15MW.txt')

# Load yaml file
parameter_filename = os.path.join(model_path, 'ServoData', 'IEA15MW-Monopile.yaml')
inps = yaml.safe_load(open(parameter_filename))
path_params = inps['path_params']
turbine_params = inps['turbine_params']
controller_params = inps['controller_params']

# Update path parameters for this tutorial
path_params['FAST_directory'] = model_path
path_params['FAST_InputFile'] = model_fst
path_params['rotor_performance_filename'] = rotperf_file

# Instantiate turbine, controller, and file processing classes
turb = turbine.Turbine(turbine_params)
cont = controller.Controller(controller_params)
file_processing = utilities.FileProcessing()
fast_io = utilities.FAST_IO()

# Load turbine data from OpenFAST and rotor performance text file
turb.load_from_fast(path_params['FAST_InputFile'], path_params['FAST_directory'], rot_source='txt',
                    txt_filename=path_params['rotor_performance_filename'], dev_branch=dev_branch)

# Tune controller
cont.tune_controller(turb)

# Write parameter input file
# This must be named DISCON.IN to be seen by the compiled controller binary.
param_file = os.path.join(model_path, 'DISCON-Monopile.IN')
file_processing.write_DISCON(turb, cont, param_file=param_file,
                             txt_filename=path_params['rotor_performance_filename'])

# Run OpenFAST
# --- May need to change fastcall if you use a non-standard command to call openfast
fast_io.run_openfast(path_params['FAST_directory'], fastcall=openfast_call,
                     fastfile=path_params['FAST_InputFile'], chdir=True)
