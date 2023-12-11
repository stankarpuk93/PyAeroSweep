# Fidelity Pointwise V18.6 Journal file - Tue Nov 21 21:27:42 2023

package require PWI_Glyph 6.22.1

pw::Application setUndoMaximumLevels 5

pw::Application setCAESolver SU2 3
pw::Application markUndoLevel {Set Dimension 3D}

pw::Application setGridPreference Structured
pw::Application setGridPreference Unstructured
