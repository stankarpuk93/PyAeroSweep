# Pointwise V18.3 Journal file - Fri Dec  9 23:06:25 2022

package require PWI_Glyph 3.18.3

pw::Application setUndoMaximumLevels 5
pw::Application reset
pw::Application markUndoLevel {Journal Reset}

pw::Application clearModified


# import airfoil components
set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic "G:/TUBS/HiWi/Dr Karpuk/PyAeroSweep-Stan-V2/Quasi 3D/main_airfoil_upper.dat"
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic "G:/TUBS/HiWi/Dr Karpuk/PyAeroSweep-Stan-V2/Quasi 3D/main_airfoil_lower.dat"
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic "G:/TUBS/HiWi/Dr Karpuk/PyAeroSweep-Stan-V2/Quasi 3D/main_airfoil_cut1.dat"
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic "G:/TUBS/HiWi/Dr Karpuk/PyAeroSweep-Stan-V2/Quasi 3D/main_airfoil_cut2.dat"
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic "G:/TUBS/HiWi/Dr Karpuk/PyAeroSweep-Stan-V2/Quasi 3D/flap_airfoil_lower.dat"
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Automatic "G:/TUBS/HiWi/Dr Karpuk/PyAeroSweep-Stan-V2/Quasi 3D/flap_airfoil_upper.dat"
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end


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



# Assign nodes to each connector
set _CN(1) [pw::GridEntity getByName con-1]
$_CN(1) setDimension 200

set _CN(2) [pw::GridEntity getByName con-2]
$_CN(2) setDimension 120

set _CN(3) [pw::GridEntity getByName con-6]
$_CN(3) setDimension 150

set _CN(4) [pw::GridEntity getByName con-5]
$_CN(4) setDimension 150

set _CN(5) [pw::GridEntity getByName con-3]
$_CN(5) setDimension 70

set _CN(6) [pw::GridEntity getByName con-4]
$_CN(6) setDimension 25

set _CN(7) [pw::GridEntity getByName con-7]
$_CN(7) setDimension 8

set _CN(8) [pw::GridEntity getByName con-8]
$_CN(8) setDimension 8


# Cluster points at each connetor
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

set _CN(3) [pw::GridEntity getByName con-3]
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(3)]]
  set _TMP(PW_1) [$_CN(1) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0.001
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(3) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0.001
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(3)]]
  set _TMP(PW_1) [$_CN(1) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0.0005
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(3) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0.0005
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _CN(4) [pw::GridEntity getByName con-7]
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(4)]]
  set _TMP(PW_1) [$_CN(4) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0.0005
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(4) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0.0005
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Modify [list $_CN(2)]]
  set _TMP(PW_1) [$_CN(2) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0.001
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _CN(5) [pw::GridEntity getByName con-4]
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(5)]]
  set _TMP(PW_1) [$_CN(5) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0.001
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Modify [list $_CN(3)]]
  set _TMP(PW_1) [$_CN(3) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0.005
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Modify [list $_CN(5)]]
  set _TMP(PW_1) [$_CN(5) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0.005
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _CN(6) [pw::GridEntity getByName con-5]
set _CN(7) [pw::GridEntity getByName con-6]
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(6) $_CN(7)]]
  set _TMP(PW_1) [$_CN(6) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0.001
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(7) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0.001
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Modify [list $_CN(6) $_CN(7)]]
  set _TMP(PW_1) [$_CN(6) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0.0005
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(7) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0.0005
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _CN(8) [pw::GridEntity getByName con-8]
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(8)]]
  set _TMP(PW_1) [$_CN(8) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0.0005
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(8) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0.0005
  unset _TMP(PW_1)
$_TMP(mode_1) end


# Create far-field boundaries
set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  $_TMP(PW_1) delete
  unset _TMP(PW_1)
$_TMP(mode_1) abort
unset _TMP(mode_1)
set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  $_TMP(PW_1) addPoint { 60 60 0 }
  $_TMP(PW_1) addPoint { 60 -60 0 }
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
  $_TMP(PW_1) addPoint { -60 -60 0 }
  set _CN(2) [pw::Connector create]
  $_CN(2) addSegment $_TMP(PW_1)
  unset _TMP(PW_1)
  $_CN(2) calculateDimension
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  $_TMP(PW_1) addPoint [$_CN(2) getPosition -arc 1]
  $_TMP(PW_1) addPoint { -60 60 0 }
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
  $_TMP(PW_1) do setDimension 20



# Create near field
set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentCircle create]
  $_TMP(PW_1) addPoint {0.5 3.4351145038167936 0}
  $_TMP(PW_1) addPoint {0.5 0 0}
  $_TMP(PW_1) setEndAngle 360 {0 0 1}
  set _CN(1) [pw::Connector create]
  $_CN(1) addSegment $_TMP(PW_1)
  $_CN(1) calculateDimension
  unset _TMP(PW_1)
$_TMP(mode_1) end

set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentCircle create]
  $_TMP(PW_1) addPoint {0.5 17.175572519083968 0}
  $_TMP(PW_1) addPoint {0.5 0 0}
  $_TMP(PW_1) setEndAngle 360 {0 0 1}
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
  $_TMP(PW_1) do setDimension 100


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
  pw::Entity transform [pwu::Transform scaling -anchor {0 0 0} {2.62 2.62 2.62}] [$_TMP(mode_1) getEntities]
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
  $_DM(1) setUnstructuredSolverAttribute BoundaryDecay 0.75
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
  $_DM(1) setUnstructuredSolverAttribute BoundaryDecay 0.85
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
  $_TMP(PW_3) setValue 4.9080049524228e-06
  $_DM(1) setUnstructuredSolverAttribute TRexMaximumLayers 100
  $_DM(1) setUnstructuredSolverAttribute TRexFullLayers 60
  $_DM(1) setUnstructuredSolverAttribute TRexGrowthRate 1.1
  $_DM(1) setUnstructuredSolverAttribute TRexGrowthRate 1.1
  $_DM(1) setUnstructuredSolverAttribute TRexPushAttributes True
  $_DM(1) setUnstructuredSolverAttribute BoundaryDecay 0.85
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



# Export the mesh
set _DM(1) [pw::GridEntity getByName dom-1]
set _DM(2) [pw::GridEntity getByName dom-2]
set _DM(3) [pw::GridEntity getByName dom-3]
set _TMP(mode_1) [pw::Application begin CaeExport [pw::Entity sort [list $_DM(1) $_DM(2) $_DM(3)]]]
  $_TMP(mode_1) initialize -strict -type CAE "G:/TUBS/HiWi/Dr Karpuk/PyAeroSweep-Stan-V2/Quasi 3D/su2meshExtrusion.su2"
  $_TMP(mode_1) setAttribute FilePrecision Double
  $_TMP(mode_1) verify
  $_TMP(mode_1) write
$_TMP(mode_1) end
unset _TMP(mode_1)


# Extrude the mesh

package require PWI_Glyph 3.18.3

pw::Application setUndoMaximumLevels 5

pw::Application setCAESolver CGNS 3
pw::Application markUndoLevel {Select Solver}

pw::Application setCAESolver CGNS 3
pw::Application markUndoLevel {Set Dimension 3D}

set _TMP(mode_1) [pw::Application begin Create]
  set _DM(1) [pw::GridEntity getByName dom-2]
  set _DM(2) [pw::GridEntity getByName dom-1]
  set _DM(3) [pw::GridEntity getByName dom-3]
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
  $_BL(1) setExtrusionSolverAttribute TranslateDirection {-0 -0 -1}
  $_BL(1) setExtrusionSolverAttribute TranslateDistance 100
  $_TMP(mode_1) run 1
$_TMP(mode_1) end
unset _TMP(mode_1)
unset _TMP(face_1)
pw::Application markUndoLevel {Extrude, Translate}

pw::Application setCAESolver SU2 3
pw::Application markUndoLevel {Select Solver}

set _TMP(PW_1) [pw::BoundaryCondition create]
pw::Application markUndoLevel {Create BC}

unset _TMP(PW_1)
set _TMP(PW_1) [pw::BoundaryCondition getByName bc-4]
$_TMP(PW_1) apply [list [list $_BL(1) $_DM(2)] [list $_BL(1) $_DM(1)] [list $_BL(1) $_DM(3)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_1) setName symmetry
pw::Application markUndoLevel {Name BC}

unset _TMP(PW_1)
unset _TMP(PW_2)

set _BL(1) [pw::GridEntity getByName blk-1]
set _DM(1) [pw::GridEntity getByName dom-1]
set _DM(2) [pw::GridEntity getByName dom-2]
set _DM(3) [pw::GridEntity getByName dom-3]
set _DM(4) [pw::GridEntity getByName dom-4]
set _DM(5) [pw::GridEntity getByName dom-5]
set _DM(6) [pw::GridEntity getByName dom-6]
set _DM(7) [pw::GridEntity getByName dom-7]
set _DM(8) [pw::GridEntity getByName dom-8]
set _DM(9) [pw::GridEntity getByName dom-9]
set _DM(10) [pw::GridEntity getByName dom-10]
set _DM(11) [pw::GridEntity getByName dom-11]
set _DM(12) [pw::GridEntity getByName dom-12]
set _DM(13) [pw::GridEntity getByName dom-13]
set _DM(14) [pw::GridEntity getByName dom-14]
set _DM(15) [pw::GridEntity getByName dom-15]
set _DM(16) [pw::GridEntity getByName dom-16]
set _DM(17) [pw::GridEntity getByName dom-17]
set _DM(18) [pw::GridEntity getByName dom-18]
set _TMP(mode_1) [pw::Application begin CaeExport [pw::Entity sort [list $_BL(1) $_DM(1) $_DM(2) $_DM(3) $_DM(4) $_DM(5) $_DM(6) $_DM(7) $_DM(8) $_DM(9) $_DM(10) $_DM(11) $_DM(12) $_DM(13) $_DM(14) $_DM(15) $_DM(16) $_DM(17) $_DM(18)]]]
  $_TMP(mode_1) initialize -strict -type CAE "G:/TUBS/HiWi/Dr Karpuk/PyAeroSweep-Stan-V2/Quasi 3D/su2meshExtrusion.su2"
  $_TMP(mode_1) initialize -strict -type CAE "G:/TUBS/HiWi/Dr Karpuk/PyAeroSweep-Stan-V2/Quasi 3D/su2meshExtrusion.su2"
  $_TMP(mode_1) verify
  $_TMP(mode_1) write
$_TMP(mode_1) end
unset _TMP(mode_1)


