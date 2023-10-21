# glyph_updater_clean.py
#
# Created: Oct 2023, S.Holenarsipura
# Modified: Oct 2023, S.Holenarsipura
#
# This script provides the ability to automatically update Glyph script of Clean Airfoil.

# ----------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------

from Delta_S import delta_s


def update_glyph_script_cl( glyph_file_cl, upper_surface_filename, lower_surface_filename, connector_dimensions,  
                         spacing_59_63, spacing_68_71, su2meshed_file, run_iterations_1, run_iterations_2, 
                         stop_at_height_1, stop_at_height_2, normal_marching_vector, scaling_anchor,scaling_factors ):
    

    ''' Update specific lines in a Glyph script with new values for generating structured grids.
    
        Inputs:
            glyph_file_cl               : Path to the Clean Airfoil Glyph script to update.
            upper_surface_filename      : Path to the upper surface file.
            lower_surface_filename      : Path to the lower surface file.
            connector_dimensions        : List of connector dimensions.
            spacing_59_63               : Spacing value for lines 59-63.
            spacing_68_71               : Spacing value for lines 68-71.
            su2meshed_file              : Path to the SU2 meshed file.
            run_iterations_1            : Number of iterations to run for mode 1.
            run_iterations_2            : Number of iterations to run for mode 2.
            stop_at_height_1            : Height at which to stop for mode 1.
            stop_at_height_2            : Height at which to stop for mode 2.
            normal_marching_vector      : Normal marching vector for extrusion.
            scaling_anchor              : Scaling anchor for entity transformation.
            scaling_factors             : Scaling factors for entity transformation.

        Assumptions:
            1. The Glyph script contains specific lines to be updated with new values.
    '''


    lines_to_update = [14, 20, 46, 49, 52, 59, 62, 68, 71, 80, 98, 99, 100, 101, 102, 139]            
                      # 16 updates in total (17th update is written below, for line 96)
    
    
    new_values = [
        f"  $_TMP(mode_1) initialize -strict -type Automatic {upper_surface_filename}",
        f"  $_TMP(mode_1) initialize -strict -type Automatic {lower_surface_filename}",
        f"$_CN(1) setDimension {connector_dimensions[0]}",
        f"$_CN(2) setDimension {connector_dimensions[1]}",
        f"$_CN(3) setDimension {connector_dimensions[2]}",
        f"  $_TMP(PW_1) setBeginSpacing {spacing_59_63}",
        f"  $_TMP(PW_1) setEndSpacing {spacing_59_63}",
        f"  $_TMP(PW_1) setEndSpacing {spacing_68_71}",
        f"  $_TMP(PW_1) setBeginSpacing {spacing_68_71}",
        f"  pw::Entity transform [pwu::Transform scaling -anchor {scaling_anchor} {scaling_factors}] [$_TMP(mode_1) getEntities]",
        f"  $_DM(1) setExtrusionSolverAttribute NormalMarchingVector {normal_marching_vector}",
        f"  $_DM(1) setExtrusionSolverAttribute StopAtHeight {stop_at_height_1}",
        f"  $_DM(1) setExtrusionSolverAttribute StopAtHeight {stop_at_height_2}",
        f"  $_TMP(mode_1) run {run_iterations_1}",
        f"  $_TMP(mode_1) run {run_iterations_2}",
        f"  $_TMP(mode_1) initialize -strict -type CAE {su2meshed_file}",
        f"  $_TMP(mode_1) initialize -strict -type CAE {su2meshed_file}"
    ]

    # Read the entire content of the Glyph script
    with open(glyph_file_cl, 'r') as glyph_script:
        glyph_lines = glyph_script.readlines()

    # Update specific lines in the Glyph script with new values
    for i in range(len(lines_to_update)):
        line_number = lines_to_update[i]
        if 0 < line_number <= len(glyph_lines) and i < len(new_values):
            glyph_lines[line_number - 1] = new_values[i] + '\n'  # Line numbers are 1-based
            glyph_lines[97] = f"  $_DM(1) setExtrusionSolverAttribute NormalInitialStepSize {delta_s}\n"

    # Write the updated content back to the Glyph script file
    with open(glyph_file_cl, 'w') as updated_glyph_script:
        updated_glyph_script.writelines(glyph_lines)

#######################################################################################################


