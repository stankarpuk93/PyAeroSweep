#Solver.py
# 
# Created:  Nov 2023, S. Karpuk, 
# Modified: 
#           


# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import os




class Solver():

    def __init__(self):

        self.dimensions     = '2d' 
        self.processors     = 2
        self.monitor        = "DRAG"
        self.tolerance      = 1e-5
        self.max_iterations = 5000
        self.save_frequency = 100 
        self.warmstart      = 'NO'

        # Xfoil default values
        self.e_n = 9                        # The factor N for the e^N method

        self.free_transition = False
        self.x_transition    = [0.0, 0.0]


    def run_solver(self,Freestream,Mesh,Geometry):
        ''' 
        Exectutes a CFD solver depending on the selected software
        
        Inputs:
         

        Outputs:


        Assumptions:

        '''

        if self.name == 'SU2':
            from SU2_class import SU2
            self.solution_method = SU2()
            SU2.solve(self,Freestream,Mesh,Geometry)
