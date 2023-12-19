# mesh_pre_process_Quasi3D.py
# 
# Created: Dec 2023, S. Holenarsipura M Madhava
# Modified:

# ----------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------
from Input_data import Geometry 



class Q3DMeshPreProcess():

    if Geometry.flap is False:

        def write_glyph_file(self, working_dir, Geometry, Mesh, Solver, update_glyph_data):
    

                # Header default text

                header = '''
# Extruding the mesh - Clean Airfoil

package require PWI_Glyph 6.22.1

pw::Application setUndoMaximumLevels 5

pw::Application setCAESolver CGNS 2
pw::Application markUndoLevel {Select Solver}

pw::Application setCAESolver CGNS 3
pw::Application markUndoLevel {Set Dimension 3D}
                        '''
                



        def create_extrusion(self, update_glyph_data):   
            Extrusion_direction = update_glyph_data["Extrusion_direction"]
            Extrusion_distance = update_glyph_data["Extrusion_distance"]
            Extrusion_steps = update_glyph_data["Extrusion_steps"]
                    
            extrusion = f'''

set _TMP(mode_1) [pw::Application begin Create]
set _DM(1) [pw::GridEntity getByName dom-1]
set _TMP(PW_1) [pw::FaceStructured createFromDomains [list $_DM(1)]]
set _TMP(face_1) [lindex $_TMP(PW_1) 0]
unset _TMP(PW_1)
set _BL(1) [pw::BlockStructured create]
$_BL(1) addFace $_TMP(face_1)
$_TMP(mode_1) end
unset _TMP(mode_1)
set _TMP(mode_1) [pw::Application begin ExtrusionSolver [list $_BL(1)]]
$_TMP(mode_1) setKeepFailingStep true
$_BL(1) setExtrusionSolverAttribute Mode Translate
$_BL(1) setExtrusionSolverAttribute TranslateDirection {{1 0 0}}
$_BL(1) setExtrusionSolverAttribute TranslateDirection {{{{Extrusion_direction}}}}
$_BL(1) setExtrusionSolverAttribute TranslateDistance {{{{Extrusion_distance}}}}
$_TMP(mode_1) run {{{{Extrusion_steps}}}}
$_TMP(mode_1) end
unset _TMP(mode_1)
unset _TMP(face_1)
pw::Application markUndoLevel {{Extrude, Translate}}
'''


                        
        
        
        def create_boundary_conditions(self, update_glyph_data):                  
                        
            boundary = '''           
pw::Application setCAESolver SU2 3
pw::Application markUndoLevel {Select Solver}

set _DM(2) [pw::GridEntity getByName dom-3]
set _DM(3) [pw::GridEntity getByName dom-4]
set _DM(4) [pw::GridEntity getByName dom-2]
set _TMP(PW_1) [pw::BoundaryCondition getByName wall]
$_TMP(PW_1) apply [list [list $_BL(1) $_DM(2)] [list $_BL(1) $_DM(3)] [list $_BL(1) $_DM(4)]]
pw::Application markUndoLevel {Set BC}

set _DM(5) [pw::GridEntity getByName dom-6]
set _TMP(PW_2) [pw::BoundaryCondition getByName far-field]
$_TMP(PW_2) apply [list [list $_BL(1) $_DM(5)]]
pw::Application markUndoLevel {Set BC}

set _TMP(PW_3) [pw::BoundaryCondition create]
pw::Application markUndoLevel {Create BC}

unset _TMP(PW_3)
set _DM(6) [pw::GridEntity getByName dom-8]
set _TMP(PW_3) [pw::BoundaryCondition getByName bc-4]
$_TMP(PW_3) apply [list [list $_BL(1) $_DM(6)] [list $_BL(1) $_DM(1)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_3) setName symmetry
pw::Application markUndoLevel {Name BC}
                    '''
                        
                        
                        
                        
        def save_mesh_file(self, update_glyph_data, working_dir, Mesh):       
            su2meshed_file = update_glyph_data["su2meshed_file"]          
            
            save_file = f'''
unset _TMP(PW_1)
unset _TMP(PW_2)
unset _TMP(PW_3)
set _DM(7) [pw::GridEntity getByName dom-5]
set _TMP(mode_1) [pw::Application begin CaeExport [pw::Entity sort [list $_BL(1) $_DM(1) $_DM(4) $_DM(2) $_DM(3) $_DM(7) $_DM(5) $_DM(6)]]]
$_TMP(mode_1) initialize -strict -type CAE {su2meshed_file!r}
$_TMP(mode_1) setAttribute FilePrecision Double
$_TMP(mode_1) verify
$_TMP(mode_1) write
$_TMP(mode_1) end
unset _TMP(mode_1)
'''


    
    
    
    
    
    
    
    
    
    else:
            def write_glyph_file(self, working_dir, Geometry, Mesh, Solver, update_glyph_data):
    

                # Header default text


                header = '''
# Extrude the mesh - Flapped Airfoil

package require PWI_Glyph 6.22.1

pw::Application setUndoMaximumLevels 5

pw::Application setCAESolver CGNS 2
pw::Application markUndoLevel {Select Solver}

pw::Application setCAESolver CGNS 3
pw::Application markUndoLevel {Set Dimension 3D}
                            '''
                


            def create_extrusion(self, update_glyph_data):   
                Extrusion_direction    = update_glyph_data["Extrusion_direction"]
                Extrusion_distance     = update_glyph_data["Extrusion_distance"]
                Extrusion_steps        = update_glyph_data["Extrusion_steps"]
                
                
                extrusion = '''
set _TMP(mode_1) [pw::Application begin Create]
set _DM(1) [pw::GridEntity getByName dom-1]
set _DM(2) [pw::GridEntity getByName dom-3]
set _DM(3) [pw::GridEntity getByName dom-2]
set _TMP(PW_1) [pw::FaceUnstructured createFromDomains [list $_DM(1) $_DM(2) $_DM(3)]]
set _TMP(face_1) [lindex $_TMP(PW_1) 0]
unset _TMP(PW_1)
set _BL(1) [pw::BlockExtruded create]
$_BL(1) addFace $_TMP(face_1)
$_TMP(mode_1) end
unset _TMP(mode_1)
set _TMP(mode_1) [pw::Application begin ExtrusionSolver [list $_BL(1)]]
$_TMP(mode_1) setKeepFailingStep true
$_BL(1) setExtrusionSolverAttribute Mode Translate
$_BL(1) setExtrusionSolverAttribute TranslateDirection {1 0 0}
$_BL(1) setExtrusionSolverAttribute TranslateDirection {{{}}}
$_BL(1) setExtrusionSolverAttribute TranslateDistance {{{}}}
$_TMP(mode_1) run {{{}}}
$_TMP(mode_1) end
unset _TMP(mode_1)
unset _TMP(face_1)
pw::Application markUndoLevel {Extrude, Translate}

'''.format(Extrusion_direction, Extrusion_distance, Extrusion_steps)

                        
            def create_boundary_conditions(self, update_glyph_data):                  
                            
                boundary = '''

pw::Application setCAESolver SU2 3
pw::Application markUndoLevel {Select Solver}

set _DM(4) [pw::GridEntity getByName dom-7]
set _DM(5) [pw::GridEntity getByName dom-5]
set _DM(6) [pw::GridEntity getByName dom-6]
set _DM(7) [pw::GridEntity getByName dom-4]
set _TMP(PW_1) [pw::BoundaryCondition getByName far-field]
$_TMP(PW_1) apply [list [list $_BL(1) $_DM(4)] [list $_BL(1) $_DM(5)] [list $_BL(1) $_DM(6)] [list $_BL(1) $_DM(7)]]
pw::Application markUndoLevel {Set BC}

set _TMP(PW_2) [pw::BoundaryCondition getByName wall]
$_TMP(PW_2) apply [list [list $_BL(1) $_DM(4)] [list $_BL(1) $_DM(5)] [list $_BL(1) $_DM(6)] [list $_BL(1) $_DM(7)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_1) apply [list [list $_BL(1) $_DM(4)] [list $_BL(1) $_DM(5)] [list $_BL(1) $_DM(6)] [list $_BL(1) $_DM(7)]]
pw::Application markUndoLevel {Set BC}

set _DM(8) [pw::GridEntity getByName dom-15]
set _DM(9) [pw::GridEntity getByName dom-8]
set _DM(10) [pw::GridEntity getByName dom-9]
set _DM(11) [pw::GridEntity getByName dom-10]
set _DM(12) [pw::GridEntity getByName dom-12]
set _DM(13) [pw::GridEntity getByName dom-13]
set _DM(14) [pw::GridEntity getByName dom-11]
set _DM(15) [pw::GridEntity getByName dom-14]
$_TMP(PW_2) apply [list [list $_BL(1) $_DM(8)] [list $_BL(1) $_DM(9)] [list $_BL(1) $_DM(10)] [list $_BL(1) $_DM(11)] [list $_BL(1) $_DM(12)] [list $_BL(1) $_DM(13)] [list $_BL(1) $_DM(14)] [list $_BL(1) $_DM(15)]]
pw::Application markUndoLevel {Set BC}

set _TMP(PW_3) [pw::BoundaryCondition create]
pw::Application markUndoLevel {Create BC}

unset _TMP(PW_3)
set _DM(16) [pw::GridEntity getByName dom-18]
set _DM(17) [pw::GridEntity getByName dom-17]
set _DM(18) [pw::GridEntity getByName dom-16]
set _TMP(PW_3) [pw::BoundaryCondition getByName bc-4]
$_TMP(PW_3) apply [list [list $_BL(1) $_DM(3)] [list $_BL(1) $_DM(2)] [list $_BL(1) $_DM(1)] [list $_BL(1) $_DM(16)] [list $_BL(1) $_DM(17)] [list $_BL(1) $_DM(18)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_3) setName symmetry
pw::Application markUndoLevel {Name BC}

'''
                        
                        
                        
                        
            def save_mesh_file(self, update_glyph_data, working_dir, Mesh):       
                su2meshed_file         = update_glyph_data["su2meshed_file"]          
                            
                save_file = '''


    unset _TMP(PW_1)
    unset _TMP(PW_2)
    unset _TMP(PW_3)
    set _TMP(mode_1) [pw::Application begin CaeExport [pw::Entity sort [list $_BL(1) $_DM(1) $_DM(3) $_DM(2) $_DM(7) $_DM(5) $_DM(6) $_DM(4) $_DM(9) $_DM(10) $_DM(11) $_DM(14) $_DM(12) $_DM(13) $_DM(15) $_DM(8) $_DM(18) $_DM(17) $_DM(16)]]]
    $_TMP(mode_1) initialize -strict -type CAE "G:/TUBS/HiWi/Dr Karpuk/PyAeroSweep-Stan-V2/Quasi 3D/su2meshExtrusion.su2"
    $_TMP(mode_1) setAttribute FilePrecision Double
    $_TMP(mode_1) verify
    $_TMP(mode_1) write
    $_TMP(mode_1) end
    unset _TMP(mode_1)
        
    '''

