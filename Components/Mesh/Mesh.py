#Mesh.py
# 
# Created:  Nov 2023, S. Karpuk, S. Holenarsipura M Madhava
# Modified: 
#           


# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import math
import numpy as np


class Mesh():

    def __init__(self):
        """This sets the default for meshing in SUAVE.

        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """    

        self.meshing            = False
        self.structured         = False
        self.operating_system   = 'Linux'
        self.tclsh_directory    = r"/home/doktorand/Fidelity/Pointwise/Pointwise2022.1"     
        self.Yplus              = 1.0
        self.far_field          = 0.0
        self.glyph_file         = "mesh_clean_airfoil_SU2.glf"
        self.pw_mesh_file       = 'mesh_file.pw'

        self.airfoil_mesh_settings = {}


        # 3D surface mesh settings
        self.global_surface_mesh_settings = {
            "Min boundary subdivisions"   : 10,
            "Max extents subdivisions"    : 200,
            "Curvature resolution angle"  : 5,
            "Max aspect ratio"            : 100,
            "Refinement factor"           : 1,
            "Boundary gap subdivisions"   : 5            
        }

        self.trailing_edge_meshing_settings = {
            'Trailing edge mapping'      : False,
            "Trailing edge cells"        : 10,
            "Convex spacing growth rate" : 0.5,
            "Max aspect ratio"           : 100,
            "Spacing factor"             : 1
        }

        self.boundary_layer_settings = {
            "Max layers"                    : 1000,
            "Full layers"                   : 1,
            "Stop if full lazers not met"   : True,
            "Allow incoplete layers"        : True,
            "Push attributes"               : True,
            "Skew criteria equiangle"       : 1,
            "Growth rate"                   : 1.2,
            "Max included angle"            : 170,
            "Final cell aspect ratio"       : 1.0,
            "Collision buffer"              : 2,
            "Centroid skewness"             : 0.8,
            "Size field decay"              : 0.75,
        }


    def calculate_initstepsize(self,M,altitude,L,Mesh):

        ''' Calculate the first mesh step size based on Y+
    
        Inputs:
            M        - Mach number
            altitude - cruise altitude
            L        - reference length [m]
            Yplus    - Desired Y+ value
            Yplus_scaler - additional scaler to reduce initstepsize to account for over velocitys compare to flat plate
            Trex_groth_rate - Groth rate applied to inflation layer


        Outputs:
            delta_s  - initial step size [m]

        Assumptions:

        '''
        Yplus_scaler = Mesh.airfoil_mesh_settings["Initial_trex_layer_scaler"]

        if Mesh.structured==False:
            Trex_groth_rate = Mesh.airfoil_mesh_settings["TREX growth rate"]
        
        Yplus = Mesh.Yplus

        # Constants for standard atmosphere model
        TSL         = 288.16        # Sea-level temperature (K)
        Tiso        = 216.65        # Isothermal temperature (K)
        κ           = -2.2588e-5    # Temperature lapse rate (K/m)
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
        if altitude < 11000.0:                                      # Below 36,089 ft (11 km)
            T = TSL * (1 + κ * altitude)
        else:                                                       # Between 36,089 ft (11 km) and 65,616 ft (20 km)
            T = Tiso

        # Calculate pressure (p) based on altitude
        if altitude < 11000.0:                                      # Below 36,089 ft (11 km)
            p = pSL * (1 + κ * altitude) ** 5.2461
        else:                                                       # Between 36,089 ft (11 km) and 65,616 ft (20 km)
            p = piso * (η ** (altitude - 11000.0))

        # Calculate density (ρ) based on altitude
        if altitude < 11000.0:                                      # Below 36,089 ft (11 km)
            rho = rho_SL * (1 + κ * altitude) ** 4.2561
        else:                                                       # Between 36,089 ft (11 km) and 65,616 ft (20 km)
            rho = rho_iso * (math.exp ** (η * (altitude - 11000.0)))

        # Calculate freestream velocity (U_inf) based on Mach number and speed of sound (a)
        a = math.sqrt(1.4 * R_universal * T)                        # Speed of sound (m/s)
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
        self.delta_s = (Yplus * µ) / (Ufric * rho) * 1/Yplus_scaler

        if Mesh.structured==False:
            # estimate boundary layer thickness
            delta_99 = 0.38 * L/(Rex**(1/5))
        
            # Calculate nessary trex layers to resolve boundary layer for given groth rate
            N_MinLayer = math.log(-((delta_99/self.delta_s)*(1-Trex_groth_rate)-1), Trex_groth_rate)

        
            # Round layers to integer
            self.N_MinLayerRound = math.ceil(N_MinLayer)
            self.N_MaxLayerRound = math.ceil(N_MinLayer)


            airfoil_mesh_settings = {"Max TREX layers" : self.N_MaxLayerRound,
                                    "Full TREX layers": self.N_MinLayerRound}
        else:
            airfoil_mesh_settings = {"Max TREX layers" : "nan Structured mesh",
                                    "Full TREX layers": "nan Structured mesh"}



        #Mesh.airfoil_mesh_settings.update(update_airfoil_mesh_settings)
        return self.delta_s,airfoil_mesh_settings
    



    


