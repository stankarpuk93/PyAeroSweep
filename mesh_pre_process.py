# mesh_pre_process.py
#
# Created: Oct 2023, S.Holenarsipura
# Modified: Oct 2023, S.Holenarsipura
#
# This script provides configuration data for preprocessing airfoil meshes using Glyph script.

# ----------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------

import numpy as np

# ----------------------------------------------------------------------
# Desired Y+ and Length
# ----------------------------------------------------------------------
# Desired Y+ value is required for mesh generation.
# You can change the value by modifying the `get_desired_Yplus` function.
# Length is the reference length of the airfoil.
# You can change the value by modifying the `get_length` function.

def get_desired_Yplus():
    """Returns the desired Y+ value."""
    return 1.0

desired_Yplus = get_desired_Yplus()

def get_length():
    """Returns the reference length of the airfoil."""
    return 2.62

Length = np.array([get_length()])

# ----------------------------------------------------------------------
# Altitude and Mach Ranges
# ----------------------------------------------------------------------
# Define the altitude and Mach number ranges for analysis.

# Mach_and_Alt
Alt_range   = np.array([0])             # Altitude range in meters
Mach_range  = np.array([0.21])          # Mach number range  0.4,0.5,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95

# ----------------------------------------------------------------------
# Scaling Factors
# ----------------------------------------------------------------------
# The scaling factors are used for data required in Glyph scripts.
# They depend on the reference length.


scaling_factors = np.array([Length[0], Length[0], Length[0]])
scaling_factors_str = "{" + " ".join(f"{x:.2f}" for x in scaling_factors) + "}"  # Change the brackets in the `scaling_factors` array from `[]` to `{}`.

# ----------------------------------------------------------------------
# Data for Glyph Script (mesh_clean_airfoil_SU2.glf)
# ----------------------------------------------------------------------
# This data is used for generating structured airfoil meshes WITHOUT FLAPS.

update_glyph_clean_data = {
    "upper_surface_filename": r'"G:/TUBS/HiWi/Dr Karpuk/Version/AF_CFD_V1/main_airfoil_upper.dat"',     # Path to the upper surface file
    "lower_surface_filename": r'"G:/TUBS/HiWi/Dr Karpuk/Version/AF_CFD_V1/main_airfoil_lower.dat"',     # Path to the lower surface file
    "connector_dimensions": [200, 200, 8],     # Dimensions for connectors
    "spacing_59_63": "0.001",                  # Spacing value for lines 59 to 63
    "spacing_68_71": "0.0005",                 # Spacing value for lines 68 to 71
    "su2meshed_file": r'"G:/TUBS/HiWi/Dr Karpuk/Version/AF_CFD_V1/su2meshEx.su2"',  # Path to the SU2 meshed file
    "run_iterations_1": "230",                 # Number of iterations for the first run
    "run_iterations_2": "-1",                  # Number of iterations for the second run
    "stop_at_height_1": "Off",                 # Option to stop at a specific height for the first run
    "stop_at_height_2": "529",                 # Height at which to stop for the second run
    "normal_marching_vector": "{-0 -0 -1}",    # Normal marching vector
    "scaling_anchor": "{0 0 0}",               # Anchor point for scaling
    "scaling_factors": scaling_factors_str     # Scaling factors for scaling the entities
}



# ----------------------------------------------------------------------
# Data for Glyph Script (mesh_flapped_airfoil_SU2.glf)
# ----------------------------------------------------------------------
# This data is used for generating structured airfoil meshes WITH FLAPS.
    

scaling_factors = np.array([Length[0], Length[0], Length[0]])
scaling_factors_str = "{" + " ".join(f"{x:.2f}" for x in scaling_factors) + "}"  # Change the brackets in the `scaling_factors` array from `[]` to `{}`.

update_glyph_flapped_data = {
    "upper_surface_filename": r'"G:/TUBS/HiWi/Dr Karpuk/Version/AF_CFD_V1/main_airfoil_upper.dat"',  # Path to the upper surface file
    "lower_surface_filename": r'"G:/TUBS/HiWi/Dr Karpuk/Version/AF_CFD_V1/main_airfoil_lower.dat"',  # Path to the lower surface file
    "cut1_filename": r'"G:/TUBS/HiWi/Dr Karpuk/Version/AF_CFD_V1/main_airfoil_cut1.dat"',  # Path to cut1 file
    "cut2_filename": r'"G:/TUBS/HiWi/Dr Karpuk/Version/AF_CFD_V1/main_airfoil_cut2.dat"',  # Path to cut2 file
    "flap_airfoil_lower_filename": r'"G:/TUBS/HiWi/Dr Karpuk/Version/AF_CFD_V1/flap_airfoil_lower.dat"',  # Path to the lower flap airfoil file
    "flap_airfoil_upper_filename": r'"G:/TUBS/HiWi/Dr Karpuk/Version/AF_CFD_V1/flap_airfoil_upper.dat"',  # Path to the upper flap airfoil file
    "connector_dimensions": [200, 120, 150, 150, 70, 25, 8, 8],   # Dimensions for connectors
    "spacing_127_130": "0.001",                                   # Spacing value for lines 127 to 130
    "spacing_137_140": "0.001",                                   # Spacing value for lines 137 to 140
    "spacing_146_149": "0.00050000000000000001",                  # Spacing value for lines 146 to 149
    "spacing_156_159": "0.00050000000000000001",                  # Spacing value for lines 156 to 159
    "spacing_165_172": "0.001",                                   # Spacing value for lines 165 to 172
    "spacing_178_184": "0.005",                                   # Spacing value for lines 178 to 184
    "spacing_192_195": "0.001",                                   # Spacing value for lines 192 to 195
    "spacing_201_204": "0.00050000000000000001",                  # Spacing value for lines 201 to 204
    "spacing_211_214": "0.00050000000000000001",                  # Spacing value for lines 211 to 214
    "addPoint228": "{60 60 0}",                                   # Coordinates for addPoint at line 228
    "addPoint229": "{60 -60 0}",                                  # Coordinates for addPoint at line 229
    "addPoint245": "{-60 -60 0}",                                 # Coordinates for addPoint at line 245
    "addPoint255": "{-60 60 0}",                                  # Coordinates for addPoint at line 255
    "far_field_connector_dim": "20",                              # Dimensions for the far-field connector
    "addPoint_287": "{0.5 3 0}",                                  # Coordinates for addPoint at line 287
    "addPoint_288": "{0.5 0 0}",                                  # Coordinates for addPoint at line 288
    "EndAngle_289": "360 {0 0 1}",                                # End angle for line 289
    "addPoint_298": "{0.5 15 0}",                                 # Coordinates for addPoint at line 298
    "addPoint_299": "{0.5 0 0}",                                  # Coordinates for addPoint at line 299
    "EndAngle_300": "360 {0 0 1}",                                # End angle for line 300
    "node_to_connector_313": "100",                               # Node to connector dimension
    "scaling_anchor": "{0 0 0}",                                  # Anchor point for scaling
    "scaling_factors": scaling_factors_str,                       # Scaling factors for scaling the entities
    "BoundaryDecay_359": "0.75",                                  # Boundary decay value for line 359
    "BoundaryDecay_384": "0.85",                                  # Boundary decay value for line 384
    "maxlayers_430": "100",                                       # Maximum layers for TRex at line 430
    "fulllayers_431": "60",                                       # Full layers for TRex at line 431
    "growthrate_432": "1.2",                                      # Growth rate for TRex at line 432
    "growthrate_433": "1.1",                                      # Growth rate for TRex at line 433
    "BoundaryDecay_435": "0.85",                                  # Boundary decay value for line 435
    "su2meshed_file": r'"G:/TUBS/HiWi/Dr Karpuk/Version/AF_CFD_V1/su2meshEx.su2"',  # Path to the SU2 meshed file
}


#######################################################################################################