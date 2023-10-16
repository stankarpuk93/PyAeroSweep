# glyph_updater.py

def update_glyph_script(glyph_file):
    lines_to_update = [14, 20, 46, 49, 52, 59, 62, 68, 71, 80, 97, 98, 99, 100, 101, 102, 139]
    new_values = [
        "  $_TMP(mode_1) initialize -strict -type Automatic G:\TUBS\HiWi\Dr Karpuk\Version\AF_CFD_V1\main_airfoil_upper.dat",
        "  $_TMP(mode_1) initialize -strict -type Automatic G:\TUBS\HiWi\Dr Karpuk\Version\AF_CFD_V1\main_airfoil_lower.dat",
        "$_CN(1) setDimension 200",
        "$_CN(2) setDimension 200",
        "$_CN(3) setDimension 8",
        "  $_TMP(PW_1) setBeginSpacing 0.001",
        "  $_TMP(PW_1) setEndSpacing 0.001",
        "  $_TMP(PW_1) setEndSpacing 0.0005",
        "  pw::Entity transform [pwu::Transform scaling -anchor {0 0 0} {2.62 2.62 2.62}] [$_TMP(mode_1) getEntities]",
        "  $_DM(1) setExtrusionSolverAttribute NormalMarchingVector {-0 -0 -1}",
        "  $_DM(1) setExtrusionSolverAttribute NormalInitialStepSize 0.000004321153531829642",
        "  $_DM(1) setExtrusionSolverAttribute StopAtHeight Off",
        "  $_DM(1) setExtrusionSolverAttribute StopAtHeight 529",
        "  $_TMP(mode_1) run 254",
        "  $_TMP(mode_1) run -1",
        "  $_TMP(mode_1) initialize -strict -type CAE G:\TUBS\HiWi\Dr Karpuk\Version\AF_CFD_V1\su2meshEx.su2",
    ]

    # Read the entire content of the Glyph script
    with open(glyph_file, 'r') as glyph_script:
        glyph_lines = glyph_script.readlines()

    # Update specific lines in the Glyph script with new values
    for i in range(len(lines_to_update)):
        line_number = lines_to_update[i]
        if 0 < line_number <= len(glyph_lines) and i < len(new_values):
            glyph_lines[line_number - 1] = new_values[i] + '\n'  # Line numbers are 1-based

    # Write the updated content back to the Glyph script file
    with open(glyph_file, 'w') as updated_glyph_script:
        updated_glyph_script.writelines(glyph_lines)
