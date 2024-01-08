# miscellaneous_meshing.py
# 
# Created:  Dec 2023, S. Karpuk, 
# Modified: 
#           


# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# A collection of scripts that are commonly used for different meshes
# ----------------------------------------------------------------------


def create_header(Pointwise_settings):
    ''' Creates a Pointwise glyph header
        
            Inputs:
                Pointwise_settings - dictionary with Pointwise inputs


            Outputs:
            
     
            Assumptions:


        '''

    header = \
'''
# Fidelity Pointwise V18.6 Journal file - Sun Dec  3 17:40:02 2023

package require PWI_Glyph {0}

pw::Application setUndoMaximumLevels {1}
pw::Application reset
pw::Application markUndoLevel {{Journal Reset}}

pw::Application clearModified
            
'''

    import_header = header.format(Pointwise_settings["Glyph version"],Pointwise_settings["Max undo levels"])


    return import_header


def import_geometry(working_dir,Geometry_type,filename,geom_format):
    ''' Imports a geometry file
        
            Inputs:
                working_dir     - global working directory
                Geometry_type   - either airfils or wings
                filename        - geometry filename
                geom_format     - CAD format


            Outputs:
            

            
            Assumptions:
                The script was tested only on IGES files


        '''



    if Geometry_type == 'airfoil':

        base_case_text = \
'''

set _TMP(mode_1) [pw::Application begin DatabaseImport]
$_TMP(mode_1) initialize -strict -type Automatic {0}
$_TMP(mode_1) read
$_TMP(mode_1) convert
$_TMP(mode_1) end

'''
    else:

        base_case_text = \
'''

set _TMP(mode_1) [pw::Application begin DatabaseImport]
$_TMP(mode_1) initialize -strict -type Automatic {0}
$_TMP(mode_1) setAttribute SurfaceSplitDiscontinuous true
$_TMP(mode_1) setAttribute FileUnits Meters
$_TMP(mode_1) setAttribute ShellCellMode AsIs
$_TMP(mode_1) read
$_TMP(mode_1) convert
$_TMP(mode_1) end

'''

    geometry_dir = working_dir + "/Geometry_files/" + filename + '.' + geom_format
    import_text  = base_case_text.format(geometry_dir)


    return import_text

