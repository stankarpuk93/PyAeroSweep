#Geometry.py
# 
# Created:  Nov 2023, S. Karpuk, 
# Modified: 
#           


# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import pyiges
import mpi4py
import numpy as np
from Core.Data              import Data
from Core.ContainerOrdered  import ContainerOrdered




class Geometry():

    def __init__(self):
        
        self.reference_values = {
            "Area"   : 1.0,
            "Length" : 1.0,
            "Depth"  : 1.0,
            "Point"  : [0.25*1.0,0.0,0.0]              # reference point about which the moment is taken
        }

        self.Segments = ContainerOrdered()

        self.polynomial_fit         = 2
        self.blunt_trailing_edge    = True
        self.rounded_trailing_edge  = True
        self.trailing_edge_height   = 0.002

        self.type = 'wing'

        self.generate = True


    def append_segment(self,segment):
        """ Adds a segment to the wing 
    
        Assumptions:
        None

        Source:
        N/A

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A
        """ 

        # Assert database type
        if not isinstance(segment,Data):
            raise Exception('input component must be of type Data()')

        # Store data
        self.Segments.append(segment)

        return
    

    def create_wing_geometry(self):
        """ Creates a wing geometry using pygeo
    
        Assumptions:
        Pareview V5.1 or newer required

        Source:
        https://mdolab-pygeo.readthedocs-hosted.com/en/latest/index.html

        Inputs:
        None

        Outputs:
        None

        Properties Used:
        N/A

        """ 

        num_segm = len(self.Segments.keys())


        # Pre-process wing sections for pygeo
        airfoil_list        = []
        chords              = np.zeros(num_segm)
        leading_edge_points = np.zeros((3,num_segm))
        rotation_angles     = np.zeros((3,num_segm))
        offsets             = np.zeros((num_segm,2))
        for i in range(num_segm):
            chords[i] = self.Segments[i].chord
            airfoil_list.append(self.Segments[i].Airfoil.files['merged'])

            if i == 0:
                segm_rot = 0.0 
            else:
                if self.Segments[i].rotate is True:
                    segm_rot = -self.Segments[i-1].dihedral
                else:
                    segm_rot = 0.0              
            rotation_angles[:,i] = [segm_rot,0,-self.Segments[i].incidence]

            if i > 0:
                sweep    = self.Segments[i-1].leading_edge_sweep
                dihedral = self.Segments[i-1].dihedral
                Xref     = leading_edge_points[0,i-1]
                Yref     = leading_edge_points[1,i-1]
                Zref     = self.Segments[i-1].spanwise_location
                dZ       = self.Segments[i].spanwise_location - self.Segments[i-1].spanwise_location
                leading_edge_points[0,i] = Xref + dZ * np.tan(np.radians(sweep))
                leading_edge_points[1,i] = Yref + dZ * np.tan(np.radians(dihedral))
                leading_edge_points[2,i] = Zref + dZ
            

        print(leading_edge_points[0,:])
        print(leading_edge_points[1,:])
        print(leading_edge_points[2,:])
        print(rotation_angles[0,:])
        print(rotation_angles[1,:])
        print(rotation_angles[2,:])

        # Build the wing
        from pygeo  import pyGeo

        wing = pyGeo(
        "liftingSurface",
        xsections   = airfoil_list,
        scale       = chords,
        offset      = offsets,
        x           = leading_edge_points[0,:],
        y           = leading_edge_points[1,:],
        z           = leading_edge_points[2,:],
        rotX        = rotation_angles[0,:],
        rotY        = rotation_angles[1,:],
        rotZ        = rotation_angles[2,:],
        bluntTe     = self.blunt_trailing_edge,
        roundedTe   = self.rounded_trailing_edge,
        teHeightScaled = self.trailing_edge_height,
        kSpan = self.polynomial_fit,
        nCtl  = 100,
        tip   = "rounded",
        )
        
        # Write the output geometry to a file
        wing.writeIGES(self.filename + ".igs")

        if self.output_format == "VTK":
            iges = pyiges.read(self.filename + ".igs")
            mesh = iges.to_vtk(bsplines=False, surfaces=True, merge=True, delta=0.05)
            mesh.save('mesh.vtk')

        elif self.output_format == 'Tecplot':
            wing.writeTecplot(self.filename + "_Tecplot.dat")

        else:
            pass

        mpi4py.MPI.Finalize()


        return


    







