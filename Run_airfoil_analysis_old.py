# Run_airfoil_analysis.py
# 
# Created:  Dec 2022, S. Karpuk
# Modified:


"""
The code runs the generation of an airfoil using the PARSEC method,
generates an airfoil mesh using Pointwise using an initially prepared glyph script,
and runs the airfoil analysis sweep using a given CFD package

Capabilities:
    1. Generation of PARSEC airfoils for clean and flapped configurations
    2. Airfoil automaitc meshing using Pointwise
    3. Execution of ANSYS Fluent or SU2 for given airfoils using RANS with available turbulence models

Options 1 to 3 can be used separately or together

Compatibility: 
    The tool is compatible for both Windows and Linux systems (needs further testing for bugs)

Prerequiseites:
    Installed Pointwise 

"""

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
import os
import subprocess
import numpy as np
from Input_data              import Input_data
from create_airfoil_and_flap import create_airfoil_and_flap 
from Fluent_sweeps           import main as Run_fluent
from SU2_sweeps              import main as Run_SU2


def run_airfoil_analysis(Input):

    '''Main function to run the analysis
    
        Inputs:
 


        Outputs:
           

        Assumptions:
            1. airfoil tip thickness is assumed 0.0025 from each side

    '''



    # Important directories and file names
    """PARSEC_flag   = True
    meshing_flag  = True                                                          # flag to mesh or skip the meshing part
    system        = "WINDOWS"
    tclsh_dir     = r"C:\Program Files (x86)\Pointwise\PointwiseV18.3R1\win64\bin"        # tclsh (UNIX) of Pointwise (Windows) directory (runs glyph on the background)
    working_dir   = r"D:\AE_software\PyAeroSweep\PyAeroSweep-main"                   # working directory
    glyph_file_cl = 'mesh_clean_airfoil_SU2.glf'                                  # Glyph script file - clean airfoil
    glyph_file_fl = 'mesh_flapped_airfoil_SU2.glf'                                # Glyph script file - flapped airfoil
    casefile      = 'airfoil_mesh.cas'                                            # Case file for Fluent (the name that will be created for Fluent)
    SU2_conf_file = 'Run_airfoil_template.cfg'#'Run_airfoil_template.cfg'         # SU2 config file which is used as a reference file
    SU2_mesh      = 'su2meshEx.su2'#'su2meshEx.su2'                               # SU2 mesh file
    #upper_airfoil_path = r"G:\TUBS\HiWi\Dr Karpuk\Version\AF_CFD_V1\main_airfoil_upper.dat"
    #lower_airfoil_path = r"G:\TUBS\HiWi\Dr Karpuk\Version\AF_CFD_V1\main_airfoil_lower.dat""""
    
    #--------------------------------------------------------------------------------------------------------------
      
    

    #--------------------------------------------------------------------------------------------------------------

    # CFD solver inputs
    
    #--------------------------------------------------------------------------------------------------------------
   
    '''
    Two Solver options are available:
        1. Fluent
        2. SU2
    '''
    Solver = 'SU2'

    # ANSYS Fluent parameters
    #---------------------------------
    if Solver == 'Fluent':
        Solver_dim          = '2ddp'   
        Time_type           = 'Steady'
        Solver_type         = 'pressure-based'                                   #   pressure-based density-based-implicit
        Solver_method       = 'SIMPLEC'
        turbulence_model    = 'kw-sst'                                           # K-ω Shear Stress Transport (KW-SST) turbulence model
        global_under_relax  = 0.5                                                # Global under-relaxation factor for all solver parameters     
        Courant_number      = 2.0                                                # Courant number (for density-based solvers)                                          
        num_proc            = 2                                                  # Number of processors
        save_freq           = 10
        conv_criteria       = 1e-5
        iterations          = 35000
        time_step           = 1e-4                                               # time step size for the transient solution
        Fluent_settings     = [Solver_dim, Solver_type, Solver_method, turbulence_model, global_under_relax, 
                                num_proc, save_freq, conv_criteria, iterations, Courant_number, Time_type, time_step]

    # SU2 parameters
    #------------------------------------------------------------
    elif Solver == 'SU2':                                                        # Works ofnly for steady cases and models prescribed in the reference config file
        Solver_dim          = '2d'                                               # SOlver dimension (2d or 3d)   
        symmetric           = True               
        turbulence_model    = 'SST'                                              # Shear Stress Transport (SST) turbulence model (combines the benefits of both, k-ε (k-epsilon) & k-ω (k-omega))
        num_proc            = 7                                                  # Number of processors
        save_freq           = 3000
        conv_criteria       = 5e-7
        iterations          = 50000  
        warmstart           = 'YES'                                              # Uses previous solutions in the sweep of data (currently valid for AoA sweeps only) 
        SU2_settings = [turbulence_model, num_proc, save_freq, conv_criteria, iterations, warmstart, system, symmetric]
 
    # Input sweeep data
    AoA_range   = np.array([0.0])                      # AoA range in degrees 0.0,1.0,2.0,3.0....
    # 0,3.0,6.0,8.0,10.0,12.0,13.0,14.0,15.0


    #-------------------------------------------------------------------------------------------------------------------------


    for i in range(len(Area)):
        Ref_values = [Area[i], Length[i], Depth, ref_point[0], ref_point[1], ref_point[2]]    
    
        # Run the airfoil generation script
        if PARSEC_flag is True:
                create_airfoil_and_flap(airfoil_data, flap_setting, flap_flag, droop_nose_flag, droop_nose_set)

                
        # Mesh the geometry
        if meshing_flag is True:

            if flap_flag is True: 

                # Update the Glyph script - Flapped Airfoil
                from glyph_updater_flapped  import update_glyph_script_fl   
                from mesh_pre_process       import update_glyph_flapped_data
                update_glyph_script_fl(glyph_file_fl, **update_glyph_flapped_data) 

            else:

                # Update the Glyph script - Clean Airfoil   
                from glyph_updater_clean    import update_glyph_script_cl
                from mesh_pre_process       import update_glyph_clean_data
                update_glyph_script_cl(glyph_file_cl, **update_glyph_clean_data)

            # Run Pointwise glyph script to gnerate the mesh
                if system == "WINDOWS":
                    if flap_flag is True:
                        full_glyph_path = working_dir + "\\" + glyph_file_fl 
                    else:
                        full_glyph_path = working_dir + "\\" + glyph_file_cl 
                    os.chdir(tclsh_dir)
                    subprocess.call(['tclsh ',full_glyph_path], stderr= None, stdin=subprocess.PIPE)    
                else:
                    if flap_flag is True:
                        full_glyph_path = working_dir + "/" + glyph_file_fl 
                    else:
                        full_glyph_path = working_dir + "/" + glyph_file_cl 
                    os.chdir(tclsh_dir)
                    subprocess.run('./pointwise ' + '-b ' + full_glyph_path, shell = True, stdin=subprocess.PIPE)

        # Run CFD solution
        if Solver == 'Fluent':
            Run_fluent(Alt_range,Mach_range,AoA_range,Fluent_settings,Ref_values,working_dir,casefile)
        elif Solver == 'SU2':
            Run_SU2(Solver_dim,Alt_range,Mach_range,AoA_range,SU2_settings,Ref_values,working_dir, SU2_conf_file, SU2_mesh)


    print("Analysis completed")


    return


if __name__ == '__main__':

    # Define airfoil sample inputs
    #--------------------------------------------------------------------------------------------------------------

        Input = Input_data()

        run_airfoil_analysis(Input)


#######################################################################################################


