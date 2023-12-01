# Fluent_sweeps.py
# 
# Created:  Aug 2022, S. Karpuk
# Modified:
#
# Runs the Fluent aerodynamic analysis sweep for airfoils, wings, and aircraft

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


def main(Alt_range,Mach_range,AoA_range,Fluent_settings,Ref_values,Ref_dir,casefile):
    ''' 
        Available sweeps:
            Altitude
            Mach
            anagle-of-attach
            slideslip angle (for 3D solutions)


        Inputs:
            Solver_dim                                  Solver dimension
            Solver_type                                 Solver type
            Solver_method                               Solver method
            global_under_relax                          Under-relaxation coefficient wrt default values
            num_proc                                    Number of processors used fot the solution
            Alt_range                                   Analysis altitudes
            Mach_range                                  Range of Mach numbers
            AoA_range                                   Range of angles-of-attack
            AoS_range                                   Range of sideslip angles
            Ref_dir                                     Solution refefence directory
            turbulence_model                            Turbulence model
            save_freq                                   Data saving frequency in number of iterations
            conv_criteria                               Global residual convergence criteria 
            iterations                                  Number of iterations to converge the solution

        Outputs:
            CL, CD, CM, CN, Cl


        Assumptions:
            1. Compressible flow solvers
            2. Steady-state solutions
            3. Under-relaxation factors are scaled globally
            4. Spatial discretizations are maintained by default (Gradients are Least Squares and others are 2nd Order)
            5. Boundary conditions assume a a pressure far-field everywhere
            6. Reference axes:
                2D:     X - horizontal (chordwise)
                        Y - vertical
                3D:     X - horizontal (chordwise)
                        Y - spanwise
                        Z - vertical
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

    # Unpack inpute
    Solver_dim = Fluent_settings[0]

    # Create Fluent journal file for sweeps
    #--------------------------------------------------------------------
    len_Alt  = len(Alt_range)
    len_Mach = len(Mach_range)
    len_AoA  = len(AoA_range)
    if Solver_dim == '2ddp' or Solver_dim == '2d': 
        Cl = np.zeros((len_Alt,len_Mach,len_AoA))                               # Array of Cl
        Cd = np.zeros((len_Alt,len_Mach,len_AoA))                               # Array of Cd
        Cm = np.zeros((len_Alt,len_Mach,len_AoA))                               # Array of Cm

        for i in range(len_Alt):
            for j in range(len_Mach):
                for k in range(len_AoA): 

                    # Run the solution

                    # Create a Journal file
                    filename = run_2d_Fluent_journal(Alt_range[i],Mach_range[j],AoA_range[k],\
                                                            Fluent_settings,Ref_values,Ref_dir,casefile)
                
                    # Run Fluent
                    new_direct  = 'Case_alt' + str("{:.2f}".format(Alt_range[i])) + '_Mach' + str("{:.2f}".format(Mach_range[j])) + '_AoA' + str("{:.2f}".format(AoA_range[k]))
                    file_direct = os.path.join(Ref_dir, new_direct)

                    os.chdir(file_direct)

                    print('Running Solution ' + filename)
                    run_Fluent(Fluent_settings,filename)
                    print('Solution ' + filename + ' Completed')

                    # Read results
                    Cl[i,j,k],Cd[i,j,k],Cm[i,j,k] = read_results(Solver_dim)

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




def run_2d_Fluent_journal(Alt,Mach,AoA,Fluent_settings,Ref_values,Ref_dir,casefile):
    ''' Creates a 2D case Fluent journal file for airfoils
    
        Inputs:
            Fluent_settings                             Array of fluent prescribed settings
            Alt                                         Altitudes
            Mach                                        Mach number
            AoA                                         Angle-of-attack
            Ref_dir                                     Reference directory
            Ref_values                                  Reference values
            casefile                                    case file name


        Outputs:
            filename                                    Generated journal filename


        Assumptions:

    '''

    # Compute standard atmospheric properties
    p_ref, T_ref = standard_atmosphere(Alt)

    # Create run directories and copy the case file there
    if AoA < 0:
        new_direct  = 'Case_alt' + str("{:.2f}".format(Alt)) + '_Mach' + str("{:.2f}".format(Mach)) + '_AoA_' + str("{:.2f}".format(abs(AoA)))
    else:    
        new_direct  = 'Case_alt' + str("{:.2f}".format(Alt)) + '_Mach' + str("{:.2f}".format(Mach)) + '_AoA' + str("{:.2f}".format(AoA))
    filename    = new_direct + '.jou'
    file_direct = os.path.join(Ref_dir, new_direct)


    if os.path.exists(file_direct) and os.path.isdir(file_direct):
        shutil.rmtree(file_direct)
    os.mkdir(file_direct)

    shutil.copy(Ref_dir + '\\' + casefile, file_direct + '\\' + casefile)                                                             # copies the case file from the reference folder to the target one


    os.chdir(file_direct)
    
    f = open(filename, 'w')
    f.write('; Reading in the case file \n')
    f.write('/file/read-case ' + file_direct + '\\' + casefile + '\n\n')

    if Fluent_settings[-2] == 'Transient':
        f.write('; Define transient solution \n /define/models/unsteady-2nd-order \n yes \n\n')

    f.write('; Define the CFD solver \n/define/models/energy \nyes \nyes \nyes \n\n')
    f.write('; Define the CFD solver \n/define/models/energy \nyes \nyes \nyes \n\n')
    f.write('/define/models/solver/'  + str(Fluent_settings[1] + '\nyes \n\n'))
    f.write('/define/models/viscous/' + str(Fluent_settings[3] + '\nyes \n\n'))
    f.write('; Define the fluid material \n/define/materials/change-create/air \nair \nyes \nideal-gas \nno \nno \nno \nno \nno \nno \n\n')
    
    f.write('; Define operating and boundary conditions \n/define/operating-conditions/operating-pressure\n')
    f.write(str("{:.1f}".format(p_ref)) + '\n\n')
    f.write('/define/boundary-conditions/pressure-far-field \nfar-field \nno \n0 \nno\n')
    f.write(str("{:.2f}".format(Mach)) + '\nno \n')
    f.write(str("{:.1f}".format(T_ref)) + '\nno \n')
    f.write(str(np.cos(np.radians(AoA))) + '\nno \n')
    f.write(str(np.sin(np.radians(AoA))) + '\nno \n')

    if Fluent_settings[3] == 'kw-sst':
        f.write('no \nyes \n5 \n10 \n\n')   
        f.write('/define/boundary-conditions/wall \nwall \n0 \nno \n0 \nno \nno \nno \n0 \nno \nno \nno \nno \n0 \nno \n0.5 \nno \n1 \n\n')   
    elif Fluent_settings[3] == 'spalart-allmaras':
        f.write('no \nyes \nno \n10 \n\n')   
        f.write('/define/boundary-conditions/wall \nwall \n0 \nno \n0 \nno \nno \nno \n0 \nno \nno \nno \nno \n0 \nno \n0.5 \nno \n1 \n\n')


    f.write('; Define reference values \n')
    f.write('/report/reference-values/compute/pressure-far-field \nfar-field \n')
    f.write('/report/reference-values/area \n')
    f.write(str(Ref_values[0]) + '\n')
    f.write('/report/reference-values/length \n')
    f.write(str(Ref_values[1]) + '\n')
    f.write('/report/reference-values/depth \n')
    f.write(str(Ref_values[2]) + '\n\n')
    f.write('; Define discretization methods\n')
    if Fluent_settings[1] == 'pressure-based':

        # Define solver for pressure lowspeed solutions (subsonic flow) 
        f.write('/solve/set/p-v-coupling \n')

        # Define the discretization method number  
        def solver_set(x):
            switcher = {
                'SIMPLE' : 20,
                'SIMPLEC': 21,
                'PISO'   : 22,
                'Coupled': 24
            }
            return switcher.get(x,"Invalid Option!")

        f.write(str(solver_set(Fluent_settings[2])) + '\n')

        if Fluent_settings[2] == 'SIMPLE' or Fluent_settings[2] == 'SIMPLEC':

            f.write('/solve/set/under-relaxation/pressure \n')
            f.write(str(0.3*Fluent_settings[4]) + '\n')
            f.write('/solve/set/under-relaxation/density \n')
            f.write(str(1.0*Fluent_settings[4]) + '\n')
            f.write('/solve/set/under-relaxation/body-force \n')
            f.write(str(1.0*Fluent_settings[4]) + '\n')
            f.write('/solve/set/under-relaxation/mom \n')
            f.write(str(0.7*Fluent_settings[4]) + '\n')
            f.write('/solve/set/under-relaxation/turb-viscosity \n')
            f.write(str(1.0*Fluent_settings[4]) + '\n')
            f.write('/solve/set/under-relaxation/temperature \n')
            f.write(str(1.0*Fluent_settings[4]) + '\n\n') 

            if Fluent_settings[3] == 'spalart-allmaras':
                f.write('/solve/set/under-relaxation/nut \n')
                f.write(str(0.8*Fluent_settings[4]) + '\n')

            elif Fluent_settings[3] == 'transition-sst' or 'kw-sst':
                f.write('/solve/set/under-relaxation/k \n')
                f.write(str(0.8*Fluent_settings[4]) + '\n')
                f.write('/solve/set/under-relaxation/omega \n')
                f.write(str(0.8*Fluent_settings[4]) + '\n')

                if  Fluent_settings[2] == 'transition-sst':
                    f.write('/solve/set/under-relaxation/intermit \n')
                    f.write(str(0.8*Fluent_settings[4]) + '\n')
                    f.write('/solve/set/under-relaxation/retheta \n')
                    f.write(str(0.8*Fluent_settings[4]) + '\n')
 
        else:
            # Other models
            f.write('/solve/set/under-relaxation/body-force \n')
            f.write(str(1.0*Fluent_settings[4]) + '\n')
            f.write('/solve/set/under-relaxation/k \n')
            f.write(str(0.8*Fluent_settings[4]) + '\n')
            f.write('/solve/set/under-relaxation/omega \n')
            f.write(str(0.8*Fluent_settings[4]) + '\n')
            f.write('/solve/set/under-relaxation/turb-viscosity \n')
            f.write(str(1.0*Fluent_settings[4]) + '\n')
            f.write('/solve/set/under-relaxation/density \n')
            f.write(str(1.0*Fluent_settings[4]) + '\n\n')                

    else:
        # Define the discretization for transonic or supersonic flows

        f.write('/solve/set/courant-number \n')   
        f.write(str(Fluent_settings[-3]) + '\n\n') 

        f.write('/solve/set/under-relaxation/nut \n')
        f.write(str(0.8*Fluent_settings[4]) + '\n')
        f.write('/solve/set/under-relaxation/solid \n')
        f.write(str(1.0*Fluent_settings[4]) + '\n')       
        f.write('/solve/set/under-relaxation/turb-viscosity \n')
        f.write(str(1.0*Fluent_settings[4]) + '\n')   


    f.write('; Report definitions \n')
    f.write('/solve/report-definitions/add \ncd \ndrag \nforce-vector \n')
    f.write(str(np.cos(np.radians(AoA))) + '\n')
    f.write(str(np.sin(np.radians(AoA))) + '\n')
    f.write('thread-names \nwall \n\nq \n\n')

    f.write('/solve/report-definitions/add \ncl \nlift \nforce-vector \n')
    f.write(str(-np.sin(np.radians(AoA))) + '\n')
    f.write(str(np.cos(np.radians(AoA))) + '\n')
    f.write('thread-names \nwall \n\nq \n \n')

    f.write('/solve/report-definitions/add \ncm \nmoment \nmom-axis \n')
    f.write('0 \n0 \n1 \n')
    f.write('mom-center \n')
    f.write(str(Ref_values[3]) + '\n' + str(Ref_values[4]) + '\n')
    f.write('thread-names \nwall \n\nq \n\n')

    f.write('/solve/report-files/add \naero_report \n')
    f.write('file-name \naero_report.out \n')
    f.write('frequency \n' + str(Fluent_settings[-6]) + '\n')
    f.write('print \nyes \nreport-defs \ncl \ncd \ncm \n\nq \n\n')

    f.write('/solve/monitors/residual/convergence-criteria \n')
    for i in range(8):
        f.write(str(Fluent_settings[-5]) + '\n')

    f.write('q\nq\nq\n; Initialize the solution and Solve the case\n\n')
    if Fluent_settings[-2] == 'Transient':
       f.write('/solve/set/transient-controls/fixed-user-specified \n yes \n\n')
       f.write('/solve/set/transient-controls/max-iterations-per-time-step \n 100 \n\n')
       f.write('/solve/set/transient-controls/number-of-time-steps\n' + str(Fluent_settings[-4]) + '\n\n')
       f.write('/solve/set/transient-controls/time-step-size\n' + str(Fluent_settings[-1]) + '\n\n')
       f.write('/solve/initialize/initialize-flow\n\n')   
       f.write('/solve/dual-time-iterate  \n' + str(Fluent_settings[-4]) + '\n 100' + '\n\n')
    else: 
        f.write('/solve/initialize/hyb-initialization \n\n')      
        f.write('/solve/iterate \n' + str(Fluent_settings[-4]) + '\n\n')

    f.write('; Save the case and data \n')
    f.write('/file/write-case-data \n')
    f.write(file_direct + '\\' + casefile + '.h5 \n\n')
    f.write('exit \nOK\n\n')

    f.close


    return filename


def run_Fluent(Fluent_settings,filename):
    ''' Runs ANSYS Fluent
    
        Inputs:
            Fluent_settings                             Array of fluent prescribed settings
            filename                                    Generated journal filename

        Outputs:
            

        Assumptions:

    '''

    # Run Fluent
    with open('Fluent_output.log', 'w') as f:
        subprocess.call(['fluent ', Fluent_settings[0],'-g', '-t'+str(Fluent_settings[5]), '-i', filename], stdout= f, stderr= None, stdin=subprocess.PIPE)

    return


def read_results(Fluent_dim):
    ''' Read output Fluent results 
    
        Inputs:
            Fluent_dim                      Fluent solution dimension

        Outputs:
            Cl, Cd, Cm

        Assumptions:

    '''

    # Read results 
    with open('aero_report.out', 'r') as f:
        last_line = f.readlines()[-1]

    results_array = last_line.split()

    if Fluent_dim == '2ddp' or Fluent_dim == '2d': 
        Cl = float(results_array[1])
        Cd = float(results_array[2])
        Cm = float(results_array[3])



    return Cl, Cd, Cm






def run_3d_Fluent():
    ''' Creates a 3D case Fluent journal file for airfoils and runs the case 
    
        Inputs:
            Fluent_settings                             Array of fluent prescribed settings
            Alt                                         Altitudes
            Mach                                        Mach number
            AoA                                         Angle-of-attack


        Outputs:
            


        Assumptions:

    '''



    return




def standard_atmosphere(Alt):
    ''' Computes temperature and pressure at a given altitude using standard atmosphere formulations

        Inputs:
            Alt                 Altitude in m

        Outputs:
            T                   Temperature in K
            p                   Pressure in Pa
            

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


    return p, T




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
    AoA_range   = np.array([14.5,15.5,16.0])                                    # AoA range in degrees  ,1.0,2.0,3.0
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
