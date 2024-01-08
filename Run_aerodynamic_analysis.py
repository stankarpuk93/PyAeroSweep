# Run_airfoil_analysis.py
# 
# Created:  Dec 2022, S. Karpuk
# Modified: Oct 2023, S. Holenarsipura M Madhava
#           Nov 2023, S. Karpuk


"""
The code runs the generation of an airfoil or a wing using the PARSEC or CST methods,
generates a mesh using Pointwise glyph capabilities,
and runs the analysis sweep using a given CFD package

Capabilities:
    1. Generation of PARSEC/CST airfoils for clean and flapped configurations
    2. Airfoil/Wing automaitc meshing using Pointwise
    3. Execution of SU2 for given meshes using RANS with available turbulence models

Compatibility: 
    The tool is compatible for both Windows and Linux systems

Prerequisites:
    1. Pointwise 
    2. SU2
    3. pygeo
    4. OpenMPI
    5. preFoil

"""

# ----------------------------------------------------------------------
#   Generic Imports
# ----------------------------------------------------------------------
import os
import shutil
import subprocess
import numpy as np
from Methods.Mesh.mesh_pre_process_2D     import mesh_pre_process_2D
from Methods.Mesh.mesh_pre_process_3D     import WingMeshPreProcess 
from Methods.Solver                       import run_SU2


def run_aerodynamic_analysis(Input):

    '''Main function to run the analysis
    
        Inputs:
            Input.Solver     - Solver settings
                  Geometry   - Geometric settings
                  Freestream - Freestream conditions
                  Mesh       - Mesh settings


        Outputs:
           

        Assumptions:

    '''


    # Unpack all inputs
    Solver     = Input.Solver
    Geometry   = Input.Geometry
    Freestream = Input.Freestream
    Mesh       = Input.Mesh
 
    # Run the airfoil/wing generation script in a separate directory
    if Geometry.generate is True:
        file_path = os.path.join(Solver.working_dir, 'Geometry_files/')
        if os.path.exists(file_path):
            shutil.rmtree(file_path)
        os.mkdir(file_path)
        os.chdir(file_path)
        num_segm = len(Geometry.Segments.keys())
        for i in range(num_segm):
            if len(Geometry.Segments[i].Airfoil.PARSEC) != 0:
                Geometry.Segments[i].create_PARSEC_airfoil()
            elif len(Geometry.Segments[i].Airfoil.CST) != 0:
                Geometry.Segments[i].create_CST_airfoil()


        # Create a wing using pygeo if a 3D case is defined 
        if Solver.dimensions == '3d':  
            Geometry.create_wing_geometry()

         
    # Mesh the geometry
    if Mesh.meshing is True:

        # Calculate mesh step size based on Y+
        Mesh.calculate_initstepsize(max(Freestream.Mach), min(Freestream.Altitude), Geometry.reference_values["Length"], Mesh.Yplus)

        # Assign a flag for an inviscid solver
        if Solver.turbulence_model == 'Inviscid':
            Inviscid_flag = True
        else:
            Inviscid_flag = False

        # Update the Glyph script depending on the geometry 
        if  Solver.dimensions == '2d':
            mesh_pre_process_2D(Solver.working_dir,Geometry,Mesh)
            if  Geometry.Segments[0].TrailingEdgeDevice.type == 'Slotted': 
                # Update the Glyph script - Slotted flap airfoil                               
                from Methods.Mesh.glyph_updater_flapped   import update_glyph_script_fl    
                update_glyph_script_fl(Mesh,Solver.working_dir) 
            else:
                # Update the Glyph script - clean Airfoil or one with a plain flap 
                from Methods.Mesh.glyph_updater_clean     import update_glyph_script_cl
                update_glyph_script_cl(Mesh,Solver.working_dir)

        elif Solver.dimensions == '3d':
            wing_meshing = WingMeshPreProcess()
            wing_meshing.write_glyph_file(Solver.working_dir,Geometry,Mesh,Solver,Inviscid_flag)
        else:
            print("Specify 2d or 3d solver dimensions")
        

        # Run Pointwise glyph script to generate the mesh
        os.chdir(Mesh.tclsh_directory)
        if Mesh.operating_system == "WINDOWS":
            working_dir_change = Solver.working_dir.replace('/','\\')
            full_glyph_path    = working_dir_change + "\\" + Mesh.glyph_file 
            p = subprocess.call(['tclsh ',full_glyph_path], stderr= None, stdin=subprocess.PIPE)    
        else:
            full_glyph_path = Solver.working_dir + "/" + Mesh.glyph_file 
            p = subprocess.call('./pointwise ' + '-b ' + full_glyph_path, shell = True, stdin=subprocess.PIPE)


    # Run CFD solution
    run_SU2.solve(Solver,Freestream,Mesh,Geometry)
    

    print("Analysis completed")


    return
