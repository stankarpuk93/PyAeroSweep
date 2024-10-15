
import numpy as np
from Core.Data                          import Data
from Components.Solver                  import Solver
from Components.Geometry                import Geometry
from Components.Geometry.Wing.Segment   import Segment
from Components.Mesh                    import Mesh

from Run_aerodynamic_analysis import run_aerodynamic_analysis

def Input_data():

    working_dir   = r"/home/doktorand/Hiwi_Narunat/PyAeroSweep/Test_Cases/Flapped_airfoil_full"  

# ------------------------------- SOLVER SETTINGS ----------------------------------------------------------- #
#

    Solver_settings = Solver()

    Solver_settings.working_dir = working_dir
    Solver_settings.output_dir = working_dir + "/output_PARSEC"

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
    Freestream.Mach             = np.array([0.21])
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
    Geometry_data.generate = True

    segment = Segment()
    segment.tag                = 'section_1'
    segment.chord              = 2.62
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
                                    "th_suc"     : -12.391677695858,            # trailing edge angle on the suction side [deg]
                                    "yte upper"  : 0.002,
                                    "yte lower"  : -0.002
    }

    segment.TrailingEdgeDevice.type = 'Slotted'
    segment.TrailingEdgeDevice.PARSEC = {
        "cf_c"       : 0.3,                         # flap chord ratio
        "ce_c"       : 0.3,                         # conical curve extent ratio wrt the flap chord length
        "csr_c"      : 0.85,                        # shroud chord ratio 
        "clip_ext"   : 0.05,                        # shroud lip extent ratio wrt the flap  
        "r_le_flap"  : 0.01,                        # flap leading edge radius
        "tc_shr_tip" : 0.003,                       # shroud tip thickness
        "w_conic"    : 0.5,                         # conical parameter for the suction side of the flap airfoil
        "delta_f"    : 40,                          # flap deflection [deg]   
        "x_gap"      : 0.01,                        # x-length gap from the shroud TE (positive value is moving the flap left)
        "y_gap"      : 0.005,                       # y-length gap from the shroud TE (positive value is moving the flap down)    
    }  

    segment.TrailingEdgeDevice.files = {
        "upper surface file" : "flap_airfoil_upper.dat",
        "lower surface file" : "flap_airfoil_lower.dat",
        "flap cutout"        : ["main_airfoil_cut1.dat", "main_airfoil_cut2.dat"]
    }

    segment.LeadingEdgeDevice.type   = 'Droop'
    segment.LeadingEdgeDevice.PARSEC = {
        "delta_s"    : 15,              # droop nose deflection [deg]
        "cs_c"       : 0.10,             # droop nose chord ratio
        "d_cs_up"    : 0.03,            # droop nose offset from the hinge on the upper surface 
        "d_cs_low"   : 0.03,            # shroud lip extent ratio wrt the flap  
        "w_con_seal" : 1.0              # conical parameter for the droop nose seal
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
    Mesh_data.operating_system = 'Unix'

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
        "near-field boundary decay 1"    : 0.85,
        "Initial_trex_layer_scaler"      : 1
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
