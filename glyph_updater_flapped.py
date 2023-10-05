# glyph_updater_flapped.py

def update_glyph_script_fl( glyph_file_fl, upper_surface_filename, lower_surface_filename, cut1_filename, cut2_filename, 
                           flap_airfoil_lower_filename, flap_airfoil_upper_filename, connector_dimensions,
                           begin_spacing_127, end_spacing_130, end_spacing_137, begin_spacing_140, end_spacing_146,
                           begin_spacing_149, begin_spacing_156, end_spacing_159, begin_spacing_165, end_spacing_172, 
                           end_spacing_178, begin_spacing_184, end_spacing_192, begin_spacing_195, begin_spacing_201, 
                           end_spacing_204, begin_spacing_211, end_spacing_214, addPoint228, addPoint229, addPoint245,
                           addPoint255, far_field_connector_dim, addPoint_287, addPoint_288, EndAngle_289, addPoint_298,
                           addPoint_299, EndAngle_300, node_to_connector_313, scaling_anchor,scaling_factors, BoundaryDecay_359,
                           BoundaryDecay_384, value_429, maxlayers_430, fulllayers_431, growthrate_432, growthrate_433, BoundaryDecay_435,
                           su2meshed_file ):
    
    lines_to_update = [ 14, 20, 26, 32, 38, 44, 98, 101, 104, 107, 110, 113, 116, 119, 127, 130, 137, 140, 146, 149, 156, 159,
                       165, 172, 178, 184, 192, 195, 201, 204, 211, 214, 228, 229, 245, 255, 280, 287, 288, 289, 298, 299,
                       300, 313, 332, 359, 384, 429, 430, 431, 432, 433, 435, 512 ]             
                    # 53 updates in total 
   
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
        f"  $_TMP(PW_1) setBeginSpacing {begin_spacing_127}",
        f"  $_TMP(PW_1) setEndSpacing {end_spacing_130}",
        f"  $_TMP(PW_1) setEndSpacing {end_spacing_137}",
        f"  $_TMP(PW_1) setBeginSpacing {begin_spacing_140}",
        f"  $_TMP(PW_1) setEndSpacing {end_spacing_146}",
        f"  $_TMP(PW_1) setBeginSpacing {begin_spacing_149}",
        f"  $_TMP(PW_1) setBeginSpacing {begin_spacing_156}",
        f"  $_TMP(PW_1) setEndSpacing {end_spacing_159}",
        f"  $_TMP(PW_1) setBeginSpacing {begin_spacing_165}",
        f"  $_TMP(PW_1) setEndSpacing {end_spacing_172}",
        f"  $_TMP(PW_1) setEndSpacing {end_spacing_178}",
        f"  $_TMP(PW_1) setBeginSpacing {begin_spacing_184}",
        f"  $_TMP(PW_1) setEndSpacing {end_spacing_192}",
        f"  $_TMP(PW_1) setBeginSpacing {begin_spacing_195}",
        f"  $_TMP(PW_1) setBeginSpacing {begin_spacing_201}",
        f"  $_TMP(PW_1) setEndSpacing {end_spacing_204}",
        f"  $_TMP(PW_1) setBeginSpacing {begin_spacing_211}",
        f"  $_TMP(PW_1) setEndSpacing {end_spacing_214}",
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
        f"  pw::Entity transform [pwu::Transform scaling -anchor {scaling_anchor} {scaling_factors}] [$_TMP(mode_1) getEntities]",
        f"  $_DM(1) setUnstructuredSolverAttribute BoundaryDecay {BoundaryDecay_359}",
        f"  $_DM(1) setUnstructuredSolverAttribute BoundaryDecay {BoundaryDecay_384}",
        f"  $_TMP(PW_3) setValue {value_429}",
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

    # Write the updated content back to the Glyph script file
    with open(glyph_file_fl, 'w') as updated_glyph_script:
        updated_glyph_script.writelines(glyph_lines)

##################################################################################################################


'''
def update_glyph_script(glyph_file):
    lines_to_update = [14, 20, 46, 49, 52, 59, 62, 68, 71, 80, 98, 99, 100, 101, 102, 139]
    new_values = [
        "  $_TMP(mode_1) initialize -strict -type Automatic G:\\TUBS\HiWi\\Dr Karpuk\\Version\\AF_CFD_V1\\main_airfoil_upper.dat",
        "  $_TMP(mode_1) initialize -strict -type Automatic G:\\TUBS\\HiWi\\Dr Karpuk\\Version\\AF_CFD_V1\\main_airfoil_lower.dat",
        "$_CN(1) setDimension 200",
        "$_CN(2) setDimension 200",
        "$_CN(3) setDimension 8",
        "  $_TMP(PW_1) setBeginSpacing 0.001",
        "  $_TMP(PW_1) setEndSpacing 0.001",
        "  $_TMP(PW_1) setEndSpacing 0.0005",
        "  pw::Entity transform [pwu::Transform scaling -anchor {0 0 0} {2.62 2.62 2.62}] [$_TMP(mode_1) getEntities]",
        "  $_DM(1) setExtrusionSolverAttribute NormalMarchingVector {-0 -0 -1}",
        "  $_DM(1) setExtrusionSolverAttribute StopAtHeight Off",
        "  $_DM(1) setExtrusionSolverAttribute StopAtHeight 529",
        "  $_TMP(mode_1) run 230",
        "  $_TMP(mode_1) run -1",
        "  $_TMP(mode_1) initialize -strict -type CAE G:\\TUBS\\HiWi\\Dr Karpuk\\Version\\AF_CFD_V1\\su2meshEx.su2"
        "  $_TMP(mode_1) initialize -strict -type CAE G:\\TUBS\\HiWi\\Dr Karpuk\\Version\\AF_CFD_V1\\su2meshEx.su2",
    ]
    
    
    
    # Read the entire content of the Glyph script
    with open(glyph_file, 'r') as glyph_script:
        glyph_lines = glyph_script.readlines()

    # Update the specific line with the calculated initial step size value
    glyph_lines[96] = f"  $_DM(1) setExtrusionSolverAttribute NormalInitialStepSize {delta_s}\n"    #Line 97 in the mesh_clean_airfoil_SU2.glf, but numbering starts from '0'

    # Write the updated content back to the Glyph script file
    with open(glyph_file, 'w') as updated_glyph_script:
            updated_glyph_script.writelines(glyph_lines)
    
##################################################################################################################   

    try:
        # Read the entire content of the Glyph script
        with open(glyph_file, 'r') as glyph_script:
            glyph_lines = glyph_script.readlines()

        # Update the specified lines with new values
        for i in range(len(lines_to_update)):
            line_number = lines_to_update[i]
            if 0 <= line_number < len(glyph_lines):
                glyph_lines[line_number] = new_values[i]

            # Update the specific line with the calculated initial step size value
            glyph_lines[96] = f"  $_DM(1) setExtrusionSolverAttribute NormalInitialStepSize {delta_s}\n"    #Line 97 in the mesh_clean_airfoil_SU2.glf, but numbering starts from '0'

        # Write the updated content back to the Glyph script file
        with open(glyph_file, 'w') as updated_glyph_script:
            updated_glyph_script.writelines(glyph_lines)

        print("Glyph script updated successfully.")

    except FileNotFoundError:
        print(f"File not found: {glyph_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    '''
##################################################################################################################

# glyph_updater.py
'''
def update_glyph_script(glyph_file):
    lines_to_update = [14, 20, 46, 49, 52, 59, 62, 68, 71, 80, 98, 99, 100, 101, 102, 139]
    new_values = [
        "  $_TMP(mode_1) initialize -strict -type Automatic G:\TUBS\HiWi\Dr Karpuk\Version\AF_CFD_V1\main_airfoil_upper.dat",
        "  $_TMP(mode_1) initialize -strict -type Automatic G:\TUBS\HiWi\Dr Karpuk\Version\AF_CFD_V1\main_airfoil_lower.dat",
        "$_CN(1) setDimension 200",
        "$_CN(2) setDimension 200",
        "$_CN(3) setDimension 8",
        "  $_TMP(PW_1) setBeginSpacing 0.001",
        "  $_TMP(PW_1) setEndSpacing 0.001",
        "  $_TMP(PW_1) setEndSpacing 0.0005",
        "  pw::Entity transform [pwu::Transform scaling -anchor {0 0 0} {2.62 2.62 2.62}] [$_TMP(mode_1) getEntities]",
        "  $_DM(1) setExtrusionSolverAttribute NormalMarchingVector {-0 -0 -1}",
        "  $_DM(1) setExtrusionSolverAttribute StopAtHeight Off",
        "  $_DM(1) setExtrusionSolverAttribute StopAtHeight 529",
        "  $_TMP(mode_1) run 230",
        "  $_TMP(mode_1) run -1",
        "  $_TMP(mode_1) initialize -strict -type CAE G:\TUBS\HiWi\Dr Karpuk\Version\AF_CFD_V1\su2meshEx.su2",
        "  $_TMP(mode_1) initialize -strict -type CAE G:\TUBS\HiWi\Dr Karpuk\Version\AF_CFD_V1\su2meshEx.su2",
    ]
    


    # Read the entire content of the Glyph script
    with open(glyph_file, 'r') as glyph_script:
        glyph_lines = glyph_script.readlines()

    # Update specific lines in the Glyph script with new values
    for i in range(len(lines_to_update)):
        line_number = lines_to_update[i]
        if 0 < line_number <= len(glyph_lines) and i < len(new_values):
            glyph_lines[line_number - 1] = new_values[i] + '\n'  # Line numbers are 1-based
            glyph_lines[96] = f"  $_DM(1) setExtrusionSolverAttribute NormalInitialStepSize {delta_s}\n"

    # Write the updated content back to the Glyph script file
    with open(glyph_file, 'w') as updated_glyph_script:
        updated_glyph_script.writelines(glyph_lines)
'''
##################################################################################################################