# standard_atmosphere.py
# 
# Created:  Nov 2023, S. Karpuk
# Modified: 

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
import numpy as np



def standard_atmosphere(Alt):
    ''' Computes temperature and pressure at a given altitude using 
        standard atmosphere formulations

        Inputs:
            Alt                 Altitude in m

        Outputs:
            T                   Temperature in K
            p                   Pressure in Pa
            mu                  Dynaic viscosity in kg/m*s
                    

        Assumptions:
            1. The formulation convers altitudes until 20 km
            2. No ISA deviations are considered

        '''


    if Alt <= 11000:
        T = 288.16 * (1-2.2558e-5*Alt)
        p = 101325 * (1-2.2558e-5*Alt)**5.2461

    else:
        T       = 288.16 * (1-2.2558e-5*11000)
        p_iso   = 101325 * (1-2.2558e-5*11000)**5.2461
        p       = p_iso * np.exp(-1.5783e-4*(Alt-11000))

    mu = 17.16e-6 * (T/273.15)**1.5 * (273.15+110.6)/(T+110.6)


    return p, T, mu