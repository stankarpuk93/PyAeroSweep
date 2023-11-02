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
#   Generic Imports
# ----------------------------------------------------------------------
import os
import subprocess
import numpy as np
from mesh_pre_process        import mesh_pre_process
from create_airfoil_and_flap import create_airfoil_and_flap 
from Delta_S                 import calculate_initstepsize
from Fluent_sweeps           import main as Run_fluent
from SU2_sweeps              import main as Run_SU2


# Input function import
from Input_data              import Input_data
from Input_data_flapped      import Input_data_flapped




def run_airfoil_analysis(Input):

    '''Main function to run the analysis
    
        Inputs:
 


        Outputs:
           

        Assumptions:
            1. airfoil tip thickness is assumed 0.0025 from each side

    '''


    # Unpack all inputs
    Solver     = Input.Solver
    Geometry   = Input.Geometry
    Freestream = Input.Freestream
    Mesh       = Input.Mesh
 
    
    # Run the airfoil generation script
    if Geometry.PARSEC is True:
            create_airfoil_and_flap(Geometry)

                
    # Mesh the geometry
    if Mesh.meshing is True:

        # Update the Glyph script depending on the geometry 
        update_glyph_data = mesh_pre_process(Solver.working_dir,Geometry,Mesh)

        # Calculate mesh step size based on Y+
        delta_s = calculate_initstepsize(max(Freestream.Mach), min(Freestream.Altitude), Geometry.reference_values["Length"], Mesh.Yplus)

        if Geometry.flap is True: 

            # Update the Glyph script - Flapped Airfoil                               
            from glyph_updater_flapped   import update_glyph_script_fl    
            update_glyph_script_fl(delta_s,Mesh.glyph_file, update_glyph_data) 

        else:

            # Update the Glyph script - Clean Airfoil   
            from glyph_updater_clean     import update_glyph_script_cl
            update_glyph_script_cl(delta_s,Mesh.glyph_file, update_glyph_data)


        # Run Pointwise glyph script to generate the mesh

        os.chdir(Mesh.tclsh_directory)
        if Mesh.operating_system == "WINDOWS":
            working_dir_change = Solver.working_dir.replace('/','\\')
            full_glyph_path    = working_dir_change + "\\" + Mesh.glyph_file 
            subprocess.call(['tclsh ',full_glyph_path], stderr= None, stdin=subprocess.PIPE)    
        else:
            full_glyph_path = Solver.working_dir + "\\" + Mesh.glyph_file 
            subprocess.run('./pointwise ' + '-b ' + full_glyph_path, shell = True, stdin=subprocess.PIPE)

        # Run CFD solution
        '''if Solver == 'Fluent':
            Run_fluent(Alt_range,Mach_range,AoA_range,Fluent_settings,Ref_values,working_dir,casefile)
        elif Solver == 'SU2':
            Run_SU2(Solver_dim,Alt_range,Mach_range,AoA_range,SU2_settings,Ref_values,working_dir, SU2_conf_file, SU2_mesh)'''


    print("Analysis completed")


    return


if __name__ == '__main__':

    # Define airfoil sample inputs
    #--------------------------------------------------------------------------------------------------------------

        #Input = Input_data()
        Input = Input_data_flapped()

        run_airfoil_analysis(Input)


#######################################################################################################


