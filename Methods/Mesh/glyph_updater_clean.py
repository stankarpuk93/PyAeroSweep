# glyph_updater_clean.py
# 
# Created:  Oct 2023, S. Holenarsipura M Madhava
# Modified: Nov 2023, S. Karpuk
#           

import os

def update_glyph_script_cl(Mesh,working_dir):

    '''The file updates the Glyph script for a clean airfoil
    
        Inputs:
            delta_s             - first mesh size normal to the geometry
            glyph_file          - Glyph script filename
            update_glyph_data   - dictionary to update the Glyph script


        Outputs:
           

        Assumptions:

    '''

    # Unpack inputs
    glyph_file             = Mesh.glyph_file
    upper_surface_filename = Mesh.update_glyph_data["upper_surface_filename"]
    lower_surface_filename = Mesh.update_glyph_data["lower_surface_filename"]
    connector_dimensions   = Mesh.update_glyph_data["connector_dimensions"]
    begin_spacing          = Mesh.update_glyph_data["begin_spacing"]
    end_spacing            = Mesh.update_glyph_data["end_spacing"]
    scaling_factor         = Mesh.update_glyph_data["scaling_factor"]
    stop_at_height_1       = Mesh.update_glyph_data["stop_at_height_1"]
    stop_at_height_2       = Mesh.update_glyph_data["stop_at_height_2"]
    run_iterations_1       = Mesh.update_glyph_data["run_iterations_1"]
    run_iterations_2       = Mesh.update_glyph_data["run_iterations_2"]
    su2meshed_file         = Mesh.update_glyph_data["su2meshed_file"]


    # Assign new values to a template
    lines_to_update = [14, 20, 46, 49, 52, 59, 62, 68, 71, 80, 99, 100, 101, 102, 139]             # 15 updates in total (16th update is written below, for line 96)
    new_values = [
        f"  $_TMP(mode_1) initialize -strict -type Automatic {upper_surface_filename}",
        f"  $_TMP(mode_1) initialize -strict -type Automatic {lower_surface_filename}",
        f"$_CN(1) setDimension {connector_dimensions[0]}",
        f"$_CN(2) setDimension {connector_dimensions[1]}",
        f"$_CN(3) setDimension {connector_dimensions[2]}",
        f"  $_TMP(PW_1) setBeginSpacing {begin_spacing}",
        f"  $_TMP(PW_1) setEndSpacing {begin_spacing}",
        f"  $_TMP(PW_1) setEndSpacing {end_spacing}",
        f"  $_TMP(PW_1) setBeginSpacing {end_spacing}",
        f"  pw::Entity transform [pwu::Transform scaling -anchor " + "{0 0 0}" + f" {scaling_factor}] [$_TMP(mode_1) getEntities]",
        f"  $_DM(1) setExtrusionSolverAttribute StopAtHeight {stop_at_height_1}",
        f"  $_DM(1) setExtrusionSolverAttribute StopAtHeight {stop_at_height_2}",
        f"  $_TMP(mode_1) run {run_iterations_1}",
        f"  $_TMP(mode_1) run {run_iterations_2}",
        f"  $_TMP(mode_1) initialize -strict -type CAE {su2meshed_file}"
    ]

    # Read the entire content of the Glyph script
    os.chdir(working_dir)
    with open(glyph_file, 'r') as glyph_script:
        glyph_lines = glyph_script.readlines()

    # Update specific lines in the Glyph script with new values
    for i in range(len(lines_to_update)):
        line_number = lines_to_update[i]
        if 0 < line_number <= len(glyph_lines) and i < len(new_values):
            glyph_lines[line_number - 1] = new_values[i] + '\n'  # Line numbers are 1-based
            glyph_lines[97] = f"  $_DM(1) setExtrusionSolverAttribute NormalInitialStepSize {Mesh.delta_s}\n"

    # Write the updated content back to the Glyph script file
    with open(glyph_file, 'w') as updated_glyph_script:
        updated_glyph_script.writelines(glyph_lines)


    return


