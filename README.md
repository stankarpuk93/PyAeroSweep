<h1> PyAeroSweep </h1>

<h2> Introduction </h2>

**PyAeroSweep** is a multi-functional tool that performs aerodynamic sweeps of airfoils and wings using high-fidelity CFD methods.

**PyAeroSweep** can perform a range of pre-processing and simulation tasks:

1.  Generation of airfoil and wing geometries of various kinds:
    + **Airfoils**
        - Airfoils can be generated using PARSEC of CST parametrization methods
        - A droop nose, plain, or slotted flaps can be defined for given airfoils
        - Airfoil coordinates are imported in typical text formats
    + **Wings**
        - Generation of piesewise wing planforms using the Pygeo framework
        - Wing planforms are exported in the .igs format
        - Only clean planform capabilities are available
2. Automatic geometry meshing using Pointwise:
    + Meshing is performed using pre-defined templates that can be parameterically tuned for a particular problem
    + Viscous layers are added for unstructured meshes using TREX
    + **Airfoils**
        + Structured and unstructured mesh options available
        + Meshing of externally imported airfils is possible
    + **Wings**
        + Meshes the wing surface using the Pointwise automatic mesh generation method
3. CFD solution using SU2:
    + At the moment, can only run RANS solutions. Euler solutions are planned
    + 3D solutions for wings are currently available only with a symmetry plane
    + angle-of-attack, altitude, and Mach number sweeps are possible
    + The tool can run a similar mesh created externally


<h2> Prerequisites </h2>

The follosing set of tools must be installed to enable all capabilities:

1. Pointwise V18.6+ (https://www.pointwise.com/) 
2. SU2 v7.0+        (https://su2code.github.io/)
3. pygeo            (https://mdolab-pygeo.readthedocs-hosted.com/en/latest/?badge=latest)
4. preFoil          (https://mdolab-prefoil.readthedocs-hosted.com/en/latest/)
5. OpenMPI          (https://www.open-mpi.org/)


<h2> Installation </h2>

To use the tool, just download the directory


<h2> Testing and execution </h2>

To test the code and ensure that all cababilities are available, run cases located in the <em>Test_Cases</em> directory. 

To run the case: 

1. Use any IDE environment (for example, Visual Studio Code)
2. Allocate the working directory to the main one, where all software folders and the file <em>Run_aerodynamic_analysis.py</em> are allocated.
3. Open the file <em>Input_data.py</em> in the test case file of your interest and update all common directory variables (working directory, Pointwise execution file directory, etc).
4. Run the file


<h2> Creating your cases </h2>

Currently, the best practice is to use sample cases available as test cases and update them according to the problem of an interest.