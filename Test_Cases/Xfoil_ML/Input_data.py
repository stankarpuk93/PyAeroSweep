
import os
import numpy as np
from Core.Data                          import Data
from Components.Solver                  import Solver
from Components.Geometry                import Geometry
from Components.Geometry.Wing.Segment   import Segment
from Components.Mesh                    import Mesh

from Run_aerodynamic_analysis import run_aerodynamic_analysis


def Input_data():


# ------------------------------- SOLVER SETTINGS ----------------------------------------------------------- #
#

    Solver_settings = Solver()

    Solver_settings.working_dir = os.path.dirname(os.path.abspath(__file__))        # A standard line to get the file directory

    Solver_settings.name = 'Xfoil'                # SU2 or Xfoil

    Solver_settings.viscous = True                # Viscous or inviscid solutions

    Solver_settings.free_transition = False
    Solver_settings.x_transition    = [0.3, 0.3]

    # Convergence criteria 
    Solver_settings.max_iterations = 200

    Solver_settings.e_n = 9                       # The factor N for the e^N method


# ------------------------------- FREESTREAM SETTINGS ------------------------------------------------------- #
#
    Freestream = Data()
    Freestream.Mach             = np.array([0.1,0.2,0.4])
    Freestream.Altitude         = np.array([0,2000])                    # in meters
    Freestream.Angle_of_attack  = np.array([0.0,3.0,5.0,7.0])               # in degrees. 
                                                                        # For Xfoil, make sure to put equally spaced values



# ------------------------------- MESH SETTINGS ---------------------------------------------------------------- #
#

    Mesh_data = Mesh()

    # Flag to mesh the shape or not. In Xfoil, no classical CFD mesh is created. Therefore, False
    Mesh_data.meshing = False




# ------------------------------- GEOMETRY SETTINGS --------------------------------------------------------- #
#
    Geometry_data = Geometry()

    # Geometry to analyze
    ''' Only airfoils for Xfoil
        Airfoils can be parametrically defined using the PARSEC or CST methods'''

    # Reference values
    Geometry_data.reference_values = {
        "Length" : 2.62,
        "Point"  : [0.25*2.62,0,0]              # reference point about which the moment is taken
    }

    segment = Segment()
    segment.tag                = 'section_1'
    segment.spanwise_location  = 0 
    segment.chord              = 2.62
    segment.Airfoil.files      = {
        "upper" : "main_airfoil_upper_1.dat",        # Upper airfoil surface (used for Pointwise meshing)
        "lower" : "main_airfoil_lower_1.dat"         # Lower airfoil surface (used for Pointwise meshing)
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
                                    "yte upper" : 0.002,
                                    "yte lower" : -0.002
    }
    Geometry_data.Segments.append(segment)

    segment.plot_airfoil = True


# ------------------------------- MESH SETTINGS ---------------------------------------------------------------- #
#

    # In Xfoil, only airfoil surface panel distribution can be changed

    Mesh_data = Mesh()


    Mesh_data.airfoil_mesh_settings = {
        "clustering_coefficient" : 1.0,           # a spacing coefficient that defines LE and TE clustering          
        "LETE_spacing"           : 0.15,          # LE/TE panel density ratio
        "connector dimensions"   : 160,           # in this case, a total number of panel nodes in Xfoil
        "LE_spacing"             : 0.2,           # defines density at the leadinge edge 
        "refine_xc_top"          : [1, 1],        # defines a region where the mesh is refined. [1, 1] means 'disabled'
        "refine_xc_bottom"       : [1, 1]         # defines a region where the mesh is refined. [1, 1] means 'disabled'    
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
