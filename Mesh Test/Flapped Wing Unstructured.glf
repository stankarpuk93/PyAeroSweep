# Fidelity Pointwise V18.6 Journal file - Mon Nov 20 14:51:49 2023

package require PWI_Glyph 6.22.1

pw::Application setUndoMaximumLevels 5

pw::Application setCAESolver SU2 3
pw::Application markUndoLevel {Set Dimension 3D}

set _TMP(mode_1) [pw::Application begin Create]
  set _CN(1) [pw::GridEntity getByName con-3]
  set _CN(2) [pw::GridEntity getByName con-8]
  set _CN(3) [pw::GridEntity getByName con-2]
  set _CN(4) [pw::GridEntity getByName con-4]
  set _CN(5) [pw::GridEntity getByName con-1]
  set _CN(6) [pw::GridEntity getByName con-5]
  set _CN(7) [pw::GridEntity getByName con-7]
  set _CN(8) [pw::GridEntity getByName con-6]
  set _CN(9) [pw::GridEntity getByName con-11]
  set _CN(10) [pw::GridEntity getByName con-14]
  set _CN(11) [pw::GridEntity getByName con-13]
  set _CN(12) [pw::GridEntity getByName con-12]
  set _CN(13) [pw::GridEntity getByName con-9]
  set _CN(14) [pw::GridEntity getByName con-10]
  set _TMP(PW_1) [pw::Edge createFromConnectors [list $_CN(1) $_CN(2) $_CN(3) $_CN(4) $_CN(5) $_CN(6) $_CN(7) $_CN(8) $_CN(9) $_CN(10) $_CN(11) $_CN(12) $_CN(13) $_CN(14)]]
  set _TMP(edge_1) [lindex $_TMP(PW_1) 0]
  set _TMP(edge_2) [lindex $_TMP(PW_1) 1]
  set _TMP(edge_3) [lindex $_TMP(PW_1) 2]
  set _TMP(edge_4) [lindex $_TMP(PW_1) 3]
  set _TMP(edge_5) [lindex $_TMP(PW_1) 4]
  unset _TMP(PW_1)
  set _DM(1) [pw::DomainStructured create]
  $_DM(1) addEdge $_TMP(edge_1)
  set _DM(2) [pw::DomainStructured create]
  $_DM(2) addEdge $_TMP(edge_2)
  set _DM(3) [pw::DomainStructured create]
  $_DM(3) addEdge $_TMP(edge_3)
  set _DM(4) [pw::DomainStructured create]
  $_DM(4) addEdge $_TMP(edge_4)
  set _DM(5) [pw::DomainStructured create]
  $_DM(5) addEdge $_TMP(edge_5)
$_TMP(mode_1) end
unset _TMP(mode_1)
set _TMP(mode_1) [pw::Application begin ExtrusionSolver [list $_DM(1) $_DM(2) $_DM(3) $_DM(4) $_DM(5)]]
  $_TMP(mode_1) setKeepFailingStep true
  $_DM(1) setExtrusionSolverAttribute Mode Translate
  $_DM(2) setExtrusionSolverAttribute Mode Translate
  $_DM(3) setExtrusionSolverAttribute Mode Translate
  $_DM(4) setExtrusionSolverAttribute Mode Translate
  $_DM(5) setExtrusionSolverAttribute Mode Translate
  $_DM(1) setExtrusionSolverAttribute TranslateDirection {1 0 0}
  $_DM(2) setExtrusionSolverAttribute TranslateDirection {1 0 0}
  $_DM(3) setExtrusionSolverAttribute TranslateDirection {1 0 0}
  $_DM(4) setExtrusionSolverAttribute TranslateDirection {1 0 0}
  $_DM(5) setExtrusionSolverAttribute TranslateDirection {1 0 0}
  $_DM(1) setExtrusionSolverAttribute TranslateDirection {-0 -0 -1}
  $_DM(2) setExtrusionSolverAttribute TranslateDirection {-0 -0 -1}
  $_DM(3) setExtrusionSolverAttribute TranslateDirection {-0 -0 -1}
  $_DM(4) setExtrusionSolverAttribute TranslateDirection {-0 -0 -1}
  $_DM(5) setExtrusionSolverAttribute TranslateDirection {-0 -0 -1}
  $_DM(1) setExtrusionSolverAttribute TranslateDistance 100
  $_DM(2) setExtrusionSolverAttribute TranslateDistance 100
  $_DM(3) setExtrusionSolverAttribute TranslateDistance 100
  $_DM(4) setExtrusionSolverAttribute TranslateDistance 100
  $_DM(5) setExtrusionSolverAttribute TranslateDistance 100
  $_TMP(mode_1) run 10
$_TMP(mode_1) end
unset _TMP(mode_1)
unset _TMP(edge_5)
unset _TMP(edge_4)
unset _TMP(edge_3)
unset _TMP(edge_2)
unset _TMP(edge_1)
pw::Application markUndoLevel {Extrude, Translate}

