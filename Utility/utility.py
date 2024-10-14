# collection of quality of live funktions

import os
import shutil
import subprocess

def overwrite_folder(folder_path):
    ''' Function to check if a specific folder exixts
        If folder exits User is asked if it should be overridden
        If folder does not exist it is created

    
        Inputs:
        folder_path    - Folder path

        Outputs:


    '''

    if os.path.exists(folder_path):
        choice = input(f"The Folder '{folder_path}' already exists. Do you want to override(y/n) or append (a)? Type (y/n/a): ").strip().lower()
        if choice == 'y':
            shutil.rmtree(folder_path)
            print(f"The Folder '{folder_path}' was overrdiden.")
            os.mkdir(folder_path)
        elif choice == 'n':
            quit("Override canceled. Execution terminated")
        elif choice == 'a':
            print(f"The Folder '{folder_path}' is not deleted. Files can be appended")
        else:
            quit("Unvalid input. Execution terminated")
    else:
        os.mkdir(folder_path)
    

def auto_copy_to_remote(config ,output_dir,case_output_dir_name):
    
    if config['solver_machine_name'] == config['remote_machine_1_name']:
        remote_machine_hostadress = config['remote_machine_1_hostadress']
        remote_machine_folderpath = config['remote_machine_1_folderpath']

    elif config['solver_machine_name'] == config['remote_machine_2_name']:
        remote_machine_hostadress = config['remote_machine_2_hostadress']
        remote_machine_folderpath = config['remote_machine_2_folderpath']

    else: 
        quit("No remote machine name name in config matching 'solver_machine_name' == " + config['solver_machine_name'])

    
    choice = input(f"Copy files to remote machine '{remote_machine_hostadress}' Type (y/n): ").strip().lower()


    if choice == 'y':
            print("Attempt to copy to remote")
            
            utility_dir   = os.path.dirname(__file__)
            location_Copy_to_remote = utility_dir + "/Copy_to_remote.sh"

            print(location_Copy_to_remote)
            #call_Copy_to_remote =f'../Setup_Tools&Templates/Copy_to_remote.sh {remote_machine_hostadress} {remote_machine_folderpath}'
            subprocess.call([location_Copy_to_remote, remote_machine_hostadress , remote_machine_folderpath, output_dir, case_output_dir_name])
            
    elif choice == 'n':
        quit("Copy canceled. Execution terminated")

    else:
        quit("Copy canceled. Unvalid input. Execution terminated")

