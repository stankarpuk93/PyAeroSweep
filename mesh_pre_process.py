#mesh_pre_process.py

import numpy as np

'''Mesh pre-processing file

        Notes:
            1. define all paths with '/' both for Ubuntu and windows systems

    '''

#--------------------------------------------------------------------------------------------------------------

# Desired Y+
desired_Yplus = 1.0               # Replace with the desired Y+

# Desired Length
Length = np.array([2.62])         # Reference length in m   

#--------------------------------------------------------------------------------------------------------------

# Data required for mesh_clean_airfoil_SU2.glf
scaling_factor = np.array([Length[0],Length[0],Length[0]])
update_glyph_clean_data = {
        "upper_surface_filename": r"D:/AE_software/PyAeroSweep/PyAeroSweep-main/main_airfoil_upper.dat",
        "lower_surface_filename": r"D:/AE_software/PyAeroSweep/PyAeroSweep-main/main_airfoil_lower.dat",
        "connector_dimensions": [200, 200, 8],
        "begin_spacing" : "0.001",
        "end_spacing"   : "0.0005",
        "su2meshed_file": r"D:/AE_software/PyAeroSweep/PyAeroSweep-main/su2meshEx.su2",
        "run_iterations_1": "230",
        "run_iterations_2": "-1",
        "stop_at_height_1": "Off",
        "stop_at_height_2": "529",
        "scaling_factor": "{" + str(Length[0]) + ' ' + str(Length[0]) + ' ' + str(Length[0]) +"}"  # Include the calculated scaling factors here
    }

    #--------------------------------------------------------------------------------------------------------------
    
    # Data required for mesh_flapped_airfoil_SU2.glf
scaling_factors = np.array([Length[0], Length[0], Length[0]])
update_glyph_flapped_data = {
        "upper_surface_filename": r"G:\TUBS\HiWi\Dr Karpuk\Version\AF_CFD_V1\main_airfoil_upper.dat",
        "lower_surface_filename": r"G:\TUBS\HiWi\Dr Karpuk\Version\AF_CFD_V1\main_airfoil_lower.dat",
        "cut1_filename": r"G:\TUBS\HiWi\Dr Karpuk\Version\AF_CFD_V1\main_airfoil_cut1.dat",
        "cut2_filename": r"G:\TUBS\HiWi\Dr Karpuk\Version\AF_CFD_V1\main_airfoil_cut2.dat",
        "flap_airfoil_lower_filename": r"G:\TUBS\HiWi\Dr Karpuk\Version\AF_CFD_V1\flap_airfoil_lower.dat",
        "flap_airfoil_upper_filename": r"G:\TUBS\HiWi\Dr Karpuk\Version\AF_CFD_V1\flap_airfoil_upper.dat",
        "connector_dimensions": [200, 120, 150, 150, 70, 25, 8, 8],
        "spacing_127_130": "0.001",
        "spacing_137_140": "0.001",
        "spacing_146_149": "0.00050000000000000001",
        "spacing_156_159": "0.00050000000000000001", 
        "spacing_165_172": "0.001",  
        "spacing_178_184": "0.005", 
        "spacing_192_195": "0.001",
        "spacing_201_204": "0.00050000000000000001",
        "spacing_211_214": "0.00050000000000000001",
        "addPoint228": "{60 60 0}",
        "addPoint229": "{60 -60 0}",
        "addPoint245": "{-60 -60 0}",
        "addPoint255": "{-60 60 0}",
        "far_field_connector_dim": "20", 
        "addPoint_287": "{0.5 3 0}",
        "addPoint_288": "{0.5 0 0}",
        "EndAngle_289": "360 {0 0 1}",
        "addPoint_298": "{0.5 15 0}",
        "addPoint_299": "{0.5 0 0}",
        "EndAngle_300": "360 {0 0 1}",
        "node_to_connector_313": "100", 
        "scaling_anchor": "{0 0 0}",
        "scaling_factors": scaling_factors,  # Include the calculated scaling factors here
        "BoundaryDecay_359": "0.75",
        "BoundaryDecay_384": "0.85", 
        "maxlayers_430": "100", 
        "fulllayers_431": "60",
        "growthrate_432": "1.2", 
        "growthrate_433": "1.1", 
        "BoundaryDecay_435": "0.85",
        "su2meshed_file": r"G:\TUBS\HiWi\Dr Karpuk\Version\AF_CFD_V1\su2meshEx.su2",   
    }

#######################################################################################################