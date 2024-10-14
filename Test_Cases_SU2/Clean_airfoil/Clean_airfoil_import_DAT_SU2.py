
import numpy as np
import yaml
import os
import sys

# Point to upstream python Packages
# Extend PythonPath to import modules from parent directories
child_dir = os.path.dirname(__file__)
parent_dir1 = os.path.abspath(os.path.join(child_dir, '..'))
parent_dir2 = os.path.abspath(os.path.join(parent_dir1, '..'))
parent_dir3 = os.path.abspath(os.path.join(parent_dir2, '..'))
sys.path.append(parent_dir3)


from Core.Data                          import Data
from Components.Solver                  import Solver
from Components.Geometry                import Geometry
from Components.Geometry.Wing.Segment   import Segment
from Components.Mesh                    import Mesh

from Run_aerodynamic_analysis import run_aerodynamic_analysis

# Load systemspecific config
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)

def Input_data():

    # get location location of input and .glf and .cfg file
    working_dir   = os.path.dirname(__file__)

    # Define output folder location
    output_dir_global = config['OutputDirectory']
    # Define case output folder name
    case_output_dir_name = 'Clean_airfoil_import_DAT_SU2_out'
    # Define Case output directory
    output_dir = output_dir_global + '/' + case_output_dir_name

# ------------------------------- SOLVER SETTINGS ----------------------------------------------------------- #
#

    Solver_settings = Solver()

    Solver_settings.working_dir = working_dir
    Solver_settings.output_dir= output_dir

    Solver_settings.name = 'SU2'                 # SU2 or Fluent or TAU

    # Solver dimensions
    # 2d   or 3d        for SU2 
    Solver_settings.dimensions = '2d'            

    # Only available for SU2 in 3D
    # defines half od the shape or a full shape analysis (Only symmetric works for now)
    Solver_settings.symmetric = True             

    # SST or SA for SU2
    Solver_settings.turbulence_model = 'SST'

    # Number of processors
    Solver_settings.processors = config['UtilisedCpuCores']

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
    Freestream.Altitude         = np.array([0])                 # in meters
    Freestream.Angle_of_attack  = np.array([3.0])               # in degrees




# ------------------------------- GEOMETRY SETTINGS --------------------------------------------------------- #
#
    Geometry_data = Geometry()

    airfoil_file_path = r"/home/christoffer/Data/Airfoil_geometry_files/section3.dat"

    # Geometry to analyze

    Geometry_data.type = 'airfoil'

    # Reference values
    Geometry_data.reference_values = {
        "Area"   : 2.62,
        "Length" : 2.62,
        "Depth"  : 1,
        "Point"  : [0.25*2.62,0,0]              # reference point about which the moment is taken
    }

    # Import coordinates from .dat file
    datax = np.loadtxt(airfoil_file_path,skiprows=1 ,usecols=0, dtype=float) #skiprows to reject first row
    datay = np.loadtxt(airfoil_file_path,skiprows=1 ,usecols=1, dtype=float) #skiprows to reject first row

    segment = Segment()
    segment.tag                = 'section_1'
    segment.chord              = 2.62
    segment.Airfoil.files      = {
        "upper" : "main_airfoil_upper_1.dat",
        "lower" : "main_airfoil_lower_1.dat"

    }
    segment.Airfoil.DAT = {
                    "datax" :datax,                   
                    "datay" :datay,    
}
    
    # print(segment.Airfoil.DAT['upper'])
    # print(segment.Airfoil.DAT['lower'])
    # quit()
    Geometry_data.Segments.append(segment)

    segment.plot_airfoil = True


# ------------------------------- MESH SETTINGS ---------------------------------------------------------------- #
#

    Mesh_data = Mesh()

    # Flag to mesh the shape or not
    Mesh_data.meshing    = True

    # Mesh type
    Mesh_data.structured = True

    # Defined the OS in which Pointwise is used
    # WINDOWS or Linux
    Mesh_data.operating_system = config['MeshOperatingsystem']

    # Pointwise tclsh directory used in Windows
    Mesh_data.tclsh_directory =  config['PointwisePath']

    # Desired Y+ value
    Mesh_data.Yplus = 1.0

    # Define the Glyph template to use for meshing
    Mesh_data.glyph_file = "mesh_clean_airfoil_SU2.glf"

    # Mesh filename for either the newly generated mesh or an eisting mesh
    Mesh_data.filename = 'su2meshEx.su2'

    # Define far-field 
    Mesh_data.far_field = 100 * Geometry_data.reference_values["Length"]


    Mesh_data.airfoil_mesh_settings = {
        "LE_spacing"             : 0.001,                       # Airfoil leading edge spacing
        "TE_spacing"             : 0.0005,                      # Airfoil trailing edge spacing
        "flap_cluster"           : 0.005,
        "connector dimensions"   : [200, 200, 8],     #         "connector_dimensions": [200, 120, 150, 150, 70, 25, 8, 8],
        "number of normal cells" : 230
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