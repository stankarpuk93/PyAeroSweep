# Delta_S.py
# 
# Created:  Oct 2023, S. Holenarsipura M Madhava
# Modified: 
#           

import math


# Calculate initial step size using the provided values
def calculate_initstepsize(M,altitude,L,Yplus):

    '''Calculate the first mesh step size based on Y+
    
        Inputs:
            M     - Mach number
            altitude - cruise altitude
            L           - reference length [m]
            Yplus       - Desired Y+ value


        Outputs:
           delta_s - first mesh step size normal to the surface

        Assumptions:

    '''


    # Constants for standard atmosphere model
    TSL         = 288.16        # Sea-level temperature (K)
    Tiso        = 216.65        # Isothermal temperature (K)
    κ           = -2.2588e-5       # Temperature lapse rate (K/m)
    pSL         = 101325.0      # Sea-level pressure (Pa)
    piso        = 22632.1       # Pressure at isothermal layer (Pa)
    η           = -1.5783e-4    # Isothermal region constant
    rho_SL      = 1.225         # Sea-level density (kg/m^3)
    rho_iso     = 0.36391       # Density at isothermal layer (kg/m^3)
    µ0          = 1.716e-5      # Dynamic viscosity reference value (kg/(m·s))
    T0          = 273.15        # Reference temperature (K)
    S           = 110.6         # Sutherland's constant (K)
    R_universal = 287.05        #specific gas constant for dry air J/(kg·K)
    
    
    
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

