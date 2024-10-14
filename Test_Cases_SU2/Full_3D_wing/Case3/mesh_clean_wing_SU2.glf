
# Fidelity Pointwise V18.6 Journal file - Sun Dec  3 17:40:02 2023

package require PWI_Glyph 6.22.1

pw::Application setUndoMaximumLevels 5
pw::Application reset
pw::Application markUndoLevel {Journal Reset}

pw::Application clearModified
            


set _TMP(mode_1) [pw::Application begin DatabaseImport]
$_TMP(mode_1) initialize -strict -type Automatic /home/doktorand/Software/PyAeroSweep-Stan-V3/PyAeroSweep/Test_Cases/Full_3D_wing/Case3/Geometry_files/Wing_geometry.igs
$_TMP(mode_1) setAttribute SurfaceSplitDiscontinuous true
$_TMP(mode_1) setAttribute FileUnits Meters
$_TMP(mode_1) setAttribute ShellCellMode AsIs
$_TMP(mode_1) read
$_TMP(mode_1) convert
$_TMP(mode_1) end

set _DB(1) [pw::DatabaseEntity getByName BSurf-1-0]
set _DB(2) [pw::DatabaseEntity getByName BSurf-1-1]
set _DB(3) [pw::DatabaseEntity getByName BSurf-3-0]
set _DB(4) [pw::DatabaseEntity getByName BSurf-3-1]
set _DB(5) [pw::DatabaseEntity getByName BSurf-5-0]
set _DB(6) [pw::DatabaseEntity getByName BSurf-5-1]
set _DB(7) [pw::DatabaseEntity getByName BSurf-7]
set _DB(8) [pw::DatabaseEntity getByName BSurf-9]
set _DB(9) [pw::DatabaseEntity getByName BSurf-11]
set _TMP(PW_1) [pw::Model assemble -reject _TMP(rejectEnts) -rejectReason _TMP(rejectReasons) -rejectLocation _TMP(rejectLocations) [list $_DB(1) $_DB(2) $_DB(3) $_DB(4) $_DB(5) $_DB(6) $_DB(7) $_DB(8) $_DB(9)]]

set _DB(1) [pw::DatabaseEntity getByName BSurf-7-model]
 set _TMP(mode_1) [pw::Application begin DatabaseMesher [list $_DB(1)]]
$_TMP(mode_1) setMinimumBoundarySubdivisions 10
$_TMP(mode_1) setMaximumExtentsSubdivisions 300
$_TMP(mode_1) setCurvatureResolutionAngle 10
$_TMP(mode_1) setMaximumAspectRatio 100
$_TMP(mode_1) setRefinementFactor 1.3
$_TMP(mode_1) setBoundaryGapSubdivisions 5
set _TMP(filter_1) Global
            
set _DB(1) [pw::DatabaseEntity getByName BSurf-1-0-quilt]
set _DB(2) [pw::DatabaseEntity getByName BSurf-1-1-quilt]
set _DB(3) [pw::DatabaseEntity getByName BSurf-3-0-quilt]
set _DB(4) [pw::DatabaseEntity getByName BSurf-3-1-quilt]
set _DB(5) [pw::DatabaseEntity getByName BSurf-5-0-quilt]
set _DB(6) [pw::DatabaseEntity getByName BSurf-5-1-quilt]

$_TMP(mode_1) setBoundaryConvexUseGrowth false
$_TMP(mode_1) setBoundaryConvexSpacingFactor 0.5  
$_TMP(mode_1) addBoundaryFilter
$_TMP(mode_1) setBoundaryFilterName bf-1 LETE
$_TMP(mode_1) setBoundaryFilterGrowthType LETE MaximumAspectRatio
$_TMP(mode_1) setBoundaryFilterSpacingFactor LETE 1  
$_TMP(mode_1) setBoundaryFilterGrowthValue LETE 100

$_TMP(mode_1) setBoundaryFilterDefinition LETE [list {BSurf-1-0-quilt BSurf-1-0-quilt Curvature} {BSurf-3-0-quilt BSurf--1-0-quilt Curvature} {BSurf-5-0-quilt BSurf--3-0-quilt Curvature} {BSurf-1-1-quilt BSurf-1-1-quilt Curvature} {BSurf-3-1-quilt BSurf--1-1-quilt Curvature} {BSurf-5-1-quilt BSurf--3-1-quilt Curvature}]
$_TMP(mode_1) createGridEntities Domain
$_TMP(mode_1) setDomainAspectRatioThreshold 100
$_TMP(mode_1) end

set _DB(1) [pw::GridEntity getByName BSurf-1-0-quilt-dom]
set _DB(2) [pw::GridEntity getByName BSurf-1-1-quilt-dom]
set _DB(3) [pw::GridEntity getByName BSurf-3-0-quilt-dom]
set _DB(4) [pw::GridEntity getByName BSurf-3-1-quilt-dom]
set _DB(5) [pw::GridEntity getByName BSurf-5-0-quilt-dom]
set _DB(6) [pw::GridEntity getByName BSurf-5-1-quilt-dom]
set _DB(7) [pw::GridEntity getByName BSurf-7-quilt-dom]
set _DB(8) [pw::GridEntity getByName BSurf-9-quilt-dom]
set _DB(9) [pw::GridEntity getByName BSurf-11-quilt-dom]
set _TMP(mode_1) [pw::Application begin VolumeMesher [list $_DB(1) $_DB(2) $_DB(3) $_DB(4) $_DB(5) $_DB(6) $_DB(7) $_DB(8) $_DB(9)]]

$_TMP(mode_1) setFarfieldLength { 60 60 }
$_TMP(mode_1) setFarfieldWidth { 60 60 }
$_TMP(mode_1) setFarfieldHeight { 60 60 }
$_TMP(mode_1) setBoundaryLayerType GeometricGrowth
$_TMP(mode_1) setWallNormalSpacing 5.770548344287181e-06
$_TMP(mode_1) setGrowthRate 1.15
$_TMP(mode_1) setMaxIncludedAngle 170
$_TMP(mode_1) setFinalCellAspectRatio 1.0
$_TMP(mode_1) setCollisionBuffer 2
$_TMP(mode_1) setCentroidSkewness 0.8
$_TMP(mode_1) createGridEntities
$_TMP(mode_1) end
            
pw::Application setGridPreference Unstructured
set _TMP(mode_2) [pw::Application begin Create]
set _BL(1) [pw::BlockUnstructured create]
set _DB(1) [pw::GridEntity getByName BSurf-1-0-quilt-dom]
set _DB(2) [pw::GridEntity getByName BSurf-1-1-quilt-dom]
set _DB(3) [pw::GridEntity getByName BSurf-3-0-quilt-dom]
set _DB(4) [pw::GridEntity getByName BSurf-3-1-quilt-dom]
set _DB(5) [pw::GridEntity getByName BSurf-5-0-quilt-dom]
set _DB(6) [pw::GridEntity getByName BSurf-5-1-quilt-dom]
set _DB(7) [pw::GridEntity getByName BSurf-7-quilt-dom]
set _DB(8) [pw::GridEntity getByName BSurf-9-quilt-dom]
set _DB(9) [pw::GridEntity getByName BSurf-11-quilt-dom]
set _DB(10) [pw::GridEntity getByName dom-1]
set _DB(11) [pw::GridEntity getByName dom-2]
set _DB(12) [pw::GridEntity getByName dom-3]
set _DB(13) [pw::GridEntity getByName dom-4]
set _DB(14) [pw::GridEntity getByName dom-5]
set _DB(15) [pw::GridEntity getByName dom-6]
set _TMP(face1)  [pw::FaceUnstructured createFromDomains [list $_DB(1) $_DB(2) $_DB(3) $_DB(4) $_DB(5) $_DB(6) $_DB(7) $_DB(8) $_DB(9) $_DB(10) $_DB(11) $_DB(12) $_DB(13) $_DB(14) $_DB(15)]]
$_BL(1) addFace $_TMP(face1)
$_TMP(mode_2) end

set _BL(2) [pw::GridEntity getByName blk-1]

set _TMP(mode_2) [pw::Application begin UnstructuredSolver [list $_BL(2)]]
    $_BL(2) setUnstructuredSolverAttribute TRexMaximumLayers 100
    $_BL(2) setUnstructuredSolverAttribute TRexFullLayers 1
    $_BL(2) setUnstructuredSolverAttribute TRexGrowthRate 1.15
    $_BL(2) setUnstructuredSolverAttribute TRexPushAttributes True
    $_BL(2) setUnstructuredSolverAttribute TRexSkewCriteriaCentroid 0.8
    $_BL(2) setUnstructuredSolverAttribute TRexSkewCriteriaEquiangle 1
    $_BL(2) setUnstructuredSolverAttribute TRexSkewCriteriaMaximumAngle 170
    $_BL(2) setSizeFieldDecay 0.75
    $_TMP(mode_2) setStopWhenFullLayersNotMet True
    $_TMP(mode_2) setAllowIncomplete True
    $_TMP(mode_2) run Initialize
$_TMP(mode_2) end

pw::Application setCAESolver SU2 3


set _TMP(PW_1) [pw::BoundaryCondition create] 
set _TMP(PW_1) [pw::BoundaryCondition getByName bc-2] 
$_TMP(PW_1) setName wall
$_TMP(PW_1) apply [list [list $_BL(2) $_DB(1)] [list $_BL(2) $_DB(2)] [list $_BL(2) $_DB(3)] [list $_BL(2) $_DB(4)] [list $_BL(2) $_DB(5)] [list $_BL(2) $_DB(6)] [list $_BL(2) $_DB(7)] [list $_BL(2) $_DB(8)] [list $_BL(2) $_DB(9)]]


set _TMP(PW_2) [pw::BoundaryCondition create] 
set _TMP(PW_2) [pw::BoundaryCondition getByName bc-3] 
$_TMP(PW_2) setName symmetry
$_TMP(PW_2) apply [list [list  $_BL(2) $_DB(15)]]


set _TMP(PW_3) [pw::BoundaryCondition create] 
set _TMP(PW_3) [pw::BoundaryCondition getByName bc-4] 
$_TMP(PW_3) setName far_field
$_TMP(PW_3) apply [list [list  $_BL(2) $_DB(10)] [list  $_BL(2) $_DB(11)] [list  $_BL(2) $_DB(12)] [list  $_BL(2) $_DB(13)] [list  $_BL(2) $_DB(14)]]


set _TMP(mode_2) [pw::Application begin CaeExport [pw::Entity sort [list $_BL(2)]]]
  $_TMP(mode_2) initialize -strict -type CAE /home/doktorand/Software/PyAeroSweep-Stan-V3/PyAeroSweep/Test_Cases/Full_3D_wing/Case3/su2meshEx.su2
  $_TMP(mode_2) setAttribute FilePrecision Double
  $_TMP(mode_2) verify
  $_TMP(mode_2) write
$_TMP(mode_2) end

pw::Application save /home/doktorand/Software/PyAeroSweep-Stan-V3/PyAeroSweep/Test_Cases/Full_3D_wing/Case3/mesh_file.pw