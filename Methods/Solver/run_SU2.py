import subprocess
import os
import numpy as np
import os
import sys
import subprocess
import shutil
import xlsxwriter

from Methods.Atmosphere.standard_atmosphere import standard_atmosphere

def solve(self,Freestream,Mesh,Geometry):

        ''' Runs the SU2 aerodynamic analysis sweep for airfoils, wings, and aircraft
        So far, the file uses a .cfg template and sets reference values and methods up
        The .cfg file needs to be established beforehand

        Available sweeps:
            Altitude
            Mach
            anagle-of-attack


        Inputs:
            Freestream  - Freestream conditions
            Mesh        - Mesh settings
            Geometry    - Geometric settings
            

        Outputs:
            CL, CD, CM


        Assumptions:
            1. Solver settings depend on the .cfg file
            2. Reference axes:
                2D:     X - horizontal (chordwise)
                        Y - vertical
            7. Standard atmosphere in SI units is used
            8. Boundary conditions name requirements:
                far-field    - 'far-field'
                body surface - 'wall'

        '''


        # Define inputs
        #--------------------------------------------------------------------


        # Create SU2 .cfg files for sweeps
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

                        # Create a config file
                        # Adjust settings for the warm start
                        if (k == 0 and warstart_set== 'YES') or warstart_set == 'NO':
                            self.warmstart = 'NO'
                        else:
                            self.warmstart = 'YES'
                        filename = run_SU2_config(self,Freestream.Altitude[i],Freestream.Mach[j],Freestream.Angle_of_attack,\
                                                        Geometry.reference_values,Mesh,k)

                        # Run SU2
                        new_direct  = 'Case_alt' + str("{:.2f}".format(Freestream.Altitude[i])) + '_Mach' + \
                                                    str("{:.2f}".format(Freestream.Mach[j])) + '_AoA' + \
                                                        str("{:.2f}".format(Freestream.Angle_of_attack[k]))
                        file_direct = os.path.join(self.output_dir, new_direct)
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
            os.chdir(self.output_dir)
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



def run_SU2_config(self,Alt,Mach,AoA,Ref_values,Mesh,k):

        ''' Creates a 2D case SU2 config file for airfoils
        
            Inputs:
                Solver          - solver settings
                Mesh            - mesh settings
                Alt             - altitudes [m]
                Mach            - mach number
                AoA             - angle-of-attack [deg]
                Ref_values      - reference values for aero forces nad moments
                k               - angle-of-attack index


            Outputs:
                filename        - Generated journal filename


            Assumptions:

        '''


        # Compute standard atmospheric and reference properties
        p_ref, T_ref, mu_ref = standard_atmosphere(Alt)
        rho_ref = p_ref/(287*T_ref)
        a_ref   = np.sqrt(1.4*287*T_ref)
        V_ref   = Mach * a_ref

        # Calculate Reynoldes number
        Re = rho_ref * V_ref * Ref_values["Length"] / mu_ref               # Reynolcs number based on unit length

        # Create run directories and copy the case file there
        if AoA[k] < 0:
            new_direct  = 'Case_alt' + str("{:.2f}".format(Alt)) + '_Mach' + str("{:.2f}".format(Mach)) + '_AoA_' + str("{:.2f}".format(abs(AoA[k])))
        else:    
            new_direct  = 'Case_alt' + str("{:.2f}".format(Alt)) + '_Mach' + str("{:.2f}".format(Mach)) + '_AoA' + str("{:.2f}".format(AoA[k]))
        filename    = new_direct + '.cfg'
        file_direct = os.path.join(self.output_dir, new_direct)

        if os.path.exists(file_direct) and os.path.isdir(file_direct):
            shutil.rmtree(file_direct)
        os.mkdir(file_direct)

        os.chdir(self.output_dir)
            
        shutil.copyfile(os.path.join(self.working_dir+'/'+self.config_file), file_direct+'/'+filename) 

        # Copy the mesh file
        if Mesh.operating_system == "WINDOWS":
            shutil.copy(self.output_dir + '\\' + Mesh.filename, file_direct + '\\' + Mesh.filename)                               # copies the mesh file from the reference folder to the target one
        else:
            shutil.copy(self.output_dir + '/' + Mesh.filename, file_direct + '/' + Mesh.filename)         

        # Copy the restart file
        if self.warmstart == 'YES':
            if AoA[k] < 0:
                prev_direct  = 'Case_alt' + str("{:.2f}".format(Alt)) + '_Mach' + str("{:.2f}".format(Mach)) + '_AoA_' + str("{:.2f}".format(abs(AoA[k-1])))
            else:    
                prev_direct  = 'Case_alt' + str("{:.2f}".format(Alt)) + '_Mach' + str("{:.2f}".format(Mach)) + '_AoA' + str("{:.2f}".format(AoA[k-1]))
            prev_file_direct = os.path.join(self.output_dir, prev_direct)
            shutil.copyfile(prev_file_direct+'/restart.dat', file_direct+'/solution_flow.dat')        


        os.chdir(file_direct)
            
        # Modify the reference config file
        f = open(filename, 'r+')
        cfg_data = f.readlines()
        f.close()

        if self.dimensions == "2d":
            # Creates inputs according to the 2d airfoil template
            cfg_data[3]   = 'KIND_TURB_MODEL= ' + self.turbulence_model + '\n'
            cfg_data[8]   = 'MACH_NUMBER= ' + str(Mach) + '\n'
            cfg_data[9]   = 'AOA= ' + str(AoA[k]) + '\n'
            cfg_data[12]  = 'FREESTREAM_TEMPERATURE= ' + str(T_ref) + '\n'
            cfg_data[13]  = 'REYNOLDS_NUMBER= ' + str(round(Re)) + '\n'
            cfg_data[14]  = 'REYNOLDS_LENGTH= ' + str(Ref_values["Length"] ) + '\n'
            cfg_data[18]  = 'REF_AREA= ' + str(Ref_values["Area"]) + '\n'
            cfg_data[19]  = 'REF_LENGTH= ' + str(Ref_values["Length"] ) + '\n'
            cfg_data[20]  = 'REF_ORIGIN_MOMENT_X= ' + str(Ref_values["Point"][2]) + '\n'
            cfg_data[81]  = 'ITER= ' + str(self.max_iterations) + '\n'
            cfg_data[95]  = 'CONV_CAUCHY_EPS= ' + str(self.tolerance) + '\n'
            cfg_data[100] = 'MESH_FILENAME= ' + Mesh.filename + '\n'
            cfg_data[102] = 'RESTART_SOL= ' + self.warmstart + '\n'
            cfg_data[104] = 'OUTPUT_WRT_FREQ= ' + str(self.save_frequency) + '\n'
        elif self.dimensions == "3d":
            # Creates inputs according to the 3d airfoil template
            cfg_data[19] = 'KIND_TURB_MODEL= ' + self.turbulence_model + '\n'
            cfg_data[30] = 'MACH_NUMBER= ' + str(Mach) + '\n'
            cfg_data[33] = 'AOA= ' + str(AoA[k]) + '\n'
            cfg_data[39] = 'FREESTREAM_TEMPERATURE= ' + str(T_ref) + '\n'
            cfg_data[42] = 'REYNOLDS_NUMBER= ' + str(round(Re)) + '\n'
            cfg_data[45] = 'REYNOLDS_LENGTH= ' + str(Ref_values["Length"]) + '\n'
            cfg_data[93] = 'REF_ORIGIN_MOMENT_X= ' + str(Ref_values["Point"][2]) + '\n'
            cfg_data[98] = 'REF_LENGTH= ' + str(Ref_values["Length"]) + '\n'
            cfg_data[101] = 'REF_AREA= ' + str(Ref_values["Area"]) + '\n'
            if self.symmetric is True:
                # The case if a symmetry BC is used
                cfg_data[112] = 'MARKER_SYM= ( symmetry ) \n'
                cfg_data[139] = 'ITER= ' + str(self.max_iterations) + '\n'
                cfg_data[226] = 'CONV_CAUCHY_EPS= ' + str(self.tolerance) + '\n'
                cfg_data[238] = 'MESH_FILENAME= ' + Mesh.filename + '\n'
                cfg_data[25 ] = 'RESTART_SOL= ' + self.warmstart + '\n'
                cfg_data[281] = 'OUTPUT_WRT_FREQ= ' + str(self.save_frequency) + '\n'
            else:
                cfg_data[216] = 'ITER= ' + str(self.max_iterations) + '\n'
                cfg_data[230] = 'CONV_CAUCHY_EPS= ' + str(self.tolerance) + '\n'
                cfg_data[236] = 'MESH_FILENAME= ' + Mesh.filename + '\n'
                cfg_data[239] = 'RESTART_SOL= ' + self.warmstart + '\n'
                cfg_data[240] = 'OUTPUT_WRT_FREQ= ' + str(self.save_frequency) + '\n'
                            
        f = open(filename, 'w')
        for item in cfg_data:
                f.write(item)
        f.close()


        return filename



def launch_SU2(processors,filename):

    ''' Runs SU2
            
        Inputs:
            SU2_settings     - Array of SU2 prescribed settings
            filename         - Generated journal filename

        Outputs:
                    

        Assumptions:

    '''

    # Run SU2
    #, stdin=subprocess.PIPE

    f = open('SU2_output.log', 'w')
    f.write('here')

    print(os.getcwd())
    print(['mpiexec', '-n',str(processors),'SU2_CFD', filename])
    print(' '.join(['mpiexec', '-n',str(processors),'SU2_CFD', filename]))

    subprocess.call(['mpiexec', '-n',str(processors),'SU2_CFD', filename], stdout= f, stderr= None, stdin=subprocess.PIPE)

    f.close()    
    #with open('SU2_output.log', 'w') as f:
        #subprocess.call(['mpiexec', '-n',str(processors),'SU2_CFD', filename], stdout= f, stderr= None, stdin=subprocess.PIPE)


    return


def read_results(output_file):
    ''' Read output SU2 results 
            
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


