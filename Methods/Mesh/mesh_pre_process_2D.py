#mesh_pre_process.py

import numpy as np

'''Mesh pre-processing file

        Notes:
            1. define all paths with '/' both for Ubuntu and windows systems

    '''

def mesh_pre_process_2D(working_dir,Geometry,Mesh):

    '''Function to define dictionaries that will update the Glyph script
    
        Inputs:
            working_dir    - Working directory
            Geometry       - Geometric settings
                Mesh       - Mesh settings


        Outputs:
           

        Assumptions:

    '''

    Length          = Geometry.reference_values["Length"]
    scaling_factors = np.array([Length,Length,Length])

    Segment = Geometry.Segments[0]
    
    if len(Segment.TrailingEdgeDevice.PARSEC) == 0:
        # Data required for mesh_clean_airfoil_SU2.glf    
        Mesh.update_glyph_data = {
            "upper_surface_filename": working_dir + "/" + 'Geometry_files/' + Segment.Airfoil.files["upper"],
            "lower_surface_filename": working_dir + "/" + 'Geometry_files/' + Segment.Airfoil.files["lower"],
            "connector_dimensions"  : Mesh.airfoil_mesh_settings["connector dimensions"],
            "begin_spacing"         : Mesh.airfoil_mesh_settings["LE_spacing"],
            "end_spacing"           : Mesh.airfoil_mesh_settings["TE_spacing"],
            "su2meshed_file"        : working_dir + '/' + Mesh.filename,
            "run_iterations_1"      : Mesh.airfoil_mesh_settings["number of normal cells"],
            "run_iterations_2"      : "-1",
            "stop_at_height_1"      : "Off",
            "stop_at_height_2"      : Mesh.far_field,
            "scaling_factor"        : "{" + str(Length) + ' ' + str(Length) + ' ' + str(Length) +"}",  # Include the calculated scaling factors here
            "su2meshed_file"        : working_dir + "/" + Mesh.filename, 
        }

    #--------------------------------------------------------------------------------------------------------------
    else:
        # Data required for mesh_flapped_airfoil_SU2.glf

        # Normalize the the near-field
        R_NF1 = Mesh.airfoil_mesh_settings["near-field refinement radius 1"] / Length
        R_NF2 = Mesh.airfoil_mesh_settings["near-field refinement radius 2"] / Length    


        Mesh.update_glyph_data = {
            "upper_surface_filename"        : working_dir + "/" + 'Geometry_files/' + Segment.Airfoil.files["upper"],
            "lower_surface_filename"        : working_dir + "/" + 'Geometry_files/' + Segment.Airfoil.files["lower"],
            "cut1_filename"                 : working_dir + "/" + 'Geometry_files/' + Segment.TrailingEdgeDevice.files["flap cutout"][0], 
            "cut2_filename"                 : working_dir + "/" + 'Geometry_files/' + Segment.TrailingEdgeDevice.files["flap cutout"][1], 
            "flap_airfoil_lower_filename"   : working_dir + "/" + 'Geometry_files/' + Segment.TrailingEdgeDevice.files["lower surface file"],
            "flap_airfoil_upper_filename"   : working_dir + "/" + 'Geometry_files/' + Segment.TrailingEdgeDevice.files["upper surface file"],
            "connector_dimensions"          : Mesh.airfoil_mesh_settings["connector dimensions"],
            "spacing_127_130"               : Mesh.airfoil_mesh_settings["LE_spacing"],
            "spacing_137_140"               : Mesh.airfoil_mesh_settings["LE_spacing"],
            "spacing_146_149"               : Mesh.airfoil_mesh_settings["TE_spacing"],
            "spacing_156_159"               : Mesh.airfoil_mesh_settings["TE_spacing"], 
            "spacing_165_172"               : Mesh.airfoil_mesh_settings["LE_spacing"],  
            "spacing_178_184"               : Mesh.airfoil_mesh_settings["flap_cut_cluster"], 
            "spacing_192_195"               : Mesh.airfoil_mesh_settings["LE_flap_spacing"],
            "spacing_201_204"               : Mesh.airfoil_mesh_settings["TE_flap_spacing"],
            "spacing_211_214"               : Mesh.airfoil_mesh_settings["TE_flap_spacing"],
            "addPoint228"                   : "{ " + str(Mesh.far_field[0][1]) + " " + str(Mesh.far_field[1][1]) + " 0 }",
            "addPoint229"                   : "{ " + str(Mesh.far_field[0][1]) + " " + str(Mesh.far_field[1][0]) + " 0 }",
            "addPoint245"                   : "{ " + str(Mesh.far_field[0][0]) + " " + str(Mesh.far_field[1][0]) + " 0 }",
            "addPoint255"                   : "{ " + str(Mesh.far_field[0][0]) + " " + str(Mesh.far_field[1][1]) + " 0 }",
            "far_field_connector_dim"       : Mesh.airfoil_mesh_settings["far-field connectors"],
            "addPoint_287"                  : "{0.5 " + str(R_NF1) + " 0}",
            "addPoint_288"                  : "{0.5 0 0}",
            "EndAngle_289"                  : "360 {0 0 1}",
            "addPoint_298"                  : "{0.5 " + str(R_NF2) + " 0}",
            "addPoint_299"                  : "{0.5 0 0}",
            "EndAngle_300"                  : "360 {0 0 1}",
            "node_to_connector_313"         : Mesh.airfoil_mesh_settings["near-field nodes"], 
            "scaling_factor"                : "{" + str(Length) + ' ' + str(Length) + ' ' + str(Length) +"}",  # Include the calculated scaling factors here
            "BoundaryDecay_359"             : Mesh.airfoil_mesh_settings["near-field boundary decay 2"],
            "BoundaryDecay_384"             : Mesh.airfoil_mesh_settings["near-field boundary decay 1"], 
            "maxlayers_430"                 : Mesh.airfoil_mesh_settings["Max TREX layers"], 
            "fulllayers_431"                : Mesh.airfoil_mesh_settings["Full TREX layers"],
            "growthrate_433"                : Mesh.airfoil_mesh_settings["TREX growth rate"], 
            "BoundaryDecay_435"             : Mesh.airfoil_mesh_settings["near-field boundary decay 0"],
            "su2meshed_file"                : working_dir + "/" + Mesh.filename  
        }


    return #update_glyph_data

