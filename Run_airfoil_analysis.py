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
from create_airfoil_and_flap import create_airfoil_and_flap 
from Fluent_sweeps           import main as Run_fluent
from SU2_sweeps              import main as Run_SU2





def run_airfoil_analysis(airfoil_data, flap_setting, flap_flag, droop_nose_flag, droop_nose_set):

    '''Main function to run the analysis
    
        Inputs:
            airfoil_data.rle          Main airfoil LE radius
                         x_pre        x-location of the crest on the pressure side
                         y_pre        y-location of the crest on the pressure side
                         d2ydx2_pre   curvature of the crest on the pressure side
                         th_pre       trailing edge angle on the pressure side [deg]
                         x_suc        x-location of the crest on the suction side        
                         y_suc        y-location of the crest on the suction side    
                         d2ydx2_suc   curvature of the crest on the suction side
                         th_suc       trailing edge angle on the suction side [deg]

                         cf_c         flap chord ratio
                         ce_c         conical curve extent ratio wrt the flap chord length
                         csr_c        shroud chord ratio
                         clip_ext     shroud lip extent ratio wrt the airfoil
                         r_le_flap    flap leading edge radius
                         tc_shr_tip   shroud tip thickness
                         w_conic      conical parameter for the suction side of the flap airfoil

                         delta_f      flap deflection [deg]
                         x_gap        x-length gap from the shroud TE (positive value is moving the flap left)
                         y_gap        y-length gap from the shroud TE (positive value is moving the flap down)    

            flap_flag                 flag to compute the flap airfoil
            droop_nose_flag           flag to create a droop nose 


        Outputs:
           

        Assumptions:
            1. airfoil tip thickness is assumed 0.0025 from each side

    '''


    # Important directories and file names
    PARSEC_flag   = True
    meshing_flag  = True                                                         # flag to mesh or skip the meshing part
    system        = "Linux"
    tclsh_dir     = r"/home/doktorand/Fidelity/Pointwise/Pointwise2022.1"        # tclsh (UNIX) of Pointwise (Linux) directory (runs glyph on the background)
    working_dir   = r"/home/doktorand/SE2A/HLFC_AeroOpt2D/Hi_Fi_CFD_HiLift/TestCase"            # working directory
    glyph_file    = 'mesh_clean_airfoil_SU2.glf'                                            # Glyph script file
    casefile      = 'airfoil_mesh.cas'                                                # Case file for Fluent (the name that will be created for Fluent)
    SU2_conf_file = 'Run_airfoil_template.cfg'#'Run_airfoil_template.cfg'                                  # SU2 config file which is used as a reference file
    SU2_mesh      = 'su2meshEx.su2'#'su2meshEx.su2'                                             # SU2 mesh file


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
        turbulence_model    = 'kw-sst'
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
        turbulence_model    = 'SST'
        num_proc            = 7                                                  # Number of processors
        save_freq           = 3000
        conv_criteria       = 5e-7
        iterations          = 50000  
        warmstart           = 'YES'                                              # Uses previous solutions in the sweep of data (currently valid for AoA sweeps only) 
        SU2_settings = [turbulence_model, num_proc, save_freq, conv_criteria, iterations, warmstart, system, symmetric]
 
    # Input sweeep data
    Alt_range   = np.array([0])                                                 # Altitude range in meters
    Mach_range  = np.array([0.21])                                               # Mach number range  0.4,0.5,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95
    AoA_range   = np.array([0,3.0,6.0,8.0,10.0,12.0,13.0,14.0,15.0])                                    # AoA range in degrees  ,1.0,2.0,3.0
    # 0.0,3.0,6.0,8.0,9.0,10.0,11.0
    # Input airfoil reference values (make sure the glyph values are changed manually)
    Area            = np.array([2.62])                                                         # Reference Area in sq m
    Length          = np.array([2.62])                                                         # Reference length in m   
    Depth           = 1                                                         # Reference depth (span) in m
    ref_point       = [0.25*Length,0,0]                                                # Reference coordinate


    #-------------------------------------------------------------------------------------------------------------------------
    for i in range(len(Area)):
        Ref_values = [Area[i], Length[i], Depth, ref_point[0], ref_point[1], ref_point[2]]    

        if PARSEC_flag is True:
            # Run the airfoil generation script
            create_airfoil_and_flap(airfoil_data, flap_setting, flap_flag, droop_nose_flag, droop_nose_set)
    
        if meshing_flag is True:
            # Run Pointwise glyph script to gnerate the mesh
            if system == "Unix":
                full_glyph_path = working_dir + "\\" + glyph_file 
                os.chdir(tclsh_dir)
                subprocess.call(['tclsh ',full_glyph_path], stderr= None, stdin=subprocess.PIPE)    
            else:
                full_glyph_path = working_dir + "/" + glyph_file 
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

    # Analysis flags
    droop_nose_flag = True          #  A flag to include or exclude a droop nose
    flap_flag       = True          # A flag to include or exclude a flap
                                    # True  - airfoil has a flap
                                    # False - draws a clean airfoil
    # Airfoil inputs
    rle         = [0.0084] #0.005785            # Main airfoil LE radius
    x_pre       = [0.458080577545180]                # x-location of the crest on the pressure side
    y_pre       = [-0.04553160030118]             # y-location of the crest on the pressure side  
    d2ydx2_pre  = [0.554845554794938]                # curvature of the crest on the pressure side  0.4793
    th_pre      = [-9.649803736]                 # trailing edge angle on the pressure side [deg]
    x_suc       = [0.46036604]                # x-location of the crest on the suction side        
    y_suc       = [0.06302395539]              # y-location of the crest on the suction side    
    d2ydx2_suc  = [-0.361421420]              # curvature of the crest on the suction side
    th_suc      = [-12.391677695858]# trailing edge angle on the suction side [deg]

    cf_c        = 0.3               # flap chord ratio
    ce_c        = 0.3               # conical curve extent ratio wrt the flap chord length
    csr_c       = 0.85               # shroud chord ratio
    clip_ext    = 0.05              # shroud lip extent ratio wrt the flap 
    r_le_flap   = 0.01              # flap leading edge radius
    tc_shr_tip  = 0.003             # shroud tip thickness
    w_conic     = 0.5               # conical parameter for the suction side of the flap airfoil

    delta_f     = 25                # flap deflection [deg]
    x_gap       = 0.01              # x-length gap from the shroud TE (positive value is moving the flap left)
    y_gap       = 0.005              # y-length gap from the shroud TE (positive value is moving the flap down)    

    delta_s     = 2                # droop nose deflection [deg]
    cs_c        = 0.4            # droop nose chord ratio
    d_cs_up     = 0.15               # droop nose offset from the hinge on the upper surface
    d_cs_low    = 0.38               # droop nose offset from the hinge on the lower surface
    k_Bez1      = 0.2
    k_Bez2      = 0.5


    w_con_seal  = 0.5               # conical parameter for the droop nose seal

    for i in range(len(rle)):
        airfoil_data   = [rle[i], x_pre[i], y_pre[i], d2ydx2_pre[i], th_pre[i], x_suc[i], y_suc[i], d2ydx2_suc[i], th_suc[i], cf_c, ce_c, csr_c, clip_ext, r_le_flap, tc_shr_tip, w_conic, w_con_seal]
        flap_setting   = [delta_f, x_gap, y_gap]
        droop_nose_set = [delta_s, cs_c, d_cs_up, d_cs_low, k_Bez1, k_Bez2]

        run_airfoil_analysis(airfoil_data, flap_setting, flap_flag, droop_nose_flag, droop_nose_set)



