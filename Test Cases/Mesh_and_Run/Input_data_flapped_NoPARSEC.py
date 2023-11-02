
import numpy as np
from Data  import Data


def Input_data_flapped_NoPARSEC():

    working_dir   = r"/home/doktorand/Software/PyAeroSweep-Stan-V2/" 

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
    Geometry.PARSEC = False

    # Airfoil files are used either to write PARSEC-generated airfoil and then read by Pointwise or to read directly from them
    Geometry.airfoil_files = {
        "upper" : "main_airfoil_upper_fixed.dat",
        "lower" : "main_airfoil_lower_fixed.dat"
    }


    # Define a flap (Only the single-slotted fowler is currently available)
    Geometry.flap = True
    
    Geometry.flap_files = {
        "upper surface file" : "flap_airfoil_upper_fixed.dat",
        "lower surface file" : "flap_airfoil_lower_fixed.dat",
        "flap cutout"        : ["main_airfoil_cut1_fixed.dat", "main_airfoil_cut2_fixed.dat"]
    }

    # Define a droop nose 
    Geometry.droop = False


# ------------------------------- MESH SETTINGS ---------------------------------------------------------------- #
#

    Mesh = Data()

    # Flag to mesh the shape or not
    Mesh.meshing    = True

    # Mesh type
    Mesh.structured = False

    # Defined the OS in which Pointwise is used
    # WINDOWS or Linux
    Mesh.operating_system = 'Linux'

    # Pointwise tclsh directory used in Windows
    Mesh.tclsh_directory = r"/home/doktorand/Fidelity/Pointwise/Pointwise2022.1" 

    # Desired Y+ value
    Mesh.Yplus = 1.0

    # Define the Glyph template to use for meshing
    Mesh.glyph_file = "mesh_flapped_airfoil_SU2.glf"

    # Mesh filename for either the newly generated mesh or an eisting mesh
    Mesh.filename = 'su2meshEx.su2'

    # Define far-field 
    #   min x, max x
    #   min y, max y
    #   min z, max z (used only for 3D cases)
    Mesh.far_field = [[-60, 60], [-60 ,60]]


    Mesh.airfoil_mesh_settings = {
        "LE_spacing"                     : 0.001,                               # Airfoil leading edge spacing
        "TE_spacing"                     : 0.0005,                              # Airfoil trailing edge spacing
        "LE_flap_spacing"                : 0.001,
        "TE_flap_spacing"                : 0.0005,
        "flap_cut_cluster"               : 0.005,                               # Cluster at the flap cutout corner
        "connector dimensions"           : [200, 120, 150, 150, 70, 25, 8, 8],  #   
        "near-field refinement radius 1" : 9,
        "near-field refinement radius 2" : 45,
        "near-field nodes"               : 100,
        "far-field connectors"           : 20,
        "Max TREX layers"                : 100,
        "near-field boundary decay 0"    : 0.85,
        "Full TREX layers"               : 60,
        "TREX growth rate"               : 1.1,
        "near-field boundary decay 2"    : 0.75,
        "near-field boundary decay 1"    : 0.85
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