import subprocess
import os
import numpy as np
import os
import subprocess
import shutil
import xlsxwriter

from Methods.Atmosphere.standard_atmosphere import standard_atmosphere

def solve(self,Freestream,Mesh,Geometry,Solver):

        ''' Runs the Xfoil aerodynamic analysis sweep for low-speed airfoils

        Available sweeps:
            Altitude
            Mach
            angle-of-attack


        Inputs:
            Freestream  - Freestream conditions
            Mesh        - Mesh settings
            Geometry    - Geometric settings
            

        Outputs:
            CL, CD, CM


        Assumptions:
            1. Reference axes:
                2D:     X - horizontal (chordwise)
                        Y - vertical
            7. Standard atmosphere in SI units is used

        '''


        # Define inputs
        #--------------------------------------------------------------------


        # Create Xfoil files for sweeps
        #--------------------------------------------------------------------
        len_Alt  = len(Freestream.Altitude)
        len_Mach = len(Freestream.Mach)
        len_AoA  = len(Freestream.Angle_of_attack)

        Cl = np.zeros((len_Alt,len_Mach,len_AoA))                               # Array of Cl
        Cd = np.zeros((len_Alt,len_Mach,len_AoA))                               # Array of Cd
        Cm = np.zeros((len_Alt,len_Mach,len_AoA))                               # Array of Cm

        # Initialize the workbook
        workbook  = xlsxwriter.Workbook('arrays.xlsx')

        warstart_set = self.warmstart
        for i in range(len_Alt):
            for j in range(len_Mach):
                for k in range(len_AoA): 

                        # Run the solution

                        # Create an Xfoil
                        filename = run_Xfoil_config(self,Freestream.Altitude[i],Freestream.Mach[j], \
                                                    Freestream.Angle_of_attack,Geometry,Mesh,Solver)

                        # Run SU2
                        new_direct  = 'Case_alt' + str("{:.2f}".format(Freestream.Altitude[i])) + '_Mach' + \
                                                    str("{:.2f}".format(Freestream.Mach[j])) + '_AoA' + \
                                                        str("{:.2f}".format(Freestream.Angle_of_attack[k]))
                        file_direct = os.path.join(self.working_dir, new_direct)
                        filename1 = os.path.join(file_direct, filename)

                        os.chdir(file_direct)

                        print('Running Solution ' + filename)
                        with open('SU2_output.log', 'w') as f:
                            #subprocess.call(['SU2_CFD', filename], stdout= f, stderr= None, stdin=subprocess.PIPE)
                            subprocess.call(['mpiexec', '-n',str(self.processors),'SU2_CFD', filename], stdout= f, stderr= None, stdin=subprocess.PIPE)

                        #run_SU2(self.processors,filename1)
                        print('Solution ' + filename + ' Completed')

                        # Read results
                        Cl[i,j,k],Cd[i,j,k],Cm[i,j,k] = read_results('SU2_output.log')

            # Write data into an Excel file 
            os.chdir(self.working_dir)
            sheetname = 'Altitude ' + str(Freestream.Altitude[i]) + 'm'
            worksheet = workbook.add_worksheet(name=sheetname)

            # create the 2D table frame
            worksheet.write(0, 0,"Cl")
            worksheet.write(0, 2*len_Mach,"Cd")
            worksheet.write(0, 3*len_Mach+2,"Cm")
            worksheet.write(1, 0,"AoA\Mach")
            worksheet.write(1, 2*len_Mach,"AoA\Mach")
            worksheet.write(1, 3*len_Mach+2,"AoA\Mach")
            for j in range(len_Mach):
                for k in range(len_AoA):
                    worksheet.write(1, j+1, Freestream.Mach[j])
                    worksheet.write(1, len_Mach + j+3, Freestream.Mach[j])
                    worksheet.write(1, 2*len_Mach + j+5, Freestream.Mach[j])
                    worksheet.write(k+2, 0, Freestream.Angle_of_attack[k])
                    worksheet.write(k+2, len_Mach+2, Freestream.Angle_of_attack[k])
                    worksheet.write(k+2, 2*len_Mach+4, Freestream.Angle_of_attack[k])

                    worksheet.write(k+2, j+1, Cl[i,j,k])
                    worksheet.write(k+2, len_Mach + j+3, Cd[i,j,k])
                    worksheet.write(k+2, 2*len_Mach + j+5, Cm[i,j,k])



        workbook.close()

        print(Cl)
        print(Cd)
        print(Cm)


        return



def run_Xfoil_config(self,Alt,Mach,AoA,num_AoA,Ref_values,Geometry,Mesh,Solver):

        ''' Creates a 2D case Xfoil config file for airfoils
        
            Inputs:
                Solver          - solver settings
                Alt             - altitudes [m]
                Mach            - mach number
                AoA             - angles-of-attack [deg]
                Ref_values      - reference values for aero forces nad moments



            Outputs:
                filename        - Generated journal filename


            Assumptions:

        '''

        # Unpack inputs
        output_polar = 'polar.dat'              # Output filename        
        Ncrit        = self.e_n
        max_iter     = self.max_iterations      # Max iterations for convergence

        Nnodes        = Mesh.airfoil_mesh_settings["connector dimensions"]
        bunching      = Mesh.airfoil_mesh_settings["clustering_coefficient"]
        te_ratio      = Mesh.airfoil_mesh_settings["LETE_spacing"]
        refined_ratio = Mesh.airfoil_mesh_settings["LE_spacing"]
        x_ref_top     = " ".join([f"{num}.0" for num in Mesh.airfoil_mesh_settings["refine_xc_top"]])
        x_ref_bot     = " ".join([f"{num}.0" for num in Mesh.airfoil_mesh_settings["refine_xc_bottom"]])
        airfoil_file  = Geometry.Segments[0].Airfoil.files['main'] 


        # Compute standard atmospheric and reference properties
        p_ref, T_ref, mu_ref = standard_atmosphere(Alt)
        rho_ref = p_ref/(287*T_ref)
        a_ref   = np.sqrt(1.4*287*T_ref)
        V_ref   = Mach * a_ref

        # Calculate Reynoldes number
        Re = rho_ref * V_ref * Ref_values["Length"] / mu_ref               # Reynolcs number based on unit length

        # Create run directories and copy the case file there
        new_direct  = 'Case_alt' + str("{:.2f}".format(Alt)) + '_Mach' + str("{:.2f}".format(Mach))

        filename    = new_direct + '.txt'
        file_direct = os.path.join(self.working_dir, new_direct)

        if os.path.exists(file_direct) and os.path.isdir(file_direct):
            shutil.rmtree(file_direct)
        os.mkdir(file_direct)

        os.chdir(self.working_dir)
            
        shutil.copyfile(os.path.join(os.getcwd()+'/'+self.config_file), file_direct+'/'+filename) 

        os.chdir(file_direct)
            
        # Create a config file for Xfoil

        xfoil_commands = f"""
        NACA 2412
        OPER
        VISC 1e6      ! Reynolds number = 1,000,000
        VPAR          ! Viscous parameters
        N             ! Use default Ncrit (e^9)
        XTR           ! Transition settings
        T T           ! Force top/bottom transition (use 'X X' for free transition)
        ITER 200      ! Max iterations for convergence
        PACC          ! Enable polar output
        naca2412_viscous_polar.txt  ! Output file
        ALFA 0.0 10.0 1.0  ! Alpha sweep (0° to 10°, step 1°)
        """

        # Generate XFOIL commands
        xfoil_commands1 = f"""
        LOAD {airfoil_file}
        PPAR
        N {Nnodes}
        P {bunching}
        T {te_ratio}
        R {refined_ratio}
        XT {x_ref_top}
        XB {x_ref_bot}
        \n                  ! Exit PPAR (empty line)
        OPER
        """

        xfoil_commands2 = f"""
        VISC {Re}
        VPAR
        N {Ncrit}           ! Set Ncrit (e.g., 9 for default, 4 for early transition)
        XTR
        {transition}
        """

        xfoil_commands3 = f"""
        ITER {max_iter}
        PACC
        {output_polar}
        ALFA {AoA[0]} {AoA[-1]} {num_AoA}

        """


        with open(filename, 'w') as f:
            f.write(xfoil_commands1)

            if Solver.viscous is True:
                # Define transition location
                if self.free_transition  is False:
                    transition = f"T {self.x_transition[0]} {self.x_transition[1]}"   
                else:
                    transition = f"X X"

                f.write(xfoil_commands2)

            f.write(xfoil_commands3)



        return filename



def launch_Xfoil(processors,filename):

    ''' Runs Xfoil
            
        Inputs:
            filename         - Generated journal filename

        Outputs:
                    

        Assumptions:

    '''

    # Run Xfoil
    #, stdin=subprocess.PIPE

    f = open('Xfoil_output.log', 'w')

    #subprocess.run(["xfoil.exe"], stdin=open("xfoil_input.txt", "r"), text=True)
    subprocess.run(["xfoil.exe"], stdin=open("xfoil_input.txt", "r"), stdout= f, stderr= None, stdin=subprocess.PIPE)

    f.close()    



    return


def read_results(output_file):
    ''' Read output Xfoil results 
            
            Inputs:
                output_file     - SU2 log file with output

            Outputs:
                Cl, Cd, Cm

            Assumptions:

    '''

        # Read results 
    with open(output_file, 'r') as f:
        last_line = f.readlines()[-37]

    results_array = last_line.split('|')

    Cl = float(results_array[-4])
    Cd = float(results_array[-5])
    Cm = float(results_array[-3])


    return Cl, Cd, Cm


