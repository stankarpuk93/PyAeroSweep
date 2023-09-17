# glyph_updater.py

def update_glyph_script( glyph_file, upper_surface_filename, lower_surface_filename, connector_dimensions,begin_spacing,  
                         end_spacing_1, end_spacing_2, su2meshed_file, run_iterations_1, run_iterations_2, 
                         stop_at_height_1, stop_at_height_2, normal_marching_vector, scaling_anchor,scaling_factors ):
    lines_to_update = [14, 20, 46, 49, 52, 59, 62, 68, 71, 80, 98, 99, 100, 101, 102, 139]             # 15 updates in total
    new_values = [
        f"  $_TMP(mode_1) initialize -strict -type Automatic {upper_surface_filename}",
        f"  $_TMP(mode_1) initialize -strict -type Automatic {lower_surface_filename}",
        f"$_CN(1) setDimension {connector_dimensions[0]}",
        f"$_CN(2) setDimension {connector_dimensions[1]}",
        f"$_CN(3) setDimension {connector_dimensions[2]}",
        f"  $_TMP(PW_1) setBeginSpacing {begin_spacing}",
        f"  $_TMP(PW_1) setEndSpacing {end_spacing_1}",
        f"  $_TMP(PW_1) setEndSpacing {end_spacing_2}",
        f"  pw::Entity transform [pwu::Transform scaling -anchor {scaling_anchor} {scaling_factors}] [$_TMP(mode_1) getEntities]",
        f"  $_DM(1) setExtrusionSolverAttribute NormalMarchingVector {normal_marching_vector}",
        f"  $_DM(1) setExtrusionSolverAttribute StopAtHeight {stop_at_height_1}",
        f"  $_DM(1) setExtrusionSolverAttribute StopAtHeight {stop_at_height_2}",
        f"  $_TMP(mode_1) run {run_iterations_1}",
        f"  $_TMP(mode_1) run {run_iterations_2}",
        f"  $_TMP(mode_1) initialize -strict -type CAE {su2meshed_file}"
        f"  $_TMP(mode_1) initialize -strict -type CAE {su2meshed_file}"
    ]

    # Read the entire content of the Glyph script
    with open(glyph_file, 'r') as glyph_script:
        glyph_lines = glyph_script.readlines()

    # Calculate initial step size using the provided values
    delta_s = calculate_initstepsize(L, mu, rho, U_infinity, Yplus)

    # Update the specific line with the calculated initial step size value
    glyph_lines[96] = f"  $_DM(1) setExtrusionSolverAttribute NormalInitialStepSize {delta_s}\n"    #Line 97 in the mesh_clean_airfoil_SU2.glf, but numbering starts from '0'

    # Write the updated content back to the Glyph script file
    with open(glyph_file, 'w') as updated_glyph_script:
        updated_glyph_script.writelines(glyph_lines)


def calculate_initstepsize( L, mu, rho, U_infinity, Yplus ):
    Rex = (  rho * U_infinity * L ) / mu
    Cf = 0.026 / (Rex ** (1/7))
    tau_wall = (Cf * rho * (U_infinity ** 2)) / 2
    Ufric = (tau_wall / rho) ** 0.5
    delta_s = (Yplus * mu ) / ( Ufric * rho )
    return delta_s                                          # wall spacing (m)

#--------------------------------------------------------------------------------------------------------------

# Data required to calculate initial step size
U_infinity = 100.0  # Replace with the actual freestream velocity (m/s)
rho = 1.225         # Replace with the actual freestream density (kg/m3)
mu = 0.00002        # Replace with the actual dynamic viscosity (kg/m s)
L = 1.0             # Replace with the actual reference length (m)
Yplus = 1.0         # Replace with the actual desired y+

##################################################################################