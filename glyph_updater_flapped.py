# glyph_updater_flapped.py
#
# Created: Oct 2023, S.Holenarsipura
# Modified: Oct 2023, S.Holenarsipura
#
# This script provides the ability to automatically update Glyph script of Flapped Airfoil.

# ----------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------

from Delta_S import delta_s

def update_glyph_script_fl( glyph_file_fl, upper_surface_filename, lower_surface_filename, cut1_filename, cut2_filename, 
                           flap_airfoil_lower_filename, flap_airfoil_upper_filename, connector_dimensions,
                           spacing_127_130, spacing_137_140, spacing_146_149, spacing_156_159, spacing_165_172, 
                           spacing_178_184, spacing_192_195, spacing_201_204, spacing_211_214, addPoint228, addPoint229, addPoint245,
                           addPoint255, far_field_connector_dim, addPoint_287, addPoint_288, EndAngle_289, addPoint_298,
                           addPoint_299, EndAngle_300, node_to_connector_313, scaling_factors, BoundaryDecay_359,
                           BoundaryDecay_384, maxlayers_430, fulllayers_431, growthrate_432, growthrate_433, BoundaryDecay_435,
                           su2meshed_file ):
    
    ''' Update specific lines in a Glyph script with new values for generating structured grids with flaps.
    
        Inputs:
            glyph_file_fl                : Path to the Flapped Airfoil Glyph script to update.
            upper_surface_filename       : Path to the upper surface file.
            lower_surface_filename       : Path to the lower surface file.
            cut1_filename                : Path to the first cut file.
            cut2_filename                : Path to the second cut file.
            flap_airfoil_lower_filename  : Path to the lower flap airfoil file.
            flap_airfoil_upper_filename  : Path to the upper flap airfoil file.
            connector_dimensions         : List of connector dimensions.
            spacing_XXX                  : Spacing values for various lines.
            addPointXXX                  : Coordinates of points to add.
            far_field_connector_dim      : Dimensions of the far-field connector.
            EndAngle_XXX                : End angles for specific lines.
            node_to_connector_313        : Node-to-connector dimension.
            scaling_anchor               : Scaling anchor for entity transformation.
            scaling_factors              : Scaling factors for entity transformation.
            BoundaryDecay_XXX           : Boundary decay values for specific lines.
            maxlayers_430                : TRex maximum layers attribute value.
            fulllayers_431               : TRex full layers attribute value.
            growthrate_432               : TRex growth rate attribute value.
            growthrate_433               : TRex growth rate attribute value.
            su2meshed_file               : Path to the SU2 meshed file.

        Assumptions:
            1. The Glyph script contains specific lines to be updated with new values.
    '''

    lines_to_update = [ 14, 20, 26, 32, 38, 44, 98, 101, 104, 107, 110, 113, 116, 119, 127, 130, 137, 140, 146, 149, 156, 159,
                       165, 172, 178, 184, 192, 195, 201, 204, 211, 214, 228, 229, 245, 255, 280, 287, 288, 289, 298, 299,
                       300, 313, 332, 359, 384, 430, 431, 432, 433, 435, 512 ]             
                       # 52 updates in total 
   
    new_values = [
        f"  $_TMP(mode_1) initialize -strict -type Automatic {upper_surface_filename}",
        f"  $_TMP(mode_1) initialize -strict -type Automatic {lower_surface_filename}",
        f"  $_TMP(mode_1) initialize -strict -type Automatic {cut1_filename}",
        f"  $_TMP(mode_1) initialize -strict -type Automatic {cut2_filename}",
        f"  $_TMP(mode_1) initialize -strict -type Automatic {flap_airfoil_lower_filename}",
        f"  $_TMP(mode_1) initialize -strict -type Automatic {flap_airfoil_upper_filename}",
        f"$_CN(1) setDimension {connector_dimensions[0]}",
        f"$_CN(2) setDimension {connector_dimensions[1]}",
        f"$_CN(3) setDimension {connector_dimensions[2]}",
        f"$_CN(4) setDimension {connector_dimensions[3]}",
        f"$_CN(5) setDimension {connector_dimensions[4]}",
        f"$_CN(6) setDimension {connector_dimensions[5]}",
        f"$_CN(7) setDimension {connector_dimensions[6]}",
        f"$_CN(8) setDimension {connector_dimensions[7]}",
        f"  $_TMP(PW_1) setBeginSpacing {spacing_127_130}",
        f"  $_TMP(PW_1) setEndSpacing {spacing_127_130}",
        f"  $_TMP(PW_1) setEndSpacing {spacing_137_140}",
        f"  $_TMP(PW_1) setBeginSpacing {spacing_137_140}",
        f"  $_TMP(PW_1) setEndSpacing {spacing_146_149}",
        f"  $_TMP(PW_1) setBeginSpacing {spacing_146_149}",
        f"  $_TMP(PW_1) setBeginSpacing {spacing_156_159}",
        f"  $_TMP(PW_1) setEndSpacing {spacing_156_159}",
        f"  $_TMP(PW_1) setBeginSpacing {spacing_165_172}",
        f"  $_TMP(PW_1) setEndSpacing {spacing_165_172}",
        f"  $_TMP(PW_1) setEndSpacing {spacing_178_184}",
        f"  $_TMP(PW_1) setBeginSpacing {spacing_178_184}",
        f"  $_TMP(PW_1) setEndSpacing {spacing_192_195}",
        f"  $_TMP(PW_1) setBeginSpacing {spacing_192_195}",
        f"  $_TMP(PW_1) setBeginSpacing {spacing_201_204}",
        f"  $_TMP(PW_1) setEndSpacing {spacing_201_204}",
        f"  $_TMP(PW_1) setBeginSpacing {spacing_211_214}",
        f"  $_TMP(PW_1) setEndSpacing {spacing_211_214}",
        f"  $_TMP(PW_1) addPoint {addPoint228}",
        f"  $_TMP(PW_1) addPoint {addPoint229}",
        f"  $_TMP(PW_1) addPoint {addPoint245}",
        f"  $_TMP(PW_1) addPoint {addPoint255}",
        f"  $_TMP(PW_1) do setDimension {far_field_connector_dim}",
        f"  $_TMP(PW_1) addPoint {addPoint_287}",
        f"  $_TMP(PW_1) addPoint {addPoint_288}",
        f"  $_TMP(PW_1) setEndAngle {EndAngle_289}",
        f"  $_TMP(PW_1) addPoint {addPoint_298}",
        f"  $_TMP(PW_1) addPoint {addPoint_299}",
        f"  $_TMP(PW_1) setEndAngle {EndAngle_300}",
        f"  $_TMP(PW_1) do setDimension {node_to_connector_313}",
        f"  pw::Entity transform [pwu::Transform scaling -anchor " + "{0 0 0}" + f" {scaling_factors}] [$_TMP(mode_1) getEntities]",
        f"  $_DM(1) setUnstructuredSolverAttribute BoundaryDecay {BoundaryDecay_359}",
        f"  $_DM(1) setUnstructuredSolverAttribute BoundaryDecay {BoundaryDecay_384}",
        f"  $_DM(1) setUnstructuredSolverAttribute TRexMaximumLayers {maxlayers_430}",
        f"  $_DM(1) setUnstructuredSolverAttribute TRexFullLayers {fulllayers_431}",
        f"  $_DM(1) setUnstructuredSolverAttribute TRexGrowthRate {growthrate_432}",
        f"  $_DM(1) setUnstructuredSolverAttribute TRexGrowthRate {growthrate_433}",
        f"  $_DM(1) setUnstructuredSolverAttribute BoundaryDecay {BoundaryDecay_435}",
        f"  $_TMP(mode_1) initialize -strict -type CAE {su2meshed_file}"
    ]

    # Read the entire content of the Glyph script
    with open(glyph_file_fl, 'r') as glyph_script:
        glyph_lines = glyph_script.readlines()

    # Update specific lines in the Glyph script with new values
    for i in range(len(lines_to_update)):
        line_number = lines_to_update[i]
        if 0 < line_number <= len(glyph_lines) and i < len(new_values):
            glyph_lines[line_number - 1] = new_values[i] + '\n'  # Line numbers are 1-based
            glyph_lines[428] = f"  $_TMP(PW_3) setValue {delta_s}\n"


    # Write the updated content back to the Glyph script file
    with open(glyph_file_fl, 'w') as updated_glyph_script:
        updated_glyph_script.writelines(glyph_lines)

#######################################################################################################