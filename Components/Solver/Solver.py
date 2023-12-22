#Solver.py
# 
# Created:  Nov 2023, S. Karpuk, 
# Modified: 
#           


# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------





class Solver():

    def __init__(self):
        
        self.processors     = 2
        self.monitor        = "DRAG"
        self.tolerance      = 1e-5
        self.max_iterations = 5000
        self.save_frequency = 100 
        self.warmstart      = 'NO'



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
