
import numpy as np
from Core.Data                          import Data
from Components.Solver                  import Solver
from Components.Geometry                import Geometry
from Components.Geometry.Wing.Segment   import Segment
from Components.Mesh                    import Mesh

from Run_aerodynamic_analysis import run_aerodynamic_analysis

def Input_data_3D_wing():

    working_dir   = r"/home/doktorand/Software/PyAeroSweep-Stan-V3/PyAeroSweep/Test_Cases/Full_3D_wing/Case2"  

# ------------------------------- SOLVER SETTINGS ----------------------------------------------------------- #
#

    Solver_settings = Solver()

    Solver_settings.working_dir = working_dir

    Solver_settings.name = 'SU2'                 # SU2 or Fluent

    # Solver dimensions
    # 2d   or 3d        for SU2 
    Solver_settings.dimensions = '3d'            

    # Only available for SU2 in 3D
    # defines half od the shape or a full shape analysis (Only symmetric works for now)
    Solver_settings.symmetric = True             

    # SST, SA, or Inviscid for SU2
    Solver_settings.turbulence_model = 'SST'

    # Number of processors
    Solver_settings.processors = 7

    # Cauchy convergence criteria
    # Could be either LIFT or DRAG
    Solver_settings.monitor          = "LIFT"
    Solver_settings.tolerance        = 5e-7
    Solver_settings.max_iterations   = 50000

    # Warm start
    # YES or NO
    Solver_settings.warmstart = 'YES'

    # SU2 reference config file name which will be updated
    Solver_settings.config_file = 'Wing_template.cfg'



# ------------------------------- FREESTREAM SETTINGS ------------------------------------------------------- #
#
    Freestream = Data()
    Freestream.Mach             = np.array([0.21])
    Freestream.Altitude         = np.array([0])                 # in meters
    Freestream.Angle_of_attack  = np.array([0.0])               # in degrees




# ------------------------------- GEOMETRY SETTINGS --------------------------------------------------------- #
#
    Geometry_data = Geometry()

    # Geometry to analyze
    ''' Could be airfoil or wing
        Airfoils can be parametrically defined using the PARSEC methods
        Wings are defined only using the existing CAD file and work either for
        straight tapered wings with or without the kink'''

    Geometry_data.type = 'wing'

    # Reference values
    Geometry_data.reference_values = {
        "Area"   : 2.62,
        "Length" : 2.62,
        "Depth"  : 1,
        "Point"  : [0.25*2.62,0,0]              # reference point about which the moment is taken
    }

    Geometry.filename  = "Wing_geometry"
    Geometry.format    = 'igs'

    # Saves in igs by default
    # Can also save in Tecplot of VTK formats
    Geometry.output_format = "Tecplot"

    # Flag to use PARSEC parametrization or to use already existing airfoils
    Geometry_data.PARSEC = True

    # Polynomial fit options
    # 2 - liner; 3 - quadratic; 4 - quatic
    Geometry_data.polynomial_fit = 2

    # Airfoil files are used either to write PARSEC-generated airfoil and then read by Pointwise or to read directly from them
    segment = Segment()
    segment.tag                = 'section_1'
    segment.spanwise_location  = 0 
    segment.chord              = 7.760
    segment.incidence          = 2 
    segment.dihedral           = 3 
    segment.leading_edge_sweep = 30 
    segment.Airfoil.files      = {
        "upper" : "main_airfoil_upper_1.dat",
        "lower" : "main_airfoil_lower_1.dat"
    }
    segment.Airfoil.PARSEC     = {
                                    "rle"        : 0.0084,                      # Main airfoil LE radius
                                    "x_pre"      : 0.458080577545180,           # x-location of the crest on the pressure side
                                    "y_pre"      : -0.04553160030118,           # y-location of the crest on the pressure side  
                                    "d2ydx2_pre" : 0.554845554794938,           # curvature of the crest on the pressure side  
                                    "th_pre"     : -9.649803736,                # trailing edge angle on the pressure side [deg]
                                    "x_suc"      : 0.46036604,                  # x-location of the crest on the suction side 
                                    "y_suc"      : 0.06302395539,               # y-location of the crest on the suction side
                                    "d2ydx2_suc" : -0.361421420,                # curvature of the crest on the suction side
                                    "th_suc"     : -12.391677695858,             # trailing edge angle on the suction side [deg]
                                    "yte upper"  : 0.002,
                                    "yte lower"  : -0.002             # trailing edge angle on the suction side [deg]
    }
    Geometry_data.Segments.append(segment)

    segment = Segment()
    segment.tag                = 'section_2'
    segment.spanwise_location  = 18 
    segment.chord              = 2.0
    segment.incidence          = -1 
    segment.dihedral           = 25 
    segment.rotate             = False
    segment.leading_edge_sweep = 45 
    segment.Airfoil.files      = {
        "upper" : "main_airfoil_upper_2.dat",
        "lower" : "main_airfoil_lower_2.dat"
    }
    segment.Airfoil.PARSEC     = {
                                    "rle"        : 0.0084,                      # Main airfoil LE radius
                                    "x_pre"      : 0.458080577545180,           # x-location of the crest on the pressure side
                                    "y_pre"      : -0.04553160030118,           # y-location of the crest on the pressure side  
                                    "d2ydx2_pre" : 0.554845554794938,           # curvature of the crest on the pressure side  
                                    "th_pre"     : -9.649803736,                # trailing edge angle on the pressure side [deg]
                                    "x_suc"      : 0.46036604,                  # x-location of the crest on the suction side 
                                    "y_suc"      : 0.06302395539,               # y-location of the crest on the suction side
                                    "d2ydx2_suc" : -0.361421420,                # curvature of the crest on the suction side
                                    "th_suc"     : -12.391677695858,             # trailing edge angle on the suction side [deg]
                                    "yte upper"  : 0.002,
                                    "yte lower"  : -0.002             # trailing edge angle on the suction side [deg]
    }
    Geometry_data.Segments.append(segment)  



# ------------------------------- MESH SETTINGS ---------------------------------------------------------------- #
#

    Mesh_data = Mesh()

    # Flag to mesh the shape or not
    Mesh_data.meshing = True

    # Mesh type
    Mesh_data.structured = True

    # Defined the OS in which Pointwise is used
    # WINDOWS or Linux
    Mesh_data.operating_system = 'Linux'

    # Pointwise tclsh directory used in Windows
    Mesh_data.tclsh_directory = r"/home/doktorand/Fidelity/Pointwise/Pointwise2022.1" 

    # Desired Y+ value
    Mesh_data.Yplus = 30.0

    # Define the Glyph template to use for meshing
    Mesh_data.glyph_file = "mesh_clean_wing_SU2.glf"

    # Mesh filename for either the newly generated mesh or an eisting mesh
    Mesh_data.filename = 'su2meshEx.su2'

    Mesh_data.pw_mesh_file = 'mesh_file.pw'

    Mesh_data.wing_mesh_settings = {
        "LE_spacing"             : 0.001,                       # Airfoil leading edge spacing
        "TE_spacing"             : 0.0005,                      # Airfoil trailing edge spacing
        "flap_cluster"           : 0.005,
        "connector dimensions"   : [200, 200, 8],     #         "connector_dimensions": [200, 120, 150, 150, 70, 25, 8, 8],
        "number of normal cells" : 230
    }

    # Define far-field 
    #   min x, max x
    #   min y, max y
    #   min z, max z (used only for 3D cases)
    Mesh_data.far_field = [[-60, 60], [-60, 60], [0, 60]]


    Mesh_data.global_surface_mesh_settings = {
            "Min boundary subdivisions"   : 10,
            "Max extents subdivisions"    : 300,
            "Curvature resolution angle"  : 15,
            "Max aspect ratio"            : 100,
            "Refinement factor"           : 1.15,
            "Boundary gap subdivisions"   : 3            
        }

    Mesh_data.trailing_edge_meshing_settings = {
            "Trailing edge mapping"      : False,
            "Trailing edge cells"        : 10,
            "Convex spacing growth rate" : 0.5,
            "Max aspect ratio"           : 100,
            "Spacing factor"             : 1
        }

    Mesh_data.boundary_layer_settings = {
            "Max layers"                    : 50,
            "Full layers"                   : 1,
            "Stop if full layers not met"   : True,
            "Allow incomplete layers"       : True,
            "Push attributes"               : True,
            "Skew criteria equiangle"       : 1,
            "Growth rate"                   : 1.15,
            "Max included angle"            : 170,
            "Final cell aspect ratio"       : 1.0,
            "Collision buffer"              : 2,
            "Centroid skewness"             : 0.8,
            "Size field decay"              : 0.75,
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

    Input = Input_data_3D_wing()
    run_aerodynamic_analysis(Input)