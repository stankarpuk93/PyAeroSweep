# SU2_sweeps.py
# 
# Created:  Aug 2022, S. Karpuk
# Modified:

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
import numpy as np
import os
import subprocess
import shutil
import xlsxwriter


# ----------------------------------------------------------------------
#   Main
# ----------------------------------------------------------------------


def main(Solver,Freestream,Mesh,Geometry):
    ''' Runs the SU2 aerodynamic analysis sweep for airfoils, wings, and aircraft
        So far, the file uses a .cfg template and sets reference values and methods up
        The .cfg file needs to be established beforehand

        Available sweeps:
            Altitude
            Mach
            anagle-of-attach



        Inputs:
            num_proc                                    Number of processors used fot the solution
            Alt_range                                   Analysis altitudes
            Mach_range                                  Range of Mach numbers
            AoA_range                                   Range of angles-of-attack
            Ref_dir                                     Solution refefence directory
            turbulence_model                            Turbulence model
            save_freq                                   Data saving frequency in number of iterations
            conv_criteria                               Global residual convergence criteria 
            iterations                                  Number of iterations to converge the solution
            SU2_config_file                             Reference .cfg file

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
    ''' ANSYS Fluent solver options
        Possible options:
            Dimensions      : 2d, 2ddp, 3d, 3ddp   (dp - double precision)
            Type            : pressure-based, density-based
            Method          : SIMPLE, SIMPLEC, PISO, Coupled
            Turbulence model: inviscid, laminar, k-kl-w, ke-realizable, ke-rng, ke-standard
                              kw-standard, kw-sst, spalart-allmaras, transition-sst, reynolds-stress-model
            Time_type       : Steady, Transient

    '''


    # Create SU2 .cfg files for sweeps
    #--------------------------------------------------------------------
    len_Alt  = len(Freestream.Altitude)
    len_Mach = len(Freestream.Mach)
    len_AoA  = len(Freestream.Angle_of_attack)
    Cl = np.zeros((len_Alt,len_Mach,len_AoA))                               # Array of Cl
    Cd = np.zeros((len_Alt,len_Mach,len_AoA))                               # Array of Cd
    Cm = np.zeros((len_Alt,len_Mach,len_AoA))                               # Array of Cm

    wartsatrt_set = Solver.warmstart
    for i in range(len_Alt):
        for j in range(len_Mach):
            for k in range(len_AoA): 

                    # Run the solution

                    # Create a config file
                    # Adjust settings for the warm start
                    if (k == 0 and wartsatrt_set == 'YES') or wartsatrt_set == 'NO':
                        Solver.warmstart = 'NO'
                    else:
                        Solver.warmstart = 'YES'
                    filename = run_SU2_config(Solver,Freestream.Altitude[i],Freestream.Mach[j],Freestream.Angle_of_attack,\
                                                Geometry.reference_values,Mesh,k)

                    # Run Fluent
                    new_direct  = 'Case_alt' + str("{:.2f}".format(Alt_range[i])) + '_Mach' + str("{:.2f}".format(Mach_range[j])) + '_AoA' + str("{:.2f}".format(AoA_range[k]))
                    file_direct = os.path.join(Ref_dir, new_direct)
                    filename = os.path.join(file_direct, filename)

                    os.chdir(file_direct)

                    print('Running Solution ' + filename)
                    run_SU2(Solver.processors,filename)
                    print('Solution ' + filename + ' Completed')

                    # Read results
                    Cl[i,j,k],Cd[i,j,k],Cm[i,j,k] = read_results('SU2_output.log')

            # Write data into an Excel file 
            os.chdir(Ref_dir)
            workbook  = xlsxwriter.Workbook('arrays.xlsx')
            sheetname = 'Altitude' + str(Alt_range[i]) + 'm'
            worksheet = workbook.add_worksheet(name=sheetname)


            # create the 2D table frame
            for j in range(len_Mach):
                for k in range(len_AoA):
                    worksheet.write(0, j+1, Mach_range[j])
                    worksheet.write(0, len_Mach + j+3, Mach_range[j])
                    worksheet.write(0, 2*len_Mach + j+5, Mach_range[j])
                    worksheet.write(k+1, 0, AoA_range[k])
                    worksheet.write(k+1, len_Mach+2, AoA_range[k])
                    worksheet.write(k+1, 2*len_Mach+4, AoA_range[k])

                    worksheet.write(k+1, j+1, Cl[i,j,k])
                    worksheet.write(k+1, len_Mach + j+3, Cd[i,j,k])
                    worksheet.write(k+1, 2*len_Mach + j+5, Cm[i,j,k])


            workbook.close()


    '''else:
        for i in range(len(Altitude_range)):
            for j in range(len(Mach_range)):
                for k in range(len(AoA_range)): 
                    for l in range(len(AoS_range)):'''


    print(Cl)
    print(Cd)
    print(Cm)


    return



def run_SU2_config(Solver,Alt,Mach,AoA,Ref_values,Mesh,k):
    ''' Creates a 2D case SU2 config file for airfoils
    
        Inputs:
            SU2_settings                                Array of SU2 prescribed settings
            Alt                                         Altitudes
            Mach                                        Mach number
            AoA                                         Angle-of-attack
            Ref_dir                                     Reference directory
            Ref_values                                  Reference values
            ref_casefile                                case file name


        Outputs:
            filename                                    Generated journal filename


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
    file_direct = os.path.join(Mesh.operating_system, new_direct)

    if os.path.exists(file_direct) and os.path.isdir(file_direct):
        shutil.rmtree(file_direct)
    os.mkdir(file_direct)

    os.chdir(Solver.working_dir)
    
    shutil.copyfile(os.path.join(os.getcwd()+'/'+Solver.config_file), file_direct+'/'+filename) 

    # Copy the mesh file
    if Mesh.operating_system == "WINDOWS":
        shutil.copy(Solver.working_dir + '\\' + Mesh.filename, file_direct + '\\' + Mesh.filename)                               # copies the mesh file from the reference folder to the target one
    else:
        shutil.copy(Solver.working_dir + '/' + Mesh.filename, file_direct + '/' + Mesh.filename)         

    # Copy the restart file
    if Solver.warmstart == 'YES':
        if AoA[k] < 0:
            prev_direct  = 'Case_alt' + str("{:.2f}".format(Alt)) + '_Mach' + str("{:.2f}".format(Mach)) + '_AoA_' + str("{:.2f}".format(abs(AoA[k-1])))
        else:    
            prev_direct  = 'Case_alt' + str("{:.2f}".format(Alt)) + '_Mach' + str("{:.2f}".format(Mach)) + '_AoA' + str("{:.2f}".format(AoA[k-1]))
        prev_file_direct = os.path.join(Solver.working_dir, prev_direct)
        shutil.copyfile(prev_file_direct+'/restart.dat', file_direct+'/solution_flow.dat')        


    os.chdir(file_direct)
    
    # Modify the reference config file
    f = open(filename, 'r+')
    cfg_data = f.readlines()
    f.close()

    if Solver_dim == "2d":
        # Creates inputs according to the 2d airfoil template
        cfg_data[3]  = 'KIND_TURB_MODEL= ' + Solver.turbulence_model + '\n'
        cfg_data[8]  = 'MACH_NUMBER= ' + str(Mach) + '\n'
        cfg_data[9]  = 'AOA= ' + str(AoA[k]) + '\n'
        cfg_data[12] = 'FREESTREAM_TEMPERATURE= ' + str(T_ref) + '\n'
        cfg_data[13] = 'REYNOLDS_NUMBER= ' + str(round(Re)) + '\n'
        cfg_data[14] = 'REYNOLDS_LENGTH= ' + str(Ref_values["Length"] ) + '\n'
        cfg_data[18] = 'REF_AREA= ' + str(Ref_values["Area"]) + '\n'
        cfg_data[19] = 'REF_LENGTH= ' + str(Ref_values["Length"] ) + '\n'
        cfg_data[20] = 'REF_ORIGIN_MOMENT_X= ' + str(Ref_values["Point"][2]) + '\n'
        cfg_data[81] = 'ITER= ' + str(Solver.max_iterations) + '\n'
        cfg_data[95] = 'CONV_CAUCHY_EPS= ' + str(Solver.tolerance) + '\n'
        cfg_data[100] = 'MESH_FILENAME= ' + Mesh.filename + '\n'
        cfg_data[102] = 'RESTART_SOL= ' + Solver.warmstart + '\n'
        cfg_data[104] = 'OUTPUT_WRT_FREQ= ' + str(Solver.save_frequency) + '\n'
    elif Solver_dim == "3d":
        # Creates inputs according to the 3d airfoil template
        cfg_data[15]  = 'KIND_TURB_MODEL= ' + Solver.turbulence_model + '\n'
        cfg_data[24]  = 'MACH_NUMBER= ' + str(Mach) + '\n'
        cfg_data[27]  = 'AOA= ' + str(AoA[k]) + '\n'
        cfg_data[41] = 'FREESTREAM_TEMPERATURE= ' + str(T_ref) + '\n'
        cfg_data[44] = 'REYNOLDS_NUMBER= ' + str(round(Re)) + '\n'
        cfg_data[47] = 'REYNOLDS_LENGTH= ' + str(Ref_values["Length"]) + '\n'
        cfg_data[90] = 'REF_ORIGIN_MOMENT_X= ' + str(Ref_values["Point"][2]) + '\n'
        cfg_data[95] = 'REF_LENGTH= ' + str(Ref_values["Length"]) + '\n'
        cfg_data[98] = 'REF_AREA= ' + str(Ref_values["Area"]) + '\n'
        if Solver.symmetric is True:
            # The case if a symmetry BC is used
            cfg_data[113] = 'MARKER_SYM= ( symmetry ) \n'
            cfg_data[219] = 'ITER= ' + str(Solver.max_iterations) + '\n'
            cfg_data[233] = 'CONV_CAUCHY_EPS= ' + str(Solver.tolerance) + '\n'
            cfg_data[239] = 'MESH_FILENAME= ' + Mesh.filename + '\n'
            cfg_data[241] = 'RESTART_SOL= ' + Solver.warmstart + '\n'
            cfg_data[243] = 'OUTPUT_WRT_FREQ= ' + str(Solver.save_frequency) + '\n'
        else:
            cfg_data[216] = 'ITER= ' + str(Solver.max_iterations) + '\n'
            cfg_data[230] = 'CONV_CAUCHY_EPS= ' + str(Solver.tolerance) + '\n'
            cfg_data[236] = 'MESH_FILENAME= ' + Mesh.filename + '\n'
            cfg_data[239] = 'RESTART_SOL= ' + Solver.warmstart + '\n'
            cfg_data[240] = 'OUTPUT_WRT_FREQ= ' + str(Solver.save_frequency) + '\n'
                       


    f = open(filename, 'w')
    for item in cfg_data:
        f.write(item)
    f.close()


    return filename



def run_SU2(processors,filename):
    ''' Runs SU2
    
        Inputs:
            SU2_settings                             Array of SU2 prescribed settings
            filename                                 Generated journal filename

        Outputs:
            

        Assumptions:

    '''

    # Run Fluent
    with open('SU2_output.log', 'w') as f:
        subprocess.call(['mpiexec', '-n',str(processors),'SU2_CFD', filename], stdout= f, stderr= None, stdin=subprocess.PIPE)

    return


def read_results(output_file):
    ''' Read output SU2 results 
    
        Inputs:
            output_file                      SU2 log file with output

        Outputs:
            Cl, Cd, Cm

        Assumptions:

    '''

    # Read results 
    with open(output_file, 'r') as f:
        last_line = f.readlines()[-35]

    results_array = last_line.split('|')

    Cl = float(results_array[-4])
    Cd = float(results_array[-5])
    Cm = float(results_array[-3])



    return Cl, Cd, Cm







def standard_atmosphere(Alt):
    ''' Computes temperature and pressure at a given altitude using standard atmosphere formulations

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




if __name__ == '__main__': 

    # Sample inputs
    # Input directory and names
    Ref_dir  = r'F:\TU_Braunschweig\Research\High_Alpha_airfoil_HLFC\root'        # Reference directory
    casefile = 'root_airfoil.cas' 


    # Input solver settings
    Solver_dim          = '2ddp'   
    Time_type           = 'Steady'
    Solver_type         = 'pressure-based'                                   #   pressure-based density-based-implicit
    Solver_method       = 'SIMPLEC'
    turbulence_model    = 'kw-sst'
    global_under_relax  = 0.5                                                # Global under-relaxation factor for all solver parameters     
    Courant_number      = 2.0                                                # Courant number (for density-based solvers)                                          
    num_proc            = 7                                                  # Number of processors
    save_freq           = 10
    conv_criteria       = 1e-5
    iterations          = 17000
    time_step           = 1e-4                                               # time step size for the transient solution
    read_only           = False                                              # handle to read the data only without running Fluent

    # Input sweeep data
    Alt_range   = np.array([0])                                                 # Altitude range in meters
    Mach_range  = np.array([0.2])                                   # Mach number range  0.4,0.5,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95
    AoA_range   = np.array([5.0])                                    # AoA range in degrees  ,1.0,2.0,3.0
    AoS_range   = np.array([0.2]) #np.linspace(0,11,11)                          # AoA range in degrees

    # Input reference values
    Area            = 6.4                                                         # Reference Area in sq m
    Length          = 6.4                                                         # Reference length in m   
    Depth           = 1                                                         # Reference depth (span) in m
    ref_point       = [0.25,0,0]                                                # Reference coordinate

    # Set inputs into lists
    #--------------------------------------------------------------------
    Ref_values = [Area, Length, Depth, ref_point[0], ref_point[1], ref_point[2]]    
    Fluent_settings = [Solver_dim, Solver_type, Solver_method, turbulence_model, global_under_relax, num_proc, save_freq, conv_criteria, iterations, Courant_number, Time_type, time_step]

    main(Alt_range,Mach_range,AoA_range,Fluent_settings,Ref_values,Ref_dir,casefile)    
