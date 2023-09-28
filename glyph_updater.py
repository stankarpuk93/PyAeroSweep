# glyph_updater.py
import math
import numpy as np
from Mach_and_Alt import Alt_range, Mach_range

# Calculate initial step size using the provided values
def calculate_initstepsize(M, altitude, Yplus):
    # Constants for standard atmosphere model
    TSL = 288.16  # Sea-level temperature (K)
    Tiso = 216.65  # Isothermal temperature (K)
    κ = -0.0065  # Temperature lapse rate (K/m)
    pSL = 101325.0  # Sea-level pressure (Pa)
    piso = 22632.1  # Pressure at isothermal layer (Pa)
    η = 0.2233611  # Pressure ratio
    rho_SL = 1.225  # Sea-level density (kg/m^3)
    rho_iso = 0.36391  # Density at isothermal layer (kg/m^3)
    µ0 = 1.716e-5  # Dynamic viscosity reference value (kg/(m·s))
    T0 = 273.15  # Reference temperature (K)
    S = 110.6  # Sutherland's constant (K)
    R_universal = 287.05 #specific gas constant for dry air J/(kg·K)
    
    L = 2.62 #chord length - Scaling factor from Run_airfoil_analysis
    
    # Calculate temperature (T) based on altitude and Mach number
    if altitude < 11000.0:  # Below 36,089 ft (11 km)
        T = TSL * (1 + κ * altitude)
    else:  # Between 36,089 ft (11 km) and 65,616 ft (20 km)
        T = Tiso

    # Calculate pressure (p) based on altitude
    if altitude < 11000.0:  # Below 36,089 ft (11 km)
        p = pSL * (1 + κ * altitude) ** 5.2461
    else:  # Between 36,089 ft (11 km) and 65,616 ft (20 km)
        p = piso * (η ** (altitude - 11000.0))

    # Calculate density (ρ) based on altitude
    if altitude < 11000.0:  # Below 36,089 ft (11 km)
        rho = rho_SL * (1 + κ * altitude) ** 4.2561
    else:  # Between 36,089 ft (11 km) and 65,616 ft (20 km)
        rho = rho_iso * (math.exp ** (η * (altitude - 11000.0)))

    # Calculate freestream velocity (U_infinity) based on Mach number and speed of sound (a)
    a = math.sqrt(1.4 * R_universal * T)  # Speed of sound (m/s)
    U_infinity = M * a

    # Calculate dynamic viscosity (µ) based on temperature
    µ = µ0 *( (T / T0) ** 1.5 ) * ((T0 + S) / (T + S))

    # Calculate Reynolds number (Rex)
    Rex = (rho * U_infinity * L) / µ

    # Calculate skin friction coefficient (Cf)
    Cf = 0.026 / (Rex ** (1 / 7))

    # Calculate wall shear stress (tau_wall)
    tau_wall = (Cf * rho * (U_infinity ** 2)) / 2

    # Calculate friction velocity (Ufric)
    Ufric = math.sqrt(tau_wall / rho)

    # Calculate initial step size (delta_s)
    delta_s = (Yplus * µ) / (Ufric * rho)

    return delta_s

# Desired Y+
desired_Yplus = 1.0  # Replace with the desired Y+


# Loop over altitude and Mach number ranges      NOTE: Mach_range & Alt_range are under the file Mach_and_Alt.py (circular import error)
for altitude in Alt_range:
    for Mach_number in Mach_range:
        # Calculate initial step size
        delta_s = calculate_initstepsize(Mach_number, altitude, desired_Yplus)



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

    # Update the specific line with the calculated initial step size value
    glyph_lines[96] = f"  $_DM(1) setExtrusionSolverAttribute NormalInitialStepSize {delta_s}\n"    #Line 97 in the mesh_clean_airfoil_SU2.glf, but numbering starts from '0'

    # Write the updated content back to the Glyph script file
    with open(glyph_file, 'w') as updated_glyph_script:
            updated_glyph_script.writelines(glyph_lines)





