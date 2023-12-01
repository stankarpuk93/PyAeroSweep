
import numpy as np
from Data  import Data


def Input_data():

    working_dir   = r"G:/TUBS/HiWi/Dr Karpuk/PyAeroSweep-Stan-V2/Quasi 3D" 

# ------------------------------- SOLVER SETTINGS ----------------------------------------------------------- #
#

    Solver = Data()

    Solver.working_dir = working_dir

    Solver.name = 'SU2'                 # SU2 or Fluent

    # Solver dimensions
    # 2d   or 3d        for SU2 
    Solver.dimensions = '2d'            

    # Only available for SU2 in 3D
    # defines half od the shape or a full shape analysis (Only symmetric works for now)
    Solver.symmetric = True             

    # SST or SA for SU2
    Solver.turbulence_model = 'SST'

    # Number of processors
    Solver.processors = 7

    # Cauchy convergence criteria
    # Could be either LIFT or DRAG
    Solver.monitor          = "LIFT"
    Solver.tolerance        = 5e-7      
    Solver.max_iterations   = 100
    Solver.save_frequency   = 100

    # Warm start
    # YES or NO
    Solver.warmstart = 'YES'

    # SU2 reference config file name which will be updated
    Solver.config_file = 'Run_airfoil_template.cfg'



# ------------------------------- FREESTREAM SETTINGS ------------------------------------------------------- #
#
    Freestream = Data()
    Freestream.Mach             = np.array([0.21,0.25])
    Freestream.Altitude         = np.array([0,2000])                 # in meters
    Freestream.Angle_of_attack  = np.array([0.0,3.0,5.0])               # in degrees




# ------------------------------- GEOMETRY SETTINGS --------------------------------------------------------- #
#
    Geometry = Data()

    # Geometry to analyze
    ''' Could be airfoil or wing
        Airfoils can be parametrically defined using the PARSEC methods
        Wings are defined only using the existing CAD file and work either for
        straight tapered wings with or without the kink'''

    Geometry.type = 'airfoil'

    # Reference values
    Geometry.reference_values = {
        "Area"   : 2.62,
        "Length" : 2.62,
        "Depth"  : 1,
        "Point"  : [0.25*2.62,0,0]              # reference point about which the moment is taken
    }

    # Flag to use PARSEC parametrization or to use already existing airfoils
    Geometry.PARSEC = True

    # Airfoil files are used either to write PARSEC-generated airfoil and then read by Pointwise or to read directly from them
    Geometry.airfoil_files = {
        "upper" : "main_airfoil_upper.dat",
        "lower" : "main_airfoil_lower.dat"
    }


    # High-lift devices
    # Available only for 2d airfoil studies
    Geometry.PARSEC_airfoil = {
        "rle"        : 0.0084,                      # Main airfoil LE radius
        "x_pre"      : 0.458080577545180,           # x-location of the crest on the pressure side
        "y_pre"      : -0.04553160030118,           # y-location of the crest on the pressure side  
        "d2ydx2_pre" : 0.554845554794938,           # curvature of the crest on the pressure side  
        "th_pre"     : -9.649803736,                # trailing edge angle on the pressure side [deg]
        "x_suc"      : 0.46036604,                  # x-location of the crest on the suction side 
        "y_suc"      : 0.06302395539,               # y-location of the crest on the suction side
        "d2ydx2_suc" : -0.361421420,                # curvature of the crest on the suction side
        "th_suc"     : -12.391677695858             # trailing edge angle on the suction side [deg]
    }

    # Define a flap (Only the single-slotted fowler is currently available)
    Geometry.flap = False
    Geometry.PARSEC_flap = {
        "cf_c"       : 0.3,                         # flap chord ratio
        "ce_c"       : 0.3,                         # conical curve extent ratio wrt the flap chord length
        "csr_c"      : 0.85,                        # shroud chord ratio 
        "clip_ext"   : 0.05,                        # shroud lip extent ratio wrt the flap  
        "r_le_flap"  : 0.01,                        # flap leading edge radius
        "tc_shr_tip" : 0.003,                       # shroud tip thickness
        "w_conic"    : 0.5,                         # conical parameter for the suction side of the flap airfoil
        "delta_f"    : 25,                          # flap deflection [deg]   
        "x_gap"      : 0.01,                        # x-length gap from the shroud TE (positive value is moving the flap left)
        "y_gap"      : 0.005,                       # y-length gap from the shroud TE (positive value is moving the flap down)    
        "upper surface file" : "flap_airfoil_upper.dat",
        "lower surface file" : "flap_airfoil_lower.dat",
        "flap cutout"        : ["main_airfoil_cut1.dat", "main_airfoil_cut2.dat"]
    }   
 

    # Define a droop nose 
    Geometry.droop = False
    Geometry.PARSEC_droop = {
        "delta_s"    : 15,              # droop nose deflection [deg]
        "cs_c"       : 0.4,             # droop nose chord ratio
        "d_cs_up"    : 0.15,            # droop nose offset from the hinge on the upper surface 
        "d_cs_low"   : 0.38,            # shroud lip extent ratio wrt the flap  
        "k_Bez1"     : 0.2,                
        "k_Bez2"     : 0.5,
        "w_con_seal" : 0.5              # conical parameter for the droop nose seal
    }


# ------------------------------- MESH SETTINGS ---------------------------------------------------------------- #
#

    Mesh = Data()

    # Flag to mesh the shape or not
    Mesh.meshing    = True

    # Mesh type
    Mesh.structured = True

    # Defined the OS in which Pointwise is used
    # WINDOWS or Linux
    Mesh.operating_system = 'WINDOWS'

    # Pointwise tclsh directory used in Windows
    Mesh.tclsh_directory =  r"C:\Program Files\Cadence\PointwiseV18.6R1\win64\bin" 

    # Desired Y+ value
    Mesh.Yplus = 1.0

    # Define the Glyph template to use for meshing
    Mesh.glyph_file = "mesh_clean_airfoil_SU2.glf"

    # Mesh filename for either the newly generated mesh or an eisting mesh
    Mesh.filename = 'su2meshEx.su2'

    # Define far-field 
    Mesh.far_field = 100 * Geometry.reference_values["Length"]


    Mesh.airfoil_mesh_settings = {
        "LE_spacing"             : 0.001,                       # Airfoil leading edge spacing
        "TE_spacing"             : 0.0005,                      # Airfoil trailing edge spacing
        "flap_cluster"           : 0.005,
        "connector dimensions"   : [200, 200, 8],     #         "connector_dimensions": [200, 120, 150, 150, 70, 25, 8, 8],
        "number of normal cells" : 230
    }

    Mesh.airfoil_extrusion_settings = {
        "Extrusion_direction"            : '{-0 -0 -1}',                 # Direction of Extrusion - -ve Z Axis
        "Extrusion_distance"             : 100,                          # Airfoil extrusion - in mm
        "Extrusion_steps"                : 1,                            # Number of steps the extrusion is divided into
    }





# ----------------------------------------------------------------------------------------------------------------------------- #
#
    # Pack all inputs
    Input = Data()
    Input.Solver        = Solver
    Input.Freestream    = Freestream
    Input.Geometry      = Geometry
    Input.Mesh          = Mesh


    return Input