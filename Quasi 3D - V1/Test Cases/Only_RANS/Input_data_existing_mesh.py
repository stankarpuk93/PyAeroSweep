
import numpy as np
from Data  import Data


def Input_data_with_mesh():

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




# ------------------------------- MESH SETTINGS ---------------------------------------------------------------- #
#

    Mesh = Data()

    # Flag to mesh the shape or not
    Mesh.meshing    = False

    # Defined the OS in which Pointwise is used
    # WINDOWS or Linux
    Mesh.operating_system = 'Linux'

    # Mesh filename for either the newly generated mesh or an eisting mesh
    Mesh.filename = 'su2meshE_existing.su2'





# ----------------------------------------------------------------------------------------------------------------------------- #
#
    # Pack all inputs
    Input = Data()
    Input.Solver        = Solver
    Input.Freestream    = Freestream
    Input.Geometry      = Geometry
    Input.Mesh          = Mesh


    return Input