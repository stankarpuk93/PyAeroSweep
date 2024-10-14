import numpy as np
from Core.Data                          import Data
from Components.Solver                  import Solver
from Components.Geometry                import Geometry
from Components.Geometry.Wing.Segment   import Segment
from Components.Mesh                    import Mesh

from Run_aerodynamic_analysis import run_aerodynamic_analysis



def Input_data():

    working_dir   = r"/home/doktorand/Software/PyAeroSweep-Stan-V3/PyAeroSweep/Test_Cases/Mesh_and_Run" 

# ------------------------------- SOLVER SETTINGS ----------------------------------------------------------- #
#

    Solver_settings = Solver()

    Solver_settings.working_dir = working_dir

    Solver_settings.name = 'SU2'                 # SU2 or Fluent

    # Solver dimensions
    # 2d   or 3d        for SU2 
    Solver_settings.dimensions = '2d'            

    # Only available for SU2 in 3D
    # defines half od the shape or a full shape analysis (Only symmetric works for now)
    Solver_settings.symmetric = True             

    # SST or SA for SU2
    Solver_settings.turbulence_model = 'SST'

    # Number of processors
    Solver_settings.processors = 7

    # Cauchy convergence criteria
    # Could be either LIFT or DRAG
    Solver_settings.monitor          = "LIFT"
    Solver_settings.tolerance        = 5e-7      
    Solver_settings.max_iterations   = 100
    Solver_settings.save_frequency   = 100

    # Warm start
    # YES or NO
    Solver_settings.warmstart = 'YES'

    # SU2 reference config file name which will be updated
    Solver_settings.config_file = 'Run_airfoil_template.cfg'



# ------------------------------- FREESTREAM SETTINGS ------------------------------------------------------- #
#
    Freestream = Data()
    Freestream.Mach             = np.array([0.21,0.25])
    Freestream.Altitude         = np.array([0,2000])                 # in meters
    Freestream.Angle_of_attack  = np.array([0.0,3.0,5.0])               # in degrees




# ------------------------------- GEOMETRY SETTINGS --------------------------------------------------------- #
#
    Geometry_data = Geometry()

    # Geometry to analyze
    ''' Could be airfoil or wing
        Airfoils can be parametrically defined using the PARSEC methods
        Wings are defined only using the existing CAD file and work either for
        straight tapered wings with or without the kink'''

    Geometry_data.type = 'airfoil'

    # Reference values
    Geometry_data.reference_values = {
        "Area"   : 2.62,
        "Length" : 2.62,
        "Depth"  : 1,
        "Point"  : [0.25*2.62,0,0]              # reference point about which the moment is taken
    }

    # Flag to use PARSEC parametrization or to use already existing airfoils
    Geometry_data.generate = False

    segment = Segment()
    segment.tag                = 'section_1'
    segment.chord              = 2.62
    segment.Airfoil.files      = {
        "upper" : "main_airfoil_upper_fixed.dat",
        "lower" : "main_airfoil_lower_fixed.dat"
    }

    segment.TrailingEdgeDevice.type = 'Slotted'
    segment.TrailingEdgeDevice.files = {
        "upper surface file" : "flap_airfoil_upper_fixed.dat",
        "lower surface file" : "flap_airfoil_lower_fixed.dat",
        "flap cutout"        : ["main_airfoil_cut1_fixed.dat", "main_airfoil_cut2_fixed.dat"]
    }

    segment.plot_airfoil = True

    Geometry_data.Segments.append(segment)



# ------------------------------- MESH SETTINGS ---------------------------------------------------------------- #
#

    Mesh_data = Mesh()

    # Flag to mesh the shape or not
    Mesh_data.meshing    = True

    # Mesh type
    Mesh_data.structured = False

    # Defined the OS in which Pointwise is used
    # WINDOWS or Linux
    Mesh_data.operating_system = 'Linux'

    # Pointwise tclsh directory used in Windows
    Mesh_data.tclsh_directory = r"/home/doktorand/Fidelity/Pointwise/Pointwise2022.1" 

    # Desired Y+ value
    Mesh_data.Yplus = 1.0

    # Define the Glyph template to use for meshing
    Mesh_data.glyph_file = "mesh_flapped_airfoil_SU2.glf"

    # Mesh filename for either the newly generated mesh or an eisting mesh
    Mesh_data.filename = 'su2meshEx.su2'

    # Define far-field 
    #   min x, max x
    #   min y, max y
    #   min z, max z (used only for 3D cases)
    Mesh_data.far_field = [[-60, 60], [-60 ,60]]


    Mesh_data.airfoil_mesh_settings = {
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
    Input.Solver        = Solver_settings
    Input.Freestream    = Freestream
    Input.Geometry      = Geometry_data
    Input.Mesh          = Mesh_data


    return Input

if __name__ == '__main__':

    Input = Input_data()
    run_aerodynamic_analysis(Input)
