#mesh_pre_process_3D.py
# 
# Created:  Dec 2023, S. Karpuk, 
# Modified: 
#           


# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------


class WingMeshPreProcess():

    def __init__(self):

        self.Pointwise_settings = {
            "Glyph version"   : '6.22.1',
            "Max undo levels" : 5            
        }


        self.segment_quilts = 3                     # Default number of quilts per wing segments
    

    def write_glyph_file(self,working_dir,Geometry,Mesh,Solver,Inviscid_flag):

        # Header default text

        header = \
'''
# Fidelity Pointwise V18.6 Journal file - Sun Dec  3 17:40:02 2023

package require PWI_Glyph {0}

pw::Application setUndoMaximumLevels {1}
pw::Application reset
pw::Application markUndoLevel {{Journal Reset}}

pw::Application clearModified
            
'''

        # Set up the number of quilts per segment based on the solver
        if Inviscid_flag is True:
           self.segment_quilts = 2
        else:
           self.segment_quilts = 3

        self.number_segments = len(Geometry.Segments.keys())

        # Read the entire content of the Glyph script
        with open(working_dir + '/' + Mesh.glyph_file, 'w') as glyph_script:

            # Create a glyph header 
            # -------------------------------------------------------------------
            glyph_script.write(header.format(self.Pointwise_settings["Glyph version"],self.Pointwise_settings["Max undo levels"]))

            # Import the geometry
            # -------------------------------------------------------------------
            glyph_script.write(self.import_geometry(working_dir,Geometry))

            # Assemble the model
            # -------------------------------------------------------------------
            self.assemble_wing_quilts(glyph_script,Geometry,Mesh)
            self.assemble_geometry(Mesh,glyph_script)

            # Create surface mesh
            # -------------------------------------------------------------------
            self.surface_mesh(Mesh,Geometry,glyph_script)

            # Create the far-field region
            # -------------------------------------------------------------------
            self.create_bounding_box_mesh(Mesh,glyph_script,Geometry)

            # Create the volume mesh
            # -------------------------------------------------------------------
            self.create_volume_mesh(Mesh,Geometry,glyph_script)

            # Assign the solver
            # -------------------------------------------------------------------
            self.set_solver(Solver,glyph_script)

            # Assign boundary coditions and export the mesh
            # -------------------------------------------------------------------
            self.create_boundary_conditions(glyph_script)
            self.export_mesh(Solver.working_dir,Mesh.filename,glyph_script)


            # Save the pointwise mesh file
            # -------------------------------------------------------------------
            self.save_mesh_file(Solver.working_dir,Mesh.pw_mesh_file,glyph_script)


            glyph_script.close()

        return

    def import_geometry(self,working_dir,Geometry):
        ''' Imports a geometry file and splits quilts
        
            Inputs:



            Outputs:
            

            
            Assumptions:
                The script was tested only on IGES files


        '''


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

        geometry_dir = working_dir + "/Geometry_files/" + Geometry.filename + '.' + Geometry.format
        import_text  = base_case_text.format(geometry_dir)


        return import_text





    def assemble_geometry(self,Mesh,file):
        ''' Writes a set of functions to assemble the wing model
        
            Inputs:


            Outputs:
            
            
            Assumptions:


        '''
        self.surface_count = (self.number_segments-1)*self.segment_quilts+3

        # Assemble the model
        self.database_list = ' '.join(['$_DB(' + str(i+1) + ')' for i in range(self.DB_count-1)])
        text_line = 'set _TMP(PW_1) [pw::Model assemble -reject _TMP(rejectEnts) -rejectReason _TMP(rejectReasons) -rejectLocation _TMP(rejectLocations) [list ' \
                    + self.database_list + ']]\n\n'
        file.write(text_line)


        return 



    def assemble_wing_quilts(self,filename,Geometry,Mesh):
        ''' Creates a list of quilts that fully describe the wing geometry
        
            Inputs:


            Outputs:       

            
            Assumptions:

        '''

        # Create quilts names for wing segments
        wing_surfaces = []
        self.DB_count = 0
        for i in range(self.segment_quilts):
            surface_name = self.create_wing_surface_name(self.number_segments,2*i+1,self.DB_count,Geometry.polynomial_fit)
            wing_surfaces.append(surface_name)
            filename.write(''.join(surface_name))
            if self.number_segments == 2 or Geometry.polynomial_fit> 2:
                self.DB_count += 1
            else:
                self.DB_count = (self.number_segments-1)*(i+1)

        # Close the rounded wingtip (3 surfaces)
        self.DB_count+=1
        self.total_segm_quiilt = 2*self.segment_quilts
        for i in range(3):
            quilt_index  = self.total_segm_quiilt + 2*i + 1
            surface_name = 'set _DB(' + str(self.DB_count) + ') [pw::DatabaseEntity getByName BSurf-' + str(quilt_index) + ']\n'
            wing_surfaces.append(surface_name)
            filename.write(surface_name)
            self.DB_count +=1

        Mesh.surface_names = wing_surfaces

        return 


    def create_wing_surface_name(self,segment_index,quilt_num,count,fit_index):
        ''' Creates a set of names for surfaces of upper, lower, or 
            trailing edge wing parts
        
            Inputs:


            Outputs:
            
       
            Assumptions:

        '''

        if segment_index == 2 or fit_index > 2:
            quilts = 'set _DB(' + str(count+1) + ') [pw::DatabaseEntity getByName BSurf-' + str(quilt_num) + ']\n'           
        else:
            quilts = ['set _DB(' + str(count+i+1) + ') [pw::DatabaseEntity getByName BSurf-' + str(quilt_num) + '-' + str(i) + ']\n' for i in range(segment_index-1)]

        return quilts


    def create_grid_entity(self,segment_index,quilt_num,count,fit_index):
        ''' Creates a domain grid entity vor volume meshing
        
            Inputs:


            Outputs:
            
       
            Assumptions:

        '''
        if segment_index == 2 or fit_index > 2:
            entity = 'set _DB(' + str(count+1) + ') [pw::GridEntity getByName BSurf-' + str(quilt_num) + '-quilt-dom]\n'
        else:
            entity = ['set _DB(' + str(count+i+1) + ') [pw::GridEntity getByName BSurf-' + str(quilt_num) + '-' + str(i) + '-quilt-dom]\n' for i in range(segment_index-1)]

        return entity

    def surface_mesh(self,Mesh,Geometry,file):
        ''' Creates a surface mesh set of commands
        
            Inputs:


            Outputs:
            
       
            Assumptions:
                The script uses the Pointwise Automatic Mesh Generator

        '''

        # Unpack inputs
        N_min_bound  = Mesh.global_surface_mesh_settings['Min boundary subdivisions']
        N_max_extent = Mesh.global_surface_mesh_settings['Max extents subdivisions']
        alpha_curve  = Mesh.global_surface_mesh_settings['Curvature resolution angle']
        Max_AR       = Mesh.global_surface_mesh_settings['Max aspect ratio']
        k_refine     = Mesh.global_surface_mesh_settings['Refinement factor']
        N_gap        = Mesh.global_surface_mesh_settings['Boundary gap subdivisions']

        N_TE         = Mesh.trailing_edge_meshing_settings['Trailing edge cells']
        k_conv       = Mesh.trailing_edge_meshing_settings['Convex spacing growth rate']
        Max_AR_TE    = Mesh.trailing_edge_meshing_settings['Max aspect ratio']
        k_space      = Mesh.trailing_edge_meshing_settings['Spacing factor']


        # Assign a model
        if self.number_segments == 2 or Geometry.polynomial_fit > 2:
            model_index = 1
        else:
            model_index = self.total_segm_quiilt+1
        file.write('set _DB(1) [pw::DatabaseEntity getByName BSurf-' + str(model_index) + '-model]\n \
set _TMP(mode_1) [pw::Application begin DatabaseMesher [list $_DB(1)]]')


        # Set global mesh parameters
        global_surface_params = \
'''
$_TMP(mode_1) setMinimumBoundarySubdivisions {0}
$_TMP(mode_1) setMaximumExtentsSubdivisions {1}
$_TMP(mode_1) setCurvatureResolutionAngle {2}
$_TMP(mode_1) setMaximumAspectRatio {3}
$_TMP(mode_1) setRefinementFactor {4}
$_TMP(mode_1) setBoundaryGapSubdivisions {5}
set _TMP(filter_1) Global
            
'''

        glob_suf_text = global_surface_params.format(N_min_bound,N_max_extent,
                                                      alpha_curve,Max_AR,k_refine,N_gap)

        file.write(glob_suf_text)

        # Define the trailing edge mapping region
        trailing_edge_meshing_params = \
'''
$_TMP(mode_1) addMappingFilter Automatic
$_TMP(mode_1) setMappingFilterName filter-1 TE
$_TMP(mode_1) setMappingFilterValue TE Force
$_TMP(mode_1) setMappingFilterValue TE {0}

'''

        # Assign wing surface quilts excluding the trailing edge
        #quilt_names = []
        for i in range(self.segment_quilts):
            if self.number_segments == 2 or Geometry.polynomial_fit > 2:
                #quilt_names.append(Mesh.surface_names[i][j][:-2] + '-quilt]\n')
                file.write(Mesh.surface_names[i][:-2] + '-quilt]\n')    
            else:            
                for j in range(self.number_segments-1):
                    #quilt_names.append(Mesh.surface_names[i][j][:-2] + '-quilt]\n')
                    file.write(Mesh.surface_names[i][j][:-2] + '-quilt]\n')

        if Mesh.trailing_edge_meshing_settings['Trailing edge mapping'] is True: 
            file.write(trailing_edge_meshing_params.format(N_TE))
            list_TE = []
            for i in range(self.number_segments-1): 
                list_TE.append('$_DB(' + str(self.DB_count-2-self.number_segments+i) + ')')    
            file.write('$_TMP(mode_1) setMappingFilterEntities TE [list '+ ' '.join(list_TE)  + ']')


        # Define leading and trailing edge boundary filters
        boundary_refinement_params = \
'''
$_TMP(mode_1) setBoundaryConvexUseGrowth false
$_TMP(mode_1) setBoundaryConvexSpacingFactor {0}  
$_TMP(mode_1) addBoundaryFilter
$_TMP(mode_1) setBoundaryFilterName bf-1 LETE
$_TMP(mode_1) setBoundaryFilterGrowthType LETE MaximumAspectRatio
$_TMP(mode_1) setBoundaryFilterSpacingFactor LETE {1}  
$_TMP(mode_1) setBoundaryFilterGrowthValue LETE {2}

'''

        file.write(boundary_refinement_params.format(k_conv,k_space,Max_AR_TE))
        curvature_connectors = []
        for i in range(self.number_segments-1):
            for j in range(self.segment_quilts):
                curvature_connectors.append('{BSurf-'+str(2*j+1)+'-'+str(i)+'-quilt BSurf-'+str(2*(self.number_segments-2-j)-1)+'-'+str(i)+'-quilt Curvature}')
        file.write('$_TMP(mode_1) setBoundaryFilterDefinition LETE [list ' + ' '.join(curvature_connectors) + ']\n')

        file.write('$_TMP(mode_1) createGridEntities Domain\n\
$_TMP(mode_1) setDomainAspectRatioThreshold ' + str(Max_AR) + '\n' + \
'$_TMP(mode_1) end\n\n')


        return 




    def create_bounding_box_mesh(self,Mesh,file,Geometry):
        ''' Defines a far-field domain and meshes its surfaces
            
                Inputs:


                Outputs:
                
        
                Assumptions:
                    The script uses the Pointwise Automatic Mesh Generator

        '''

        # Unpack inputs
        k_gr       = Mesh.boundary_layer_settings["Growth rate"]
        alpha_max  = Mesh.boundary_layer_settings["Max included angle"]
        FC_AR      = Mesh.boundary_layer_settings["Final cell aspect ratio"]
        CB         = Mesh.boundary_layer_settings["Collision buffer"]
        cent_skew  = Mesh.boundary_layer_settings["Centroid skewness"]


        # Define the bounding box
        TMP_mode = 'TMP(mode_1)' 

        wing_surfaces = []
        self.DB_count = 0
        count   = 0
        for i in range(self.segment_quilts):
            surface_name = self.create_grid_entity(self.number_segments,2*i+1,self.DB_count,Geometry.polynomial_fit)
            wing_surfaces.append(surface_name)
            file.write(''.join(surface_name))
            if self.number_segments == 2 or Geometry.polynomial_fit> 2:
                self.DB_count += 1
            else:
                self.DB_count = (self.number_segments-1)*(i+1)
            count += 1

        # Close the rounded wingtip (3 surfaces)
        self.DB_count+=1
        for i in range(3):
            quilt_index  = self.total_segm_quiilt + 2*i + 1
            surface_name = 'set _DB(' + str(self.DB_count) + ') [pw::GridEntity getByName BSurf-' + str(quilt_index) + '-quilt-dom]\n'
            wing_surfaces.append(surface_name)
            file.write(surface_name)
            self.DB_count +=1
            count += 1


        file.write('set _' + TMP_mode + ' [pw::Application begin VolumeMesher [list ' + ''.join(self.database_list) + ']]\n')


        bounding_surface_params = \
'''
$_TMP(mode_1) setFarfieldLength {{ {0} {1} }}
$_TMP(mode_1) setFarfieldWidth {{ {2} {3} }}
$_TMP(mode_1) setFarfieldHeight {{ {4} {5} }}
$_TMP(mode_1) setBoundaryLayerType GeometricGrowth
$_TMP(mode_1) setWallNormalSpacing {6}
$_TMP(mode_1) setGrowthRate {7}
$_TMP(mode_1) setMaxIncludedAngle {8}
$_TMP(mode_1) setFinalCellAspectRatio {9}
$_TMP(mode_1) setCollisionBuffer {10}
$_TMP(mode_1) setCentroidSkewness {11}
$_TMP(mode_1) createGridEntities
$_TMP(mode_1) end
            
'''

        file.write(bounding_surface_params.format(abs(Mesh.far_field[0][0]), abs(Mesh.far_field[0][1]), \
                                                  abs(Mesh.far_field[1][0]), abs(Mesh.far_field[1][1]), \
                                                  abs(Mesh.far_field[2][1]),abs(Mesh.far_field[2][1]),
                                                  Mesh.delta_s,k_gr,alpha_max,FC_AR,CB,cent_skew))




        return


    def create_volume_mesh(self,Mesh,Geometry,file):
        ''' Creates a volume mesh around the wing 
            
                Inputs:


                Outputs:
                
        
                Assumptions:
                    The script only works for viscous meshes so far

        '''

        # Unpack inputs
        Nmax        = Mesh.boundary_layer_settings["Max layers"] 
        Nfull       = Mesh.boundary_layer_settings["Full layers"]
        stop_flag   = Mesh.boundary_layer_settings["Stop if full layers not met"]
        inc_flag    = Mesh.boundary_layer_settings["Allow incomplete layers"]
        push_atr    = Mesh.boundary_layer_settings["Push attributes"]
        skew_equl   = Mesh.boundary_layer_settings["Skew criteria equiangle"]
        skew_centr  = Mesh.boundary_layer_settings["Centroid skewness"]
        growth_rate = Mesh.boundary_layer_settings["Growth rate"]
        Max_angle   = Mesh.boundary_layer_settings["Max included angle"]
        decay       = Mesh.boundary_layer_settings["Size field decay"]

        # Create an unstructured block
        TMP_mode = 'TMP(mode_2)' 

        file.write('pw::Application setGridPreference Unstructured\n')
        file.write('set _' + TMP_mode + ' [pw::Application begin Create]\n')
        file.write('set _BL(1) [pw::BlockUnstructured create]\n')


        wing_surfaces = []
        self.DB_count = 0
        count   = 0
        for i in range(self.segment_quilts):
            surface_name = self.create_grid_entity(self.number_segments,2*i+1,self.DB_count,Geometry.polynomial_fit)
            wing_surfaces.append(surface_name)
            file.write(''.join(surface_name))
            if self.number_segments == 2 or Geometry.polynomial_fit> 2:
                self.DB_count += 1
            else:
                self.DB_count = (self.number_segments-1)*(i+1)
            count += 1

        # Close the rounded wingtip (3 surfaces)
        self.DB_count+=1
        for i in range(3):
            quilt_index  = self.total_segm_quiilt + 2*i + 1
            surface_name = 'set _DB(' + str(self.DB_count) + ') [pw::GridEntity getByName BSurf-' + str(quilt_index) + '-quilt-dom]\n'
            wing_surfaces.append(surface_name)
            file.write(surface_name)
            self.DB_count +=1
            count += 1


        # Create a bounding box
        if     Mesh.trailing_edge_meshing_settings['Trailing edge mapping'] is True:
            ref_value  = self.number_segments
        else:
            ref_value = 1
        total_segm = (self.number_segments-1) * self.segment_quilts + 3 
        DB_list = []
        for i in range(6):
            entit_value = ref_value + i
            file.write('set _DB(' + str(total_segm+i+1) + ') [pw::GridEntity getByName dom-' + str(entit_value) + ']\n')
            DB_list.append('$_DB('+str(total_segm+i+1) + ')')

        file.write('set _TMP(face1)  [pw::FaceUnstructured createFromDomains [list ' + \
                   self.database_list + ' ' + ' '.join(DB_list) + ']]\n')
        file.write('$_BL(1) addFace $_TMP(face1)\n')
        file.write('$_TMP(mode_2) end\n\n')

        # Mesh the volume
        file.write('set _BL(2) [pw::GridEntity getByName blk-1]\n')
        Vol_mesh = \
'''
set _TMP(mode_2) [pw::Application begin UnstructuredSolver [list $_BL(2)]]
    $_BL(2) setUnstructuredSolverAttribute TRexMaximumLayers {0}
    $_BL(2) setUnstructuredSolverAttribute TRexFullLayers {1}
    $_BL(2) setUnstructuredSolverAttribute TRexGrowthRate {2}
    $_BL(2) setUnstructuredSolverAttribute TRexPushAttributes {3}
    $_BL(2) setUnstructuredSolverAttribute TRexSkewCriteriaCentroid {4}
    $_BL(2) setUnstructuredSolverAttribute TRexSkewCriteriaEquiangle {5}
    $_BL(2) setUnstructuredSolverAttribute TRexSkewCriteriaMaximumAngle {6}
    $_BL(2) setSizeFieldDecay {7}
    $_TMP(mode_2) setStopWhenFullLayersNotMet {8}
    $_TMP(mode_2) setAllowIncomplete {9}
    $_TMP(mode_2) run Initialize
$_TMP(mode_2) end

'''
        file.write(Vol_mesh.format(Nmax,Nfull,growth_rate,push_atr,skew_centr,
                                   skew_equl,Max_angle,decay,stop_flag,inc_flag))


        return



    def set_solver(self,Solver,file):
        ''' Assign the solver
            
                Inputs:


                Outputs:
                
        
                Assumptions:


        '''

        if Solver.dimensions == '3d':
            dimensions = 3
        else:
            dimensions = 2

        file.write('pw::Application setCAESolver ' + Solver.name + ' ' + str(dimensions) + '\n\n')



        return



    def create_boundary_conditions(self,file):
        ''' Assign boundary conditions
            
                Inputs:


                Outputs:
                
        
                Assumptions:
                    Only works for a wing with the symmetry plane

        '''
        BC_create_template = \
'''
set _TMP(PW_{0}) [pw::BoundaryCondition create] 
set _TMP(PW_{0}) [pw::BoundaryCondition getByName bc-{1}] 
$_TMP(PW_{0}) setName {2}
'''
        PW_count = 1
        bc_count = 2
        file.write(BC_create_template.format(PW_count,bc_count,'wall'))
        DB_indeces = []
        for i in range(self.DB_count-1):
            DB_indeces.append('[list $_BL(2) $_DB(' + str(i+1) + ')]')
        file.write('$_TMP(PW_' + str(PW_count) + ') apply [list '+  ' '.join(DB_indeces) + ']\n\n')
        PW_count += 1
        bc_count += 1

        file.write(BC_create_template.format(PW_count,bc_count,'symmetry'))
        file.write('$_TMP(PW_' + str(PW_count) + ') apply [list [list  $_BL(2) $_DB('+  str(self.DB_count+5) + ')]]\n\n')
        PW_count += 1
        bc_count += 1

        file.write(BC_create_template.format(PW_count,bc_count,'far_field'))
        far_field_indeces = []
        for i in range(5):
            far_field_indeces.append('[list  $_BL(2) $_DB(' + str(self.DB_count+i) + ')]')
        file.write('$_TMP(PW_' + str(PW_count) + ') apply [list '+  ' '.join(far_field_indeces) + ']\n\n')


        return


    def export_mesh(self,working_dir,mesh_file,file):
        ''' Exports the mesh
            
            Inputs:


            Outputs:
                
        
            Assumptions:
                The file is saved with the double precision

        '''

        export_template = \
'''
set _TMP(mode_2) [pw::Application begin CaeExport [pw::Entity sort [list $_BL(2)]]]
  $_TMP(mode_2) initialize -strict -type CAE {0}
  $_TMP(mode_2) setAttribute FilePrecision Double
  $_TMP(mode_2) verify
  $_TMP(mode_2) write
$_TMP(mode_2) end

'''

        file.write(export_template.format(working_dir + "/" + mesh_file))


        return
    


    def save_mesh_file(self,working_dir,mesh_file,file):
        ''' Saves the mesh file in the Pointwise format
            
            Inputs:


            Outputs:
                
        
            Assumptions:

        '''

        file.write('pw::Application save ' + working_dir + "/" + mesh_file)

        return








