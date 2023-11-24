# Fidelity Pointwise V18.6 Journal file - Fri Nov 24 13:59:33 2023

package require PWI_Glyph 6.22.1

pw::Application setUndoMaximumLevels 5

pw::Application setCAESolver SU2 3
pw::Application markUndoLevel {Set Dimension 3D}

set _TMP(mode_2) [pw::Application begin Create]
  set _DM(1) [pw::GridEntity getByName dom-1]
  set _TMP(PW_1) [pw::FaceStructured createFromDomains [list $_DM(1)]]
  set _TMP(face_1) [lindex $_TMP(PW_1) 0]
  unset _TMP(PW_1)
  set _BL(1) [pw::BlockStructured create]
  $_BL(1) addFace $_TMP(face_1)
$_TMP(mode_2) end
unset _TMP(mode_2)
set _TMP(mode_2) [pw::Application begin ExtrusionSolver [list $_BL(1)]]
  $_TMP(mode_2) setKeepFailingStep true
  $_BL(1) setExtrusionSolverAttribute Mode Translate
  $_BL(1) setExtrusionSolverAttribute TranslateDirection {1 0 0}
  $_BL(1) setExtrusionSolverAttribute TranslateDirection {-0 -0 -1}
  $_BL(1) setExtrusionSolverAttribute TranslateDistance 100
  $_TMP(mode_2) run 1
$_TMP(mode_2) end
unset _TMP(mode_2)
unset _TMP(face_1)
pw::Application markUndoLevel {Extrude, Translate}

