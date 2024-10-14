# Pointwise V18.3 Journal file - Fri Dec  9 23:06:25 2022

package require PWI_Glyph 3.18.3

pw::Application setUndoMaximumLevels 5
pw::Application reset
pw::Application markUndoLevel {Journal Reset}

pw::Application clearModified


# import airfoil components
set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic /home/christoffer/Projects/VersionControlled/Outputs_PyAeroSweep/Clean_airfoil_import_DAT_SU2_out/Geometry_files/main_airfoil_upper_1.dat
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic /home/christoffer/Projects/VersionControlled/Outputs_PyAeroSweep/Clean_airfoil_import_DAT_SU2_out/Geometry_files/main_airfoil_lower_1.dat
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end

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

# Assign nodes to each connector
set _CN(1) [pw::GridEntity getByName con-1]
$_CN(1) setDimension 200

set _CN(2) [pw::GridEntity getByName con-2]
$_CN(2) setDimension 200

set _CN(3) [pw::GridEntity getByName con-3]
$_CN(3) setDimension 8

# Cluster points at each connector
set _CN(1) [pw::GridEntity getByName con-1]
set _CN(2) [pw::GridEntity getByName con-2]
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(2)]]
  set _TMP(PW_1) [$_CN(1) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0.001
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(2) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0.001
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(2)]]
  set _TMP(PW_1) [$_CN(1) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0.0005
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(2) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0.0005
  unset _TMP(PW_1)
$_TMP(mode_1) end

# Scale the domain according to the physical dimension
set _CN(1) [pw::GridEntity getByName con-1]
set _CN(2) [pw::GridEntity getByName con-2]
set _CN(3) [pw::GridEntity getByName con-3]
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(2) $_CN(3) ]]
  pw::Entity transform [pwu::Transform scaling -anchor {0 0 0} {2.62 2.62 2.62}] [$_TMP(mode_1) getEntities]
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
  $_DM(1) setExtrusionSolverAttribute NormalMarchingVector {-0 -0 -1}
  $_DM(1) setExtrusionSolverAttribute NormalInitialStepSize 5.770548344287181e-06
  $_DM(1) setExtrusionSolverAttribute StopAtHeight Off
  $_DM(1) setExtrusionSolverAttribute StopAtHeight 262.0
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

set _DM(1) [pw::GridEntity getByName dom-1]
set _TMP(mode_1) [pw::Application begin CaeExport [pw::Entity sort [list $_DM(1)]]]
  $_TMP(mode_1) initialize -strict -type CAE /home/christoffer/Projects/VersionControlled/Outputs_PyAeroSweep/Clean_airfoil_import_DAT_SU2_out/su2meshEx.su2
  $_TMP(mode_1) setAttribute FilePrecision Double
  $_TMP(mode_1) verify
  $_TMP(mode_1) write
$_TMP(mode_1) end





