#mesh_pre_process_2D.py
# 
# Created:  Dec 2023, S. Karpuk, 
# Modified: 
#     


# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import numpy as np
from Methods.Mesh.miscellaneous_meshing import  create_header,\
                                                import_geometry

class AirfoilMeshPreprocess():

    def __init__(self):

        self.Pointwise_settings = {
            "Glyph version"   : '6.22.1',
            "Max undo levels" : 5            
        }

    def write_glyph_file(self,working_dir,Geometry,Mesh,Solver,Inviscid_flag):


        with open(working_dir + '/' + Mesh.glyph_file, 'w') as glyph_script:

            # Create a glyph header 
            # -------------------------------------------------------------------
            glyph_script.write(create_header(self.Pointwise_settings))

            # Import the geometry
            # -------------------------------------------------------------------
            # Main airfoil parts
            for airfoil_file in Geometry.Segments[0].airfoil_files:  
                glyph_script.write(import_geometry(working_dir,Geometry.type,airfoil_file,'dat'))

            # Slotted arifoil parts
            if len(Geometry.Segments[0].TrailingEdgeDevice.files) != 0:
                for airfoil_file in Geometry.Segments[0].TrailingEdgeDevice.files:
                    glyph_script.write(import_geometry(working_dir,Geometry.type,airfoil_file,'dat'))

            # Create connectors
            # -------------------------------------------------------------------
            cn_id = 0
            db_id = 0
            if len(Geometry.Segments[0].TrailingEdgeDevice.files) != 0 and \
                   Geometry.Segments[0].TrailingEdgeDevice.type == 'Slotted':
                self.create_connectors(glyph_script,6)
                self.close_trailing_edge(glyph_script,[1,2],cn_id,db_id) 
                self.close_trailing_edge(glyph_script,[5,6],cn_id,db_id) 
            else:
                self.create_connectors(glyph_script,2)
                self.close_trailing_edge(glyph_script,[1,2],cn_id,db_id) 


            # Assign nodes to connectors and cluster the nodes 
            # -------------------------------------------------------------------                   
            self.assign_connector_nodes(glyph_script,Mesh)
            self.cluster_connector_nodes(glyph_script,Mesh,Geometry)


            # Scale the domain
            # -------------------------------------------------------------------
            self.scale_domain(glyph_script,Geometry)




            # Create the furface mesh
            # -------------------------------------------------------------------
                



            # Assign the solver
            # -------------------------------------------------------------------
                




            # Assign boundary coditions and export the mesh
            # -------------------------------------------------------------------
            



            # Save the pointwise mesh file
            # -------------------------------------------------------------------
            



            glyph_script.close()



        return
    


    def create_connectors(self,file,n_parts):
        ''' Creates a list of connector generatio inputs
        
            Inputs:


            Outputs:
            
       
            Assumptions:
 

        '''

        database_list = ' '.join(['$_DB(' + str(i+1) + ')' for i in range(n_parts)])
        for i in range(n_parts):
            file.write('set _DB('+str(i+1)+') [pw::DatabaseEntity getByName curve-'+str(i+1)+']\n')

        file.write('set _TMP(PW_1) [pw::Connector createOnDatabase -parametricConnectors Aligned \
                    -merge 0 -reject _TMP(unused) [list ' + ' '.join(database_list)  + ']]\n\n')


        return


    def assign_connector_nodes(self,file,Mesh):
        ''' Assigns nodes to conectors
        
            Inputs:


            Outputs:
            
       
            Assumptions:
                Nomenclature for typical airfpils:
                    Main airfoil upper surface           - 1
                    Main airfoil lower surface           - 2
                    Main airfoil trailing edge           - 3   
                 Numenclature for slotted flaps:
                    Main airfoil upper surface           - 1
                    Main airfoil lower surface           - 2
                    Main airfoil flap slot upper surface - 3
                    Main airfoil flap slot front surface - 4
                    Flap airfoil upper surface           - 5
                    Flap airfoil lower surface           - 6
                    Main airfoil trailing edge           - 7
                    Flap airfoil trailing edge           - 8 
        '''

        connector_dim = Mesh.airfoil_mesh_settings["connector dimensions"]
        for i in range(connector_dim):
            file.write('set _CN(' + str(i+1) + '[pw::GridEntity getByName con-' + \
                       str(i+1) + '] $_CN(' + str(i+1) + ') setDimension ' + str(connector_dim[i]) + '\n')


        return

    def scale_domain(self,file,Geometry):
        ''' Scales the airfoil domain according to its reference chord length
        
            Inputs:


            Outputs:
            
       
            Assumptions:
  
        '''

        if len(Geometry.Segments[0].TrailingEdgeDevice.files) != 0 and \
                   Geometry.Segments[0].TrailingEdgeDevice.type == 'Slotted':
            n_dom = 3
        else:
            n_dom = 8

        connector_list = ' '.join(['$_CN(' + str(i+1) + ')' for i in range(n_dom)])
        for i in range(n_dom):
            file.write('set _CN(' + str(i+1) + ') [pw::GridEntity getByName con-' + str(i+1) + ']\n')

        file.write('set _TMP(mode_1) [pw::Application begin Modify [list '+ \
                    ' '.join(connector_list)  + ']]\n\n')
        
        text_scale = \
'''
pw::Entity transform [pwu::Transform scaling -anchor {{0 0 0}} {{ {1} {1} {1} }}] [$_TMP(mode_1) getEntities]

'''
        file.write(text_scale.format(Geometry.reference_values['Length']))
        file.write('$_TMP(mode_1) end\n')

        return



    def cluster_connector_nodes(self,file,Mesh,Geometry):
        ''' Cluster airfoil conntector nodes
        
            Inputs:


            Outputs:
            
       
            Assumptions:
                Nomenclature for typical airfpils:
                    Main airfoil upper surface           - 1
                    Main airfoil lower surface           - 2
                    Main airfoil trailing edge           - 3                                       
                Nomenclature for slotted flaps:
                    Main airfoil upper surface           - 1
                    Main airfoil lower surface           - 2
                    Main airfoil flap slot upper surface - 3
                    Main airfoil flap slot front surface - 4
                    Flap airfoil upper surface           - 5
                    Flap airfoil lower surface           - 6
                    Main airfoil trailing edge           - 7
                    Flap airfoil trailing edge           - 8 
 
        '''

        # Unpack inputs
        LE_spacing = Mesh.airfoil_mesh_settings["LE_spacing"]
        TE_spacing = Mesh.airfoil_mesh_settings["TE_spacing"]  
        N_conn     = len(Mesh.airfoil_mesh_settings["connector dimensions"])


        # split between slotted and other flap types
        if len(Geometry.Segments[0].TrailingEdgeDevice.files) != 0 and \
                   Geometry.Segments[0].TrailingEdgeDevice.type == 'Slotted':

            flap_slot_space = Mesh.airfoil_mesh_settings["flap_cut_cluster"]
            LE_flap_spacing = Mesh.airfoil_mesh_settings["LE_flap_spacing"]
            TE_flap_spacing = Mesh.airfoil_mesh_settings["TE_flap_spacing"]

            for i in range(N_conn):
                file.write('set _CN(' + str(i+1) + ') [pw::GridEntity getByName con-' + str(i+1) + ']\n')    
            
            # Main airfoil leading edge spacing
            file.write('set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(2)]]\n')
            for i in range(2):
                file.write('set _TMP(PW_1) [$_CN(' + str(i+1) + ') getDistribution 1]\n \
                            $_TMP(PW_1) setBeginSpacing ' + str(LE_spacing) + '\n')
            file.write('$_TMP(mode_1) end\n')
                
            # Main airfoil trailing edge spacing
            file.write('set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(3)]]\n')               
            file.write('set _TMP(PW_1) [$_CN(1) getDistribution 1]\n $_TMP(PW_1) setBeginSpacing ' + str(TE_spacing) + '\n')
            file.write('set _TMP(PW_1) [$_CN(3) getDistribution 1]\n $_TMP(PW_1) setBeginSpacing ' + str(TE_spacing) + '\n')
            file.write('$_TMP(mode_1) end\n')

            # Flap slot spacing
            file.write('set _TMP(mode_1) [pw::Application begin Modify [list $_CN(3) $_CN(4)]]\n')
            for i in range(3,5):        
                file.write('set _TMP(PW_1) [$_CN(' + str(i) + ') getDistribution 1]\n \
                            $_TMP(PW_1) setBeginSpacing ' + str(flap_slot_space) + '\n')
                file.write('set _TMP(PW_1) [$_CN(' + str(i) + ') getDistribution 1]\n \
                            $_TMP(PW_1) setEndSpacing ' + str(flap_slot_space) + '\n')
            file.write('$_TMP(mode_1) end\n')

            # Flap airfoil spacing
            file.write('set _TMP(mode_1) [pw::Application begin Modify [list $_CN(5) $_CN(6)]]\n')    
            for i in range(5,7): 
                file.write('set _TMP(PW_1) [$_CN(' + str(i) + ') getDistribution 1]\n \
                            $_TMP(PW_1) setBeginSpacing ' + str(LE_flap_spacing) + '\n')
                file.write('set _TMP(PW_1) [$_CN(' + str(i) + ') getDistribution 1]\n \
                            $_TMP(PW_1) setEndSpacing ' + str(TE_flap_spacing) + '\n')
            file.write('$_TMP(mode_1) end\n')

            # Blunt trailing edge spacing
            file.write('set _TMP(mode_1) [pw::Application begin Modify [list $_CN(7) $_CN(8)]]\n')
            file.write('set _TMP(PW_1) [$_CN(7) getDistribution 1]\n $_TMP(PW_1) setBeginSpacing ' + str(TE_spacing) + '\n')
            file.write('set _TMP(PW_1) [$_CN(8) getDistribution 1]\n $_TMP(PW_1) setBeginSpacing ' + str(TE_flap_spacing) + '\n')
            file.write('set _TMP(PW_1) [$_CN(7) getDistribution 1]\n $_TMP(PW_1) setEndSpacing ' + str(TE_spacing) + '\n')
            file.write('set _TMP(PW_1) [$_CN(8) getDistribution 1]\n $_TMP(PW_1) setEndSpacing ' + str(TE_flap_spacing) + '\n')
            file.write('$_TMP(mode_1) end')

        else:

            # Assign surface connectors
            for i in range(2):
                file.write('set _CN(' + str(i+1) + ') [pw::GridEntity getByName con-' + str(i+1) + ']\n')    
            file.write('set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(2)]]\n')
            for i in range(2):
                file.write('set _TMP(PW_1) [$_CN(' + str(i+1) + ') getDistribution 1]\n \
                            $_TMP(PW_1) setBeginSpacing ' + str(LE_spacing) + '\n')
                file.write('set _TMP(PW_1) [$_CN(' + str(i+1) + ') getDistribution 1]\n \
                            $_TMP(PW_1) setEndSpacing ' + str(TE_spacing) + '\n')
            file.write('$_TMP(mode_1) end')  
            
            # Blunt trailing edge spacing
            file.write('set _TMP(mode_1) [pw::Application begin Modify [list $_CN(3)]]\n')
            file.write('set _TMP(PW_1) [$_CN(3) getDistribution 1]\n $_TMP(PW_1) setBeginSpacing ' + str(TE_spacing) + '\n')
            file.write('set _TMP(PW_1) [$_CN(3) getDistribution 1]\n $_TMP(PW_1) setEndSpacing ' + str(TE_spacing) + '\n')

        file.write('$_TMP(mode_1) end')

        return



    def close_trailing_edge(self,file,conn_num,cn_id,db_id):
        ''' Creates a trailing edge connector
        
            Inputs:


            Outputs:
            
       
            Assumptions:
 

        '''

        connector_text = \
'''
set _TMP(mode_1) [pw::Application begin Create]
set _TMP(PW_1) [pw::SegmentSpline create]
set _CN({2}) [pw::GridEntity getByName con-{0}]
set _DB({3}) [pw::DatabaseEntity getByName curve-{0}]
set _CN({4}) [pw::GridEntity getByName con-{1}]
set _DB({5}) [pw::DatabaseEntity getByName curve-{1}]
$_TMP(PW_1) addPoint [$_CN({2}) getPosition -arc 1]
$_TMP(PW_1) addPoint [$_CN({4}) getPosition -arc 0]
set _CN({6}) [pw::Connector create]
$_CN({6}) addSegment $_TMP(PW_1)
unset _TMP(PW_1)
$_CN({6}) calculateDimension
$_TMP(mode_1) end

'''

        file.write(connector_text.format(conn_num[0],conn_num[1],cn_id+1,
                                         db_id+1,cn_id+2,db_id+2,cn_id+3))

        cn_id += 3
        db_id += 2

        return cn_id, db_id
    

    # Close the trailing edge of the main airfoil and the flap
'''set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  set _CN(1) [pw::GridEntity getByName con-1]
  set _DB(1) [pw::DatabaseEntity getByName curve-1]
  set _CN(2) [pw::GridEntity getByName con-3]
  set _DB(2) [pw::DatabaseEntity getByName curve-3]
  $_TMP(PW_1) addPoint [$_CN(1) getPosition -arc 1]
  $_TMP(PW_1) addPoint [$_CN(2) getPosition -arc 0]
  set _CN(3) [pw::Connector create]
  $_CN(3) addSegment $_TMP(PW_1)
  unset _TMP(PW_1)
  $_CN(3) calculateDimension
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  $_TMP(PW_1) delete
  unset _TMP(PW_1)
$_TMP(mode_1) abort
unset _TMP(mode_1)
set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  set _CN(4) [pw::GridEntity getByName con-6]
  set _DB(3) [pw::DatabaseEntity getByName curve-6]
  set _CN(5) [pw::GridEntity getByName con-5]
  set _DB(4) [pw::DatabaseEntity getByName curve-5]
  $_TMP(PW_1) addPoint [$_CN(4) getPosition -arc 1]
  $_TMP(PW_1) addPoint [$_CN(5) getPosition -arc 0]
  set _CN(6) [pw::Connector create]
  $_CN(6) addSegment $_TMP(PW_1)
  unset _TMP(PW_1)
  $_CN(6) calculateDimension
$_TMP(mode_1) end
'''


