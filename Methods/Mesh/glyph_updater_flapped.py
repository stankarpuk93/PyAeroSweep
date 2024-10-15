# glyph_updater_flapped.py
# 
# Created:  Oct 2023, S. Holenarsipura M Madhava
# Modified: Nov 2023, S. Karpuk
#    

import os

def update_glyph_script_fl(Mesh,working_dir,solvername):

    '''The file updates the Glyph script for a flapped airfoil
    
        Inputs:
            Mesh             - Mesh settings
            working_dir      - global working directory


        Outputs:
           

        Assumptions:

    '''

    # Unpack inputs
    glyph_file                  = Mesh.glyph_file
    upper_surface_filename      = Mesh.update_glyph_data["upper_surface_filename"]
    lower_surface_filename      = Mesh.update_glyph_data["lower_surface_filename"]
    cut1_filename               = Mesh.update_glyph_data["cut1_filename"]
    cut2_filename               = Mesh.update_glyph_data["cut2_filename"]
    flap_airfoil_lower_filename = Mesh.update_glyph_data["flap_airfoil_lower_filename"]
    flap_airfoil_upper_filename = Mesh.update_glyph_data["flap_airfoil_upper_filename"]
    connector_dimensions        = Mesh.update_glyph_data["connector_dimensions"]

    spacing_127_130 = Mesh.update_glyph_data["spacing_127_130"]
    spacing_137_140 = Mesh.update_glyph_data["spacing_137_140"]
    spacing_146_149 = Mesh.update_glyph_data["spacing_146_149"]
    spacing_156_159 = Mesh.update_glyph_data["spacing_156_159"]
    spacing_165_172 = Mesh.update_glyph_data["spacing_165_172"]
    spacing_178_184 = Mesh.update_glyph_data["spacing_178_184"]
    spacing_192_195 = Mesh.update_glyph_data["spacing_192_195"]
    spacing_201_204 = Mesh.update_glyph_data["spacing_201_204"]
    spacing_211_214 = Mesh.update_glyph_data["spacing_211_214"]

    addPoint228  = Mesh.update_glyph_data["addPoint228"]
    addPoint229  = Mesh.update_glyph_data["addPoint229"]
    addPoint245  = Mesh.update_glyph_data["addPoint245"]
    addPoint255  = Mesh.update_glyph_data["addPoint255"]
    addPoint_287 = Mesh.update_glyph_data["addPoint_287"]
    addPoint_288 = Mesh.update_glyph_data["addPoint_288"]
    EndAngle_289 = Mesh.update_glyph_data["EndAngle_289"]
    addPoint_298 = Mesh.update_glyph_data["addPoint_298"]
    addPoint_299 = Mesh.update_glyph_data["addPoint_299"]
    EndAngle_300 = Mesh.update_glyph_data["EndAngle_300"]

    node_to_connector_313   = Mesh.update_glyph_data["node_to_connector_313"]
    scaling_factor          = Mesh.update_glyph_data["scaling_factor"]
    BoundaryDecay_359       = Mesh.update_glyph_data["BoundaryDecay_359"]
    BoundaryDecay_384       = Mesh.update_glyph_data["BoundaryDecay_384"]
    maxlayers_430           = Mesh.update_glyph_data["maxlayers_430"]
    fulllayers_431          = Mesh.update_glyph_data["fulllayers_431"]
    growthrate_433          = Mesh.update_glyph_data["growthrate_433"]
    BoundaryDecay_435       = Mesh.update_glyph_data["BoundaryDecay_435"]
    far_field_connector_dim = Mesh.update_glyph_data["far_field_connector_dim"]
    meshed_file             = Mesh.update_glyph_data["meshed_file"]



    if solvername == 'SU2':
        lines_to_update = [ 14, 20, 26, 32, 38, 44, 98, 101, 104, 107, 110, 113, 116, 119, 127, 130, 137, 140, 146, 149, 156, 159,
                       165, 172, 178, 184, 192, 195, 201, 204, 211, 214, 228, 229, 245, 255, 280, 287, 288, 289, 298, 299,
                       300, 313, 332, 359, 384, 430, 431, 433, 435, 512 ]             
                    # 52 updates in total
    elif solvername == 'TAU':
        lines_to_update = [ 14, 20, 26, 32, 38, 44, 98, 101, 104, 107, 110, 113, 116, 119, 127, 130, 137, 140, 146, 149, 156, 159,
                       165, 172, 178, 184, 192, 195, 201, 204, 211, 214, 228, 229, 245, 255, 280, 287, 288, 289, 298, 299,
                       300, 313, 332, 359, 384, 430, 431, 433, 435, 597 ]             
                    # 52 updates in total
 
    else:
        lines_to_update = [ 14, 20, 26, 32, 38, 44, 98, 101, 104, 107, 110, 113, 116, 119, 127, 130, 137, 140, 146, 149, 156, 159,
                       165, 172, 178, 184, 192, 195, 201, 204, 211, 214, 228, 229, 245, 255, 280, 287, 288, 289, 298, 299,
                       300, 313, 332, 359, 384, 430, 431, 433, 435, 512 ]             
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
        f"  pw::Entity transform [pwu::Transform scaling -anchor " + "{0 0 0}" + f" {scaling_factor}] [$_TMP(mode_1) getEntities]",
        f"  $_DM(1) setUnstructuredSolverAttribute BoundaryDecay {BoundaryDecay_359}",
        f"  $_DM(1) setUnstructuredSolverAttribute BoundaryDecay {BoundaryDecay_384}",
        f"  $_DM(1) setUnstructuredSolverAttribute TRexMaximumLayers {maxlayers_430}",
        f"  $_DM(1) setUnstructuredSolverAttribute TRexFullLayers {fulllayers_431}",
        f"  $_DM(1) setUnstructuredSolverAttribute TRexGrowthRate {growthrate_433}",
        f"  $_DM(1) setUnstructuredSolverAttribute BoundaryDecay {BoundaryDecay_435}",
        f"  $_TMP(mode_1) initialize -strict -type CAE {meshed_file}"
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
            glyph_lines[428] = f"  $_TMP(PW_3) setValue {Mesh.delta_s}\n"
            glyph_lines[603] = f"  pw::Application save {meshed_file}.pw\n"


    # Write the updated content back to the Glyph script file
    with open(glyph_file, 'w') as updated_glyph_script:
        updated_glyph_script.writelines(glyph_lines)



    return