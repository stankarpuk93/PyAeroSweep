# mesh_pre_process_Quasi3D.py
# 
# Created: Dec 2023, S. Holenarsipura M Madhava
# Modified:



# -----------------------------------#
# Clean - Extruded Mesh - Structured #
# -----------------------------------#
 


class Q3DMeshPreProcess_Clean:

  

        def __init__(self, update_glyph_data):
            # Initialize parameters
            # Unpack inputs
            self.upper_surface_filename = update_glyph_data["upper_surface_filename"]
            self.lower_surface_filename = update_glyph_data["lower_surface_filename"]
            self.connector_dimensions   = update_glyph_data["connector_dimensions"]
            self.begin_spacing          = update_glyph_data["begin_spacing"]
            self.end_spacing            = update_glyph_data["end_spacing"]
            self.scaling_factor         = update_glyph_data["scaling_factor"]
            self.stop_at_height_1       = update_glyph_data["stop_at_height_1"]
            self.stop_at_height_2       = update_glyph_data["stop_at_height_2"]
            self.run_iterations_1       = update_glyph_data["run_iterations_1"]
            self.run_iterations_2       = update_glyph_data["run_iterations_2"]
            self.su2meshed_file         = update_glyph_data["su2meshed_file"]

            self.Extrusion_direction    = update_glyph_data["Extrusion_direction"]
            self.Extrusion_distance     = update_glyph_data["Extrusion_distance"]
            self.Extrusion_steps        = update_glyph_data["Extrusion_steps"]
         

        def import_airfoil_components(self):
            glyph_script = f"""

package require PWI_Glyph 6.22.1

pw::Application setUndoMaximumLevels 5
pw::Application reset
pw::Application markUndoLevel {{Journal Reset}}

pw::Application clearModified


# import airfoil components
set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic {self.upper_surface_filename}
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic {self.lower_surface_filename}
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end
"""
            return glyph_script

        def close_trailing_edge(self):
            glyph_script = f"""
set _DB(1) [pw::DatabaseEntity getByName curve-1]
set _DB(2) [pw::DatabaseEntity getByName curve-2]
set _TMP(PW_1) [pw::Connector createOnDatabase -parametricConnectors Aligned -merge 0 -reject _TMP(unused) [list $_DB(1) $_DB(2)]]

# Close the trailing edge of the main airfoil and the flap
set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  set _CN(1) [pw::GridEntity getByName con-1]
  set _DB(1) [pw::DatabaseEntity getByName curve-1]
  set _CN(2) [pw::GridEntity getByName con-2]
  set _DB(2) [pw::DatabaseEntity getByName curve-2]
  $_TMP(PW_1) addPoint [$_CN(1) getPosition -arc 1]
  $_TMP(PW_1) addPoint [$_CN(2) getPosition -arc 0]
  set _CN(3) [pw::Connector create]
  $_CN(3) addSegment $_TMP(PW_1)
  unset _TMP(PW_1)
  $_CN(3) calculateDimension
$_TMP(mode_1) end
"""
            return glyph_script

        def assign_nodes_and_dimensions(self):
            glyph_script = f"""
# Assign nodes to each connector
set _CN(1) [pw::GridEntity getByName con-1]
$_CN(1) setDimension {self.connector_dimensions[0]}

set _CN(2) [pw::GridEntity getByName con-2]
$_CN(2) setDimension {self.connector_dimensions[1]}

set _CN(3) [pw::GridEntity getByName con-3]
$_CN(3) setDimension {self.connector_dimensions[2]}

# Cluster points at each connector
set _CN(1) [pw::GridEntity getByName con-1]
set _CN(2) [pw::GridEntity getByName con-2]
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(2)]]
  set _TMP(PW_1) [$_CN(1) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing {self.begin_spacing}
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(2) getDistribution 1]
  $_TMP(PW_1) setEndSpacing {self.begin_spacing}
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(2)]]
  set _TMP(PW_1) [$_CN(1) getDistribution 1]
  $_TMP(PW_1) setEndSpacing {self.end_spacing}
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(2) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing {self.end_spacing}
  unset _TMP(PW_1)
$_TMP(mode_1) end
"""
            return glyph_script
        

        def scale_the_domain(self, delta_s):
            glyph_script = f"""
# Scale the domain according to the physical dimension
set _CN(1) [pw::GridEntity getByName con-1]
set _CN(2) [pw::GridEntity getByName con-2]
set _CN(3) [pw::GridEntity getByName con-3]
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(2) $_CN(3) ]]
  pw::Entity transform [pwu::Transform scaling -anchor {{0 0 0}} {self.scaling_factor}] [$_TMP(mode_1) getEntities]
$_TMP(mode_1) end

# Extrude a structured mesh
set _TMP(mode_1) [pw::Application begin Create]
  set _CN(1) [pw::GridEntity getByName con-3]
  set _CN(2) [pw::GridEntity getByName con-2]
  set _CN(3) [pw::GridEntity getByName con-1]
  set _TMP(PW_1) [pw::Edge createFromConnectors [list $_CN(1) $_CN(2) $_CN(3)]]
  set _TMP(edge_1) [lindex $_TMP(PW_1) 0]
  unset _TMP(PW_1)
  set _DM(1) [pw::DomainStructured create]
  $_DM(1) addEdge $_TMP(edge_1)
$_TMP(mode_1) end
unset _TMP(mode_1)
set _TMP(mode_1) [pw::Application begin ExtrusionSolver [list $_DM(1)]]
  $_TMP(mode_1) setKeepFailingStep true
  $_DM(1) setExtrusionSolverAttribute NormalMarchingVector {{-0 -0 -1}}
  $_DM(1) setExtrusionSolverAttribute NormalInitialStepSize {delta_s}
  $_DM(1) setExtrusionSolverAttribute StopAtHeight {self.stop_at_height_1}
  $_DM(1) setExtrusionSolverAttribute StopAtHeight {self.stop_at_height_2}
  $_TMP(mode_1) run 230
  $_TMP(mode_1) run -1
$_TMP(mode_1) end

# Assign boundary conditions
pw::Application setCAESolver SU2 2

set _TMP(PW_1) [pw::BoundaryCondition create]

unset _TMP(PW_1)
set _TMP(PW_1) [pw::BoundaryCondition getByName bc-2]
$_TMP(PW_1) setName wall

set _TMP(PW_2) [pw::BoundaryCondition create]

unset _TMP(PW_2)
set _TMP(PW_2) [pw::BoundaryCondition getByName bc-3]
$_TMP(PW_2) setName far-field

set _CN(4) [pw::GridEntity getByName con-5]
set _DM(2) [pw::GridEntity getByName dom-1]
$_TMP(PW_2) apply [list [list $_DM(2) $_CN(4)]]

$_TMP(PW_1) apply [list [list $_DM(2) $_CN(1)] [list $_DM(2) $_CN(3)] [list $_DM(2) $_CN(2)]]

set _DM(1) [pw::GridEntity getByName dom-1]
set ents [list $_DM(1)]
set _TMP(mode_1) [pw::Application begin Modify $ents]
  $_DM(1) setOrientation IMaximum JMinimum
  set _CN(1) [pw::GridEntity getByName con-1]
  set _CN(2) [pw::GridEntity getByName con-2]
  set _CN(3) [pw::GridEntity getByName con-3]
  set _CN(4) [pw::GridEntity getByName con-4]
  set _CN(5) [pw::GridEntity getByName con-5]
$_TMP(mode_1) end
"""
        




            return glyph_script
        

        def extrude_the_mesh(self):
                glyph_script = f"""
# Extruding the mesh

pw::Application setUndoMaximumLevels 5

pw::Application setCAESolver CGNS 2
pw::Application markUndoLevel {{Select Solver}}

pw::Application setCAESolver CGNS 3
pw::Application markUndoLevel {{Set Dimension 3D}}

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
  $_BL(1) setExtrusionSolverAttribute TranslateDirection {self.Extrusion_direction}
  $_BL(1) setExtrusionSolverAttribute TranslateDistance {self.Extrusion_distance}
  $_TMP(mode_1) run {self.Extrusion_steps}
$_TMP(mode_1) end
unset _TMP(mode_1)
unset _TMP(face_1)
pw::Application markUndoLevel {{Extrude, Translate}}

pw::Application setCAESolver SU2 3
pw::Application markUndoLevel {{Select Solver}}

set _DM(2) [pw::GridEntity getByName dom-3]
set _DM(3) [pw::GridEntity getByName dom-4]
set _DM(4) [pw::GridEntity getByName dom-2]
set _TMP(PW_1) [pw::BoundaryCondition getByName wall]
$_TMP(PW_1) apply [list [list $_BL(1) $_DM(2)] [list $_BL(1) $_DM(3)] [list $_BL(1) $_DM(4)]]
pw::Application markUndoLevel {{Set BC}}

set _DM(5) [pw::GridEntity getByName dom-6]
set _TMP(PW_2) [pw::BoundaryCondition getByName far-field]
$_TMP(PW_2) apply [list [list $_BL(1) $_DM(5)]]
pw::Application markUndoLevel {{Set BC}}

set _TMP(PW_3) [pw::BoundaryCondition create]
pw::Application markUndoLevel {{Create BC}}

unset _TMP(PW_3)
set _DM(6) [pw::GridEntity getByName dom-8]
set _TMP(PW_3) [pw::BoundaryCondition getByName bc-4]
$_TMP(PW_3) apply [list [list $_BL(1) $_DM(6)] [list $_BL(1) $_DM(1)]]
pw::Application markUndoLevel {{Set BC}}

$_TMP(PW_3) setName symmetry
pw::Application markUndoLevel {{Name BC}}

unset _TMP(PW_1)
unset _TMP(PW_2)
unset _TMP(PW_3)
set _DM(7) [pw::GridEntity getByName dom-5]
set _TMP(mode_1) [pw::Application begin CaeExport [pw::Entity sort [list $_BL(1) $_DM(1) $_DM(4) $_DM(2) $_DM(3) $_DM(7) $_DM(5) $_DM(6)]]]
  $_TMP(mode_1) initialize -strict -type CAE {self.su2meshed_file}
  $_TMP(mode_1) setAttribute FilePrecision Double
  $_TMP(mode_1) verify
  $_TMP(mode_1) write
$_TMP(mode_1) end
unset _TMP(mode_1)
"""
                return glyph_script

        def run_glyph_script(self, delta_s, glyph_file):
            glyph_script = self.import_airfoil_components()
            glyph_script += self.close_trailing_edge()
            glyph_script += self.assign_nodes_and_dimensions()

            
            
            glyph_script += self.scale_the_domain(delta_s)
            


            glyph_script += self.extrude_the_mesh()


            # Save the Glyph script to a file
            with open(glyph_file, "w") as file:
                file.write(glyph_script)

            return


# ---------------------------------------#
# Flapped - Extruded Mesh - Unstructured #
# ---------------------------------------#


class Q3DMeshPreProcess_Flapped:

  

        def __init__(self, update_glyph_data):
            # Initialize parameters
            # Unpack inputs
            self.upper_surface_filename      = update_glyph_data["upper_surface_filename"]
            self.lower_surface_filename      = update_glyph_data["lower_surface_filename"]
            self.cut1_filename               = update_glyph_data["cut1_filename"]
            self.cut2_filename               = update_glyph_data["cut2_filename"]
            self.flap_airfoil_lower_filename = update_glyph_data["flap_airfoil_lower_filename"]
            self.flap_airfoil_upper_filename = update_glyph_data["flap_airfoil_upper_filename"]
            
            self.connector_dimensions        = update_glyph_data["connector_dimensions"]

            self.spacing_127_130 = update_glyph_data["spacing_127_130"]
            self.spacing_137_140 = update_glyph_data["spacing_137_140"]
            self.spacing_146_149 = update_glyph_data["spacing_146_149"]
            self.spacing_156_159 = update_glyph_data["spacing_156_159"]
            self.spacing_165_172 = update_glyph_data["spacing_165_172"]
            self.spacing_178_184 = update_glyph_data["spacing_178_184"]
            self.spacing_192_195 = update_glyph_data["spacing_192_195"]
            self.spacing_201_204 = update_glyph_data["spacing_201_204"]
            self.spacing_211_214 = update_glyph_data["spacing_211_214"]

            self.addPoint228  = update_glyph_data["addPoint228"]
            self.addPoint229  = update_glyph_data["addPoint229"]
            self.addPoint245  = update_glyph_data["addPoint245"]
            self.addPoint255  = update_glyph_data["addPoint255"]
            self.addPoint_287 = update_glyph_data["addPoint_287"]
            self.addPoint_288 = update_glyph_data["addPoint_288"]
            self.EndAngle_289 = update_glyph_data["EndAngle_289"]
            self.addPoint_298 = update_glyph_data["addPoint_298"]
            self.addPoint_299 = update_glyph_data["addPoint_299"]
            self.EndAngle_300 = update_glyph_data["EndAngle_300"]

            self.node_to_connector_313   = update_glyph_data["node_to_connector_313"]
            self.scaling_factor          = update_glyph_data["scaling_factor"]
            self.BoundaryDecay_359       = update_glyph_data["BoundaryDecay_359"]
            self.BoundaryDecay_384       = update_glyph_data["BoundaryDecay_384"]
            self.maxlayers_430           = update_glyph_data["maxlayers_430"]
            self.fulllayers_431          = update_glyph_data["fulllayers_431"]
            self.growthrate_433          = update_glyph_data["growthrate_433"]
            self.BoundaryDecay_435       = update_glyph_data["BoundaryDecay_435"]
            self.far_field_connector_dim = update_glyph_data["far_field_connector_dim"]
            self.su2meshed_file          = update_glyph_data["su2meshed_file"]

            self.Extrusion_direction    = update_glyph_data["Extrusion_direction"]
            self.Extrusion_distance     = update_glyph_data["Extrusion_distance"]
            self.Extrusion_steps        = update_glyph_data["Extrusion_steps"]

        def import_airfoil_components(self):
            glyph_script = f"""

package require PWI_Glyph 6.22.1

pw::Application setUndoMaximumLevels 5
pw::Application reset
pw::Application markUndoLevel {{Journal Reset}}

pw::Application clearModified


# import airfoil components
set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic {self.upper_surface_filename}
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic {self.lower_surface_filename}
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic {self.cut1_filename}
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic {self.cut2_filename}
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic {self.flap_airfoil_lower_filename}
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic {self.flap_airfoil_upper_filename}
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end

"""
            return glyph_script

        def close_trailing_edge(self):
            glyph_script = f"""
# Create connectors
set _DB(1) [pw::DatabaseEntity getByName curve-3]
set _DB(2) [pw::DatabaseEntity getByName curve-1]
set _DB(3) [pw::DatabaseEntity getByName curve-4]
set _DB(4) [pw::DatabaseEntity getByName curve-2]
set _DB(5) [pw::DatabaseEntity getByName curve-6]
set _DB(6) [pw::DatabaseEntity getByName curve-5]
set _TMP(PW_1) [pw::Connector createOnDatabase -parametricConnectors Aligned -merge 0 -reject _TMP(unused) [list $_DB(1) $_DB(2) $_DB(3) $_DB(4) $_DB(5) $_DB(6)]]

# Close the trailing edge of the main airfoil and the flap
set _TMP(mode_1) [pw::Application begin Create]
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
"""
            return glyph_script

        def assign_nodes_and_dimensions(self):
            glyph_script = f"""
# Assign nodes to each connector
set _CN(1) [pw::GridEntity getByName con-1]
$_CN(1) setDimension {self.connector_dimensions[0]}

set _CN(2) [pw::GridEntity getByName con-2]
$_CN(2) setDimension {self.connector_dimensions[1]}

set _CN(3) [pw::GridEntity getByName con-6]
$_CN(3) setDimension {self.connector_dimensions[2]}

set _CN(4) [pw::GridEntity getByName con-5]
$_CN(4) setDimension {self.connector_dimensions[3]}

set _CN(5) [pw::GridEntity getByName con-3]
$_CN(5) setDimension {self.connector_dimensions[4]}

set _CN(6) [pw::GridEntity getByName con-4]
$_CN(6) setDimension {self.connector_dimensions[5]}

set _CN(7) [pw::GridEntity getByName con-7]
$_CN(7) setDimension {self.connector_dimensions[6]}

set _CN(8) [pw::GridEntity getByName con-8]
$_CN(8) setDimension {self.connector_dimensions[7]}


# Cluster points at each connetor
set _CN(1) [pw::GridEntity getByName con-1]
set _CN(2) [pw::GridEntity getByName con-2]
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(2)]]
  set _TMP(PW_1) [$_CN(1) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing {self.spacing_127_130}
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(2) getDistribution 1]
  $_TMP(PW_1) setEndSpacing {self.spacing_127_130}
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _CN(3) [pw::GridEntity getByName con-3]
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(3)]]
  set _TMP(PW_1) [$_CN(1) getDistribution 1]
  $_TMP(PW_1) setEndSpacing {self.spacing_137_140}
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(3) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing {self.spacing_137_140}
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(3)]]
  set _TMP(PW_1) [$_CN(1) getDistribution 1]
  $_TMP(PW_1) setEndSpacing {self.spacing_146_149}
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(3) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing {self.spacing_146_149}
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _CN(4) [pw::GridEntity getByName con-7]
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(4)]]
  set _TMP(PW_1) [$_CN(4) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing {self.spacing_156_159}
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(4) getDistribution 1]
  $_TMP(PW_1) setEndSpacing {self.spacing_156_159}
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Modify [list $_CN(2)]]
  set _TMP(PW_1) [$_CN(2) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing {self.spacing_165_172}
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _CN(5) [pw::GridEntity getByName con-4]
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(5)]]
  set _TMP(PW_1) [$_CN(5) getDistribution 1]
  $_TMP(PW_1) setEndSpacing {self.spacing_165_172}
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Modify [list $_CN(3)]]
  set _TMP(PW_1) [$_CN(3) getDistribution 1]
  $_TMP(PW_1) setEndSpacing {self.spacing_178_184}
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Modify [list $_CN(5)]]
  set _TMP(PW_1) [$_CN(5) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing {self.spacing_178_184}
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _CN(6) [pw::GridEntity getByName con-5]
set _CN(7) [pw::GridEntity getByName con-6]
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(6) $_CN(7)]]
  set _TMP(PW_1) [$_CN(6) getDistribution 1]
  $_TMP(PW_1) setEndSpacing {self.spacing_192_195}
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(7) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing {self.spacing_192_195}
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Modify [list $_CN(6) $_CN(7)]]
  set _TMP(PW_1) [$_CN(6) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing {self.spacing_201_204}
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(7) getDistribution 1]
  $_TMP(PW_1) setEndSpacing {self.spacing_201_204}
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _CN(8) [pw::GridEntity getByName con-8]
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(8)]]
  set _TMP(PW_1) [$_CN(8) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing {self.spacing_211_214}
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(8) getDistribution 1]
  $_TMP(PW_1) setEndSpacing {self.spacing_211_214}
  unset _TMP(PW_1)
$_TMP(mode_1) end

"""
            return glyph_script
        

        def field_parameters(self, delta_s):
            glyph_script = f"""
# Create far-field boundaries
set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  $_TMP(PW_1) delete
  unset _TMP(PW_1)
$_TMP(mode_1) abort
unset _TMP(mode_1)
set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  $_TMP(PW_1) addPoint {self.addPoint228}
  $_TMP(PW_1) addPoint {self.addPoint229}
  set _CN(1) [pw::Connector create]
  $_CN(1) addSegment $_TMP(PW_1)
  unset _TMP(PW_1)
  $_CN(1) calculateDimension
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  $_TMP(PW_1) delete
  unset _TMP(PW_1)
$_TMP(mode_1) abort
unset _TMP(mode_1)
set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  $_TMP(PW_1) addPoint [$_CN(1) getPosition -arc 1]
  $_TMP(PW_1) addPoint {self.addPoint245}
  set _CN(2) [pw::Connector create]
  $_CN(2) addSegment $_TMP(PW_1)
  unset _TMP(PW_1)
  $_CN(2) calculateDimension
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  $_TMP(PW_1) addPoint [$_CN(2) getPosition -arc 1]
  $_TMP(PW_1) addPoint {self.addPoint255}
  set _CN(3) [pw::Connector create]
  $_CN(3) addSegment $_TMP(PW_1)
  unset _TMP(PW_1)
  $_CN(3) calculateDimension
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  $_TMP(PW_1) addPoint [$_CN(3) getPosition -arc 1]
  $_TMP(PW_1) addPoint [$_CN(1) getPosition -arc 0]
  set _CN(4) [pw::Connector create]
  $_CN(4) addSegment $_TMP(PW_1)
  unset _TMP(PW_1)
  $_CN(4) calculateDimension
$_TMP(mode_1) end


# Assign nodes to each far-field connector
set _CN(1) [pw::GridEntity getByName con-11]
set _CN(2) [pw::GridEntity getByName con-12]
set _CN(3) [pw::GridEntity getByName con-9]
set _CN(4) [pw::GridEntity getByName con-10]
set _TMP(PW_1) [pw::Collection create]
$_TMP(PW_1) set [list $_CN(1) $_CN(2) $_CN(3) $_CN(4)]
  $_TMP(PW_1) do setDimension {self.far_field_connector_dim}

# Create near field
set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentCircle create]
  $_TMP(PW_1) addPoint {self.addPoint_287}
  $_TMP(PW_1) addPoint {self.addPoint_288}
  $_TMP(PW_1) setEndAngle {self.EndAngle_289}
  set _CN(1) [pw::Connector create]
  $_CN(1) addSegment $_TMP(PW_1)
  $_CN(1) calculateDimension
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentCircle create]
  $_TMP(PW_1) addPoint {self.addPoint_298}
  $_TMP(PW_1) addPoint {self.addPoint_299}
  $_TMP(PW_1) setEndAngle {self.EndAngle_300}
  set _CN(2) [pw::Connector create]
  $_CN(2) addSegment $_TMP(PW_1)
  $_CN(2) calculateDimension
  unset _TMP(PW_1)
$_TMP(mode_1) end


# Assign nodes to connectors 
set _CN(1) [pw::GridEntity getByName con-13]
set _CN(2) [pw::GridEntity getByName con-14]
set _TMP(PW_1) [pw::Collection create]
$_TMP(PW_1) set [list $_CN(1) $_CN(2)]
  $_TMP(PW_1) do setDimension {self.node_to_connector_313}


# Scale the domain according to the physical dimension
set _CN(1) [pw::GridEntity getByName con-10]
set _CN(2) [pw::GridEntity getByName con-9]
set _CN(3) [pw::GridEntity getByName con-12]
set _CN(4) [pw::GridEntity getByName con-11]
set _CN(5) [pw::GridEntity getByName con-13]
set _CN(6) [pw::GridEntity getByName con-8]
set _CN(7) [pw::GridEntity getByName con-14]
set _CN(8) [pw::GridEntity getByName con-2]
set _CN(9) [pw::GridEntity getByName con-5]
set _CN(10) [pw::GridEntity getByName con-7]
set _CN(11) [pw::GridEntity getByName con-4]
set _CN(12) [pw::GridEntity getByName con-6]
set _CN(13) [pw::GridEntity getByName con-1]
set _CN(14) [pw::GridEntity getByName con-3]
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(2) $_CN(3) $_CN(4) $_CN(5) $_CN(6) $_CN(7) $_CN(8) $_CN(9) $_CN(10) $_CN(11) $_CN(12) $_CN(13) $_CN(14)]]
  pw::Entity transform [pwu::Transform scaling -anchor {{0 0 0}} {self.scaling_factor}] [$_TMP(mode_1) getEntities]
$_TMP(mode_1) end


# Create a far-field mesh
pw::Application setGridPreference Unstructured
set _TMP(mode_1) [pw::Application begin Create]
  set _CN(1) [pw::GridEntity getByName con-11]
  set _TMP(edge_1) [pw::Edge create]
  $_TMP(edge_1) addConnector $_CN(1)
  set _CN(2) [pw::GridEntity getByName con-12]
  $_TMP(edge_1) addConnector $_CN(2)
  set _CN(3) [pw::GridEntity getByName con-9]
  $_TMP(edge_1) addConnector $_CN(3)
  set _CN(4) [pw::GridEntity getByName con-10]
  $_TMP(edge_1) addConnector $_CN(4)
  set _CN(5) [pw::GridEntity getByName con-14]
  set _TMP(edge_2) [pw::Edge create]
  $_TMP(edge_2) addConnector $_CN(5)
  set _DM(1) [pw::DomainUnstructured create]
  $_DM(1) addEdge $_TMP(edge_1)
  $_DM(1) addEdge $_TMP(edge_2)
  unset _TMP(edge_2)
  unset _TMP(edge_1)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin UnstructuredSolver [list $_DM(1)]]
  $_DM(1) setUnstructuredSolverAttribute BoundaryDecay {self.BoundaryDecay_359}
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin UnstructuredSolver [list $_DM(1)]]
  $_TMP(mode_1) run Initialize
$_TMP(mode_1) end


# Create a near-field mesh
set _TMP(mode_1) [pw::Application begin Create]
  set _CN(1) [pw::GridEntity getByName con-14]
  set _TMP(edge_1) [pw::Edge create]
  $_TMP(edge_1) addConnector $_CN(1)
  set _CN(2) [pw::GridEntity getByName con-13]
  set _TMP(edge_2) [pw::Edge create]
  $_TMP(edge_2) addConnector $_CN(2)
  $_TMP(edge_2) reverse
  set _DM(1) [pw::DomainUnstructured create]
  $_DM(1) addEdge $_TMP(edge_1)
  $_DM(1) addEdge $_TMP(edge_2)
  unset _TMP(edge_2)
  unset _TMP(edge_1)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin UnstructuredSolver [list $_DM(1)]]
  $_DM(1) setUnstructuredSolverAttribute BoundaryDecay {self.BoundaryDecay_384}
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin UnstructuredSolver [list $_DM(1)]]
  $_TMP(mode_1) run Initialize
$_TMP(mode_1) end



# Calcualte airfoil mesh
set _TMP(mode_1) [pw::Application begin Create]
  set _CN(1) [pw::GridEntity getByName con-13]
  set _TMP(edge_1) [pw::Edge create]
  $_TMP(edge_1) addConnector $_CN(1)
  set _CN(2) [pw::GridEntity getByName con-2]
  set _TMP(edge_2) [pw::Edge create]
  $_TMP(edge_2) addConnector $_CN(2)
  set _CN(3) [pw::GridEntity getByName con-1]
  $_TMP(edge_2) addConnector $_CN(3)
  set _CN(4) [pw::GridEntity getByName con-7]
  $_TMP(edge_2) addConnector $_CN(4)
  set _CN(5) [pw::GridEntity getByName con-3]
  $_TMP(edge_2) addConnector $_CN(5)
  set _CN(6) [pw::GridEntity getByName con-4]
  $_TMP(edge_2) addConnector $_CN(6)
  set _CN(7) [pw::GridEntity getByName con-5]
  set _TMP(edge_3) [pw::Edge create]
  $_TMP(edge_3) addConnector $_CN(7)
  set _CN(8) [pw::GridEntity getByName con-6]
  $_TMP(edge_3) addConnector $_CN(8)
  set _CN(9) [pw::GridEntity getByName con-8]
  $_TMP(edge_3) addConnector $_CN(9)
  set _DM(1) [pw::DomainUnstructured create]
  $_DM(1) addEdge $_TMP(edge_1)
  $_DM(1) addEdge $_TMP(edge_2)
  $_DM(1) addEdge $_TMP(edge_3)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin UnstructuredSolver [list $_DM(1)]]
  set _TMP(PW_1) [pw::TRexCondition getByName Unspecified]
  set _TMP(PW_2) [pw::TRexCondition create]
  set _TMP(PW_3) [pw::TRexCondition getByName bc-2]
  unset _TMP(PW_2)
  $_TMP(PW_3) setName wall
  $_TMP(PW_3) setConditionType Wall
  $_TMP(PW_3) setValue {delta_s}
  $_DM(1) setUnstructuredSolverAttribute TRexMaximumLayers {self.maxlayers_430}
  $_DM(1) setUnstructuredSolverAttribute TRexFullLayers {self.fulllayers_431}
  $_DM(1) setUnstructuredSolverAttribute TRexGrowthRate 1.1
  $_DM(1) setUnstructuredSolverAttribute TRexGrowthRate {self.growthrate_433}
  $_DM(1) setUnstructuredSolverAttribute TRexPushAttributes True
  $_DM(1) setUnstructuredSolverAttribute BoundaryDecay {self.BoundaryDecay_435}
  $_TMP(mode_1) run Initialize
  $_TMP(PW_3) apply [list [list $_DM(1) $_CN(9) Same] [list $_DM(1) $_CN(8) Same] [list $_DM(1) $_CN(4) Same] [list $_DM(1) $_CN(2) Same] [list $_DM(1) $_CN(6) Same] [list $_DM(1) $_CN(3) Same] [list $_DM(1) $_CN(5) Same] [list $_DM(1) $_CN(7) Same]]
  $_TMP(mode_1) run Initialize
  $_DM(1) setUnstructuredSolverAttribute TRexCellType TriangleQuad
  $_TMP(mode_1) run Initialize
$_TMP(mode_1) end


# Assign boundary conditions
pw::Application setCAESolver SU2 2

set _TMP(PW_1) [pw::BoundaryCondition create]
unset _TMP(PW_1)

set _TMP(PW_1) [pw::BoundaryCondition getByName bc-2]
$_TMP(PW_1) setName far-field

set _TMP(PW_2) [pw::BoundaryCondition create]
unset _TMP(PW_2)
set _TMP(PW_2) [pw::BoundaryCondition getByName bc-3]
$_TMP(PW_2) setName wall

set _CN(1) [pw::GridEntity getByName con-1]
set _DM(1) [pw::GridEntity getByName dom-3]
set _CN(2) [pw::GridEntity getByName con-2]
set _CN(3) [pw::GridEntity getByName con-3]
set _CN(4) [pw::GridEntity getByName con-4]
set _CN(5) [pw::GridEntity getByName con-5]
set _CN(6) [pw::GridEntity getByName con-6]
set _CN(7) [pw::GridEntity getByName con-7]
set _CN(8) [pw::GridEntity getByName con-8]
set _CN(9) [pw::GridEntity getByName con-9]
set _DM(2) [pw::GridEntity getByName dom-1]
set _CN(10) [pw::GridEntity getByName con-10]
set _CN(11) [pw::GridEntity getByName con-11]
set _CN(12) [pw::GridEntity getByName con-12]
set _CN(13) [pw::GridEntity getByName con-13]
set _DM(3) [pw::GridEntity getByName dom-2]
set _CN(14) [pw::GridEntity getByName con-14]


$_TMP(PW_1) apply [list [list $_DM(2) $_CN(10)] [list $_DM(2) $_CN(11)] [list $_DM(2) $_CN(9)] [list $_DM(2) $_CN(12)]]

$_TMP(PW_2) apply [list [list $_DM(1) $_CN(8)] [list $_DM(1) $_CN(7)] [list $_DM(1) $_CN(5)] [list $_DM(1) $_CN(1)] [list $_DM(1) $_CN(6)] [list $_DM(1) $_CN(3)] [list $_DM(1) $_CN(2)] [list $_DM(1) $_CN(4)]]


# Assign normal vectors
set _DM(1) [pw::GridEntity getByName dom-3]
set _DM(2) [pw::GridEntity getByName dom-1]
set _DM(3) [pw::GridEntity getByName dom-2]
set ents [list $_DM(1) $_DM(2) $_DM(3)]
set _TMP(mode_1) [pw::Application begin Modify $ents]
  set _CN(1) [pw::GridEntity getByName con-13]
  set _CN(2) [pw::GridEntity getByName con-2]
  set _CN(3) [pw::GridEntity getByName con-1]
  set _CN(4) [pw::GridEntity getByName con-7]
  set _CN(5) [pw::GridEntity getByName con-3]
  set _CN(6) [pw::GridEntity getByName con-4]
  set _CN(7) [pw::GridEntity getByName con-5]
  set _CN(8) [pw::GridEntity getByName con-6]
  set _CN(9) [pw::GridEntity getByName con-8]
  set _CN(10) [pw::GridEntity getByName con-11]
  set _CN(11) [pw::GridEntity getByName con-12]
  set _CN(12) [pw::GridEntity getByName con-9]
  set _CN(13) [pw::GridEntity getByName con-10]
  set _CN(14) [pw::GridEntity getByName con-14]
  $_DM(3) alignOrientation [list $_DM(2) $_DM(3) $_DM(1)]
$_TMP(mode_1) end
"""

            return glyph_script
        

        def extrude_the_mesh(self):
                glyph_script = f"""
# Extruding the mesh

pw::Application setUndoMaximumLevels 5

pw::Application setCAESolver CGNS 2
pw::Application markUndoLevel {{Select Solver}}

pw::Application setCAESolver CGNS 3
pw::Application markUndoLevel {{Set Dimension 3D}}

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
  $_BL(1) setExtrusionSolverAttribute TranslateDirection {{1 0 0}}
  $_BL(1) setExtrusionSolverAttribute TranslateDirection {self.Extrusion_direction}
  $_BL(1) setExtrusionSolverAttribute TranslateDistance {self.Extrusion_distance}
  $_TMP(mode_1) run {self.Extrusion_steps}
$_TMP(mode_1) end
unset _TMP(mode_1)
unset _TMP(face_1)
pw::Application markUndoLevel {{Extrude, Translate}}

pw::Application setCAESolver SU2 3
pw::Application markUndoLevel {{Select Solver}}

set _DM(4) [pw::GridEntity getByName dom-7]
set _DM(5) [pw::GridEntity getByName dom-5]
set _DM(6) [pw::GridEntity getByName dom-6]
set _DM(7) [pw::GridEntity getByName dom-4]
set _TMP(PW_1) [pw::BoundaryCondition getByName far-field]
$_TMP(PW_1) apply [list [list $_BL(1) $_DM(4)] [list $_BL(1) $_DM(5)] [list $_BL(1) $_DM(6)] [list $_BL(1) $_DM(7)]]
pw::Application markUndoLevel {{Set BC}}

set _TMP(PW_2) [pw::BoundaryCondition getByName wall]
$_TMP(PW_2) apply [list [list $_BL(1) $_DM(4)] [list $_BL(1) $_DM(5)] [list $_BL(1) $_DM(6)] [list $_BL(1) $_DM(7)]]
pw::Application markUndoLevel {{Set BC}}

$_TMP(PW_1) apply [list [list $_BL(1) $_DM(4)] [list $_BL(1) $_DM(5)] [list $_BL(1) $_DM(6)] [list $_BL(1) $_DM(7)]]
pw::Application markUndoLevel {{Set BC}}

set _DM(8) [pw::GridEntity getByName dom-15]
set _DM(9) [pw::GridEntity getByName dom-8]
set _DM(10) [pw::GridEntity getByName dom-9]
set _DM(11) [pw::GridEntity getByName dom-10]
set _DM(12) [pw::GridEntity getByName dom-12]
set _DM(13) [pw::GridEntity getByName dom-13]
set _DM(14) [pw::GridEntity getByName dom-11]
set _DM(15) [pw::GridEntity getByName dom-14]
$_TMP(PW_2) apply [list [list $_BL(1) $_DM(8)] [list $_BL(1) $_DM(9)] [list $_BL(1) $_DM(10)] [list $_BL(1) $_DM(11)] [list $_BL(1) $_DM(12)] [list $_BL(1) $_DM(13)] [list $_BL(1) $_DM(14)] [list $_BL(1) $_DM(15)]]
pw::Application markUndoLevel {{Set BC}}

set _TMP(PW_3) [pw::BoundaryCondition create]
pw::Application markUndoLevel {{Create BC}}

unset _TMP(PW_3)
set _DM(16) [pw::GridEntity getByName dom-18]
set _DM(17) [pw::GridEntity getByName dom-17]
set _DM(18) [pw::GridEntity getByName dom-16]
set _TMP(PW_3) [pw::BoundaryCondition getByName bc-4]
$_TMP(PW_3) apply [list [list $_BL(1) $_DM(3)] [list $_BL(1) $_DM(2)] [list $_BL(1) $_DM(1)] [list $_BL(1) $_DM(16)] [list $_BL(1) $_DM(17)] [list $_BL(1) $_DM(18)]]
pw::Application markUndoLevel {{Set BC}}

$_TMP(PW_3) setName symmetry
pw::Application markUndoLevel {{Name BC}}

unset _TMP(PW_1)
unset _TMP(PW_2)
unset _TMP(PW_3)
set _TMP(mode_1) [pw::Application begin CaeExport [pw::Entity sort [list $_BL(1) $_DM(1) $_DM(3) $_DM(2) $_DM(7) $_DM(5) $_DM(6) $_DM(4) $_DM(9) $_DM(10) $_DM(11) $_DM(14) $_DM(12) $_DM(13) $_DM(15) $_DM(8) $_DM(18) $_DM(17) $_DM(16)]]]
  $_TMP(mode_1) initialize -strict -type CAE {self.su2meshed_file} 
  $_TMP(mode_1) setAttribute FilePrecision Double
  $_TMP(mode_1) verify
  $_TMP(mode_1) write
$_TMP(mode_1) end
unset _TMP(mode_1)
"""
                return glyph_script
       
        def run_glyph_script(self, delta_s, glyph_file):
            glyph_script = self.import_airfoil_components()
            glyph_script += self.close_trailing_edge()
            glyph_script += self.assign_nodes_and_dimensions()
            

            glyph_script += self.field_parameters(delta_s)


            glyph_script += self.extrude_the_mesh()


            # Save the Glyph script to a file
            with open(glyph_file, "w") as file:
                file.write(glyph_script)

            return



            