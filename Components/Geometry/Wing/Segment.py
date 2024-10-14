#Segment.py
# 
# Created:  Nov 2023, S. Karpuk, 
# Modified: July 2024. Chr. Carstensen (added .dat method)
#           


# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------
import os
import bezier
import random
import mpi4py
import numpy as np
import matplotlib.pyplot    as plt

from Core.Data          import Data
from Methods.Geometry   import parsec_functions     as pc_func
from Components.Geometry.Airfoil.Bezier_curves_airfoil  import QuadBezier, RationalizedQuadBezier
from Methods.Geometry.miscellaneous_geometry import compute_line_intersection, \
                                                    allocate_line_points_Bezier



class Segment():

    def __init__(self):
        """This sets the default for wing segments in SUAVE.

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
        self.tag = 'segment'
        self.spanwise_location   = 0.0
        self.incidence           = 0.0
        self.chord               = 0.0
        self.dihedral            = 0.0
        self.leading_edge_sweep  = 0.0
        self.rotate              = False
        self.Airfoil             = Data()

        self.plot_airfoil       = False

        # Airfoil definition constants based on the PARSEC method
        self.Airfoil.PARSEC     = {}

        # Airfoil definition constants based on the CST method
        self.Airfoil.CST         = {}

        # Airfoil definition constants based on DAT file
        self.Airfoil.DAT         = {}

        # Airfoil files are used either to write PARSEC-generated 
        # airfoil and then read by Pointwise or to read directly from them
        self.Airfoil.files       = {}   

        self.LeadingEdgeDevice   = self.LeadingEdgeDevice()  
        self.TrailingEdgeDevice  = self.TrailingEdgeDevice()        


    def create_CST_airfoil(self):
        '''Draw an airfoil based on input CST coefficients, 
           draw high-lift devices, and export coordinates into data files
        
            Inputs:
                Geometry.CST["upper"]
                         CST["lower"]

            Outputs:
            

            
            Assumptions:

        '''

        from pygeo.parameterization.DVGeoCST import DVGeometryCST
        
        # Constants
        xte     = 1.0
        yte_suc = 0.002


        # Unpack inputs 
        Airfoil = self.Airfoil.CST

        # Initialize x-coordinates
        xx_pre0 = np.flip(1 - (1 - np.cos(np.linspace(0, 1, int(np.ceil(201/2))) * np.pi)) / 2)              
        xx_suc = (1 - np.cos(np.linspace(0, 1, int(np.ceil(201/2))) * np.pi)) / 2 

        # compute y-coordinates 
        yy_pre0 = DVGeometryCST.computeCSTCoordinates(xx_pre0,Airfoil["N1 lower"],Airfoil["N2 lower"],\
                                                     Airfoil["lower"],Airfoil["yte lower"])
        yy_suc = DVGeometryCST.computeCSTCoordinates(xx_suc,Airfoil["N1 upper"],Airfoil["N2 upper"],\
                                                     Airfoil["upper"],Airfoil["yte upper"])

        xx_pre = xx_pre0[::-1]
        yy_pre = yy_pre0[::-1]

        # Draw a droop nose
        if len(self.LeadingEdgeDevice.PARSEC) != 0:
            LE_device      = self.LeadingEdgeDevice.PARSEC
            droop_nose_set = [LE_device["delta_s"], LE_device["cs_c"], 
                              LE_device["d_cs_up"], LE_device["d_cs_low"], 
                              LE_device['w_con_seal']]
            xx_pre,xx_suc,yy_pre,yy_suc = self.deploy_simple_flap(xx_pre,xx_suc,yy_pre,yy_suc,droop_nose_set,'droop')

        # Draw a flap
        if len(self.TrailingEdgeDevice.PARSEC) != 0:  
            TE_device = self.TrailingEdgeDevice.PARSEC
            if self.TrailingEdgeDevice.type == 'Plain':
                flap_data = [TE_device["delta_f"], TE_device["cf_c"], 
                             TE_device["d_cf_up"], TE_device["d_cf_low"], 
                             TE_device['w_con_seal']]
                xx_no_fl_pre,xx_no_fl_suc,yy_no_fl_pre,yy_no_fl_suc = self.deploy_simple_flap(xx_pre,xx_suc,yy_pre,yy_suc,flap_data,'flap')                
                xx_fl_pre = []
                xx_fl_suc = []
                yy_fl_pre = []
                yy_fl_suc = []
                flap_cut1 = []
                flap_cut2 = []
            elif self.TrailingEdgeDevice.type == 'Slotted':
                flap_setting = [TE_device["delta_f"], TE_device["x_gap"], TE_device["y_gap"]] 
                flap_data    = [TE_device["cf_c"],TE_device["ce_c"],TE_device["csr_c"],
                                TE_device["clip_ext"],TE_device["r_le_flap"],
                                TE_device["tc_shr_tip"],TE_device["w_conic"]]
                flap_data.append(xte)
                flap_data.append(yte_suc)
                xx_no_fl_suc, yy_no_fl_suc, xx_no_fl_pre, yy_no_fl_pre, xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre, flap_cut1, flap_cut2 = self.compute_flap(xx_suc,yy_suc,xx_pre,yy_pre,flap_data)
                xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre = self.deploy_flap(xx_no_fl_suc, yy_no_fl_suc, xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre, flap_setting)
        else:
            xx_no_fl_suc = xx_suc
            yy_no_fl_suc = yy_suc
            xx_no_fl_pre = xx_pre
            yy_no_fl_pre = yy_pre
            xx_fl_pre = []
            xx_fl_suc = []
            yy_fl_pre = []
            yy_fl_suc = []
            flap_cut1 = []
            flap_cut2 = []


        # Output airfoiil data
        self.output_airfoil(xx_no_fl_pre,xx_no_fl_suc,yy_no_fl_pre,yy_no_fl_suc,[],[],xte,xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre, flap_cut1, flap_cut2)


        mpi4py.MPI.Finalize()


        return        






    def create_PARSEC_airfoil(self):
        '''Draw an airfoil based on input PARSEC coefficients, 
           draw high-lift devices, and export coordinates into data files
        
            Inputs:
                Geometry.PARSEC_airfoil.rle          Main airfoil LE radius
                                        x_pre        x-location of the crest on the pressure side
                                        y_pre        y-location of the crest on the pressure side
                                        d2ydx2_pre   curvature of the crest on the pressure side
                                        th_pre       trailing edge angle on the pressure side [deg]
                                        x_suc        x-location of the crest on the suction side        
                                        y_suc        y-location of the crest on the suction side    
                                        d2ydx2_suc   curvature of the crest on the suction side
                                        th_suc       trailing edge angle on the suction side [deg]

                                        cf_c         flap chord ratio
                                        ce_c         conical curve extent ratio wrt the flap chord length
                                        csr_c        shroud chord ratio
                                        clip_ext     shroud lip extent ratio wrt the airfoil
                                        r_le_flap    flap leading edge radius
                                        tc_shr_tip   shroud tip thickness
                                        w_conic      conical parameter for the suction side of the flap airfoil

                                        delta_f      flap deflection [deg]
                                        x_gap        x-length gap from the shroud TE (positive value is moving the flap left)
                                        y_gap        y-length gap from the shroud TE (positive value is moving the flap down)    

                        PARSEC_droop.delta_s         Droop nose deflection [deg]
                                    cs_s            Droop nose chord ratio
                                    d_cs_up
                                    d_cs_low
                                    k_Bez1
                                    k_Bez2

                        PARSEC_flap.delta_f         Flap deflection [deg]
                                    x_gap           x-length gap from the shroud TE (positive value is moving the flap left)
                                    y_gap           y-length gap from the shroud TE (positive value is moving the flap down)    
                                    cf_c            flap chord ratio
                                    ce_c            conical curve extent ratio wrt the flap chord length
                                    csr_c           shroud chord ratio 
                                    clip_ext        shroud lip extent ratio wrt the flap  
                                    r_le_flap       flap leading edge radius
                                    tc_shr_tip      shroud tip thickness
                                    w_conic         conical parameter for the suction side of the flap airfoil

            Outputs:
            

            
            Assumptions:


        '''


        # Unpack inputs and arrange into a list
        Airfoil      = self.Airfoil.PARSEC
        airfoil_data = [Airfoil["rle"], Airfoil["x_pre"], Airfoil["y_pre"], Airfoil["d2ydx2_pre"], 
                        Airfoil["th_pre"], Airfoil["x_suc"], Airfoil["y_suc"], Airfoil["d2ydx2_suc"], Airfoil["th_suc"]]


        # Define TE & LE of airfoil (normalized, chord = 1)
        xle     = 0.0
        yle     = 0.0
        xte     = 1.0
        yte_suc = self.Airfoil.PARSEC["yte upper"]
        yte_pre = self.Airfoil.PARSEC["yte lower"]
        airfoil_data.append(xle)
        airfoil_data.append(yle)
        airfoil_data.append(xte)
        airfoil_data.append(yte_suc)
        airfoil_data.append(yte_pre)


        # Calculate airfoil coordinates using the PARSEC method                                            
        cf_pre,cf_suc,xx_pre,xx_suc,yy_pre,yy_suc = self.compute_airfoil(airfoil_data)

        # Draw a droop nose
        if len(self.LeadingEdgeDevice.PARSEC) != 0:
            LE_device      = self.LeadingEdgeDevice.PARSEC
            droop_nose_set = [LE_device["delta_s"], LE_device["cs_c"], 
                              LE_device["d_cs_up"], LE_device["d_cs_low"], 
                              LE_device['w_con_seal']]
            xx_pre,xx_suc,yy_pre,yy_suc = self.deploy_simple_flap(xx_pre,xx_suc,yy_pre,yy_suc,droop_nose_set,'droop')


        # Draw a flap
        if len(self.TrailingEdgeDevice.PARSEC) != 0:  
            TE_device = self.TrailingEdgeDevice.PARSEC
            if self.TrailingEdgeDevice.type == 'Plain':
                flap_data = [TE_device["delta_f"], TE_device["cf_c"], 
                             TE_device["d_cf_up"], TE_device["d_cf_low"], 
                             TE_device['w_con_seal']]
                xx_no_fl_pre,xx_no_fl_suc,yy_no_fl_pre,yy_no_fl_suc = self.deploy_simple_flap(xx_pre,xx_suc,yy_pre,yy_suc,flap_data,'flap')                
                xx_fl_pre = []
                xx_fl_suc = []
                yy_fl_pre = []
                yy_fl_suc = []
                flap_cut1 = []
                flap_cut2 = []
            elif self.TrailingEdgeDevice.type == 'Slotted':
                flap_setting = [TE_device["delta_f"], TE_device["x_gap"], TE_device["y_gap"]] 
                flap_data    = [TE_device["cf_c"],TE_device["ce_c"],TE_device["csr_c"],
                                TE_device["clip_ext"],TE_device["r_le_flap"],
                                TE_device["tc_shr_tip"],TE_device["w_conic"]]
                flap_data.append(xte)
                flap_data.append(yte_suc)
                xx_no_fl_suc, yy_no_fl_suc, xx_no_fl_pre, yy_no_fl_pre, xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre, flap_cut1, flap_cut2 = self.compute_flap(xx_suc,yy_suc,xx_pre,yy_pre,flap_data)
                xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre = self.deploy_flap(xx_no_fl_suc, yy_no_fl_suc, xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre, flap_setting)
        else:
            xx_no_fl_suc = xx_suc
            yy_no_fl_suc = yy_suc
            xx_no_fl_pre = xx_pre
            yy_no_fl_pre = yy_pre
            xx_fl_pre = []
            xx_fl_suc = []
            yy_fl_pre = []
            yy_fl_suc = []
            flap_cut1 = []
            flap_cut2 = []


        # Output airfoiil data
        self.output_airfoil(xx_no_fl_pre,xx_no_fl_suc,yy_no_fl_pre,yy_no_fl_suc,cf_pre,cf_suc,xte,xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre, flap_cut1, flap_cut2)



        return
    
    def create_DAT_airfoil(self):
        '''Draw an airfoil based on .dat file
           draw high-lift devices, and export coordinates into data files
        
            Inputs:
                Geometry.DAT["upper"]
                         DAT["lower"]

            Outputs:
            

            
            Assumptions:

        '''

        # Unpack inputs 
        Airfoil = self.Airfoil.DAT

        # Assign inputs
        datax = Airfoil["datax"]
        datay = Airfoil["datay"]
        
        # Get total lenght of .dat coordinates
        length=len(datax)

        # Find coordinate to split upper from lower surface
        NULL = datax.tolist().index(0)

        if datay[NULL] != 0.:
             quit("Non zero y value at x = 0 (y value = " + str(datax[NULL]) + " at split x coordinate of .dat file. Check .dat file or dismissal of first lines in input.")

        xx_pre0 = datax[0:NULL+1]
        yy_pre0 = datay[0:NULL+1]
        
        xx_pre = xx_pre0
        yy_pre = yy_pre0


        xx_suc = datax[NULL:length+1]


        yy_suc = datay[NULL:length+1]

        # # Uncomment to debug dat file
        # print("Suction Side")
        # print(xx_suc)
        # print(yy_suc)

        # print("Presure Side")
        # print(xx_pre)
        # print(yy_pre)

        # derive max trialing edge coordinate x
        xte     = max(xx_suc)
        yte_suc = yy_suc[len(yy_suc)-1]
        #print(yte_suc)

        # Draw a droop nose
        if len(self.LeadingEdgeDevice.PARSEC) != 0:
            LE_device      = self.LeadingEdgeDevice.PARSEC
            droop_nose_set = [LE_device["delta_s"], LE_device["cs_c"], 
                              LE_device["d_cs_up"], LE_device["d_cs_low"], 
                              LE_device['w_con_seal']]
            xx_pre,xx_suc,yy_pre,yy_suc = self.deploy_simple_flap(xx_pre,xx_suc,yy_pre,yy_suc,droop_nose_set,'droop')

        # Draw a flap
        if len(self.TrailingEdgeDevice.PARSEC) != 0:  
            TE_device = self.TrailingEdgeDevice.PARSEC
            if self.TrailingEdgeDevice.type == 'Plain':
                flap_data = [TE_device["delta_f"], TE_device["cf_c"], 
                             TE_device["d_cf_up"], TE_device["d_cf_low"], 
                             TE_device['w_con_seal']]
                xx_no_fl_pre,xx_no_fl_suc,yy_no_fl_pre,yy_no_fl_suc = self.deploy_simple_flap(xx_pre,xx_suc,yy_pre,yy_suc,flap_data,'flap')                
                xx_fl_pre = []
                xx_fl_suc = []
                yy_fl_pre = []
                yy_fl_suc = []
                flap_cut1 = []
                flap_cut2 = []
            elif self.TrailingEdgeDevice.type == 'Slotted':
                flap_setting = [TE_device["delta_f"], TE_device["x_gap"], TE_device["y_gap"]] 
                flap_data    = [TE_device["cf_c"],TE_device["ce_c"],TE_device["csr_c"],
                                TE_device["clip_ext"],TE_device["r_le_flap"],
                                TE_device["tc_shr_tip"],TE_device["w_conic"]]
                flap_data.append(xte)
                flap_data.append(yte_suc)
                xx_no_fl_suc, yy_no_fl_suc, xx_no_fl_pre, yy_no_fl_pre, xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre, flap_cut1, flap_cut2 = self.compute_flap(xx_suc,yy_suc,xx_pre,yy_pre,flap_data)
                #print(flap_cut1[1])
                xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre = self.deploy_flap(flap_cut1[0], flap_cut1[1], xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre, flap_setting)
        else:
            xx_no_fl_suc = xx_suc
            yy_no_fl_suc = yy_suc
            xx_no_fl_pre = xx_pre
            yy_no_fl_pre = yy_pre
            xx_fl_pre = []
            xx_fl_suc = []
            yy_fl_pre = []
            yy_fl_suc = []
            flap_cut1 = []
            flap_cut2 = []


        # Output airfoiil data
        self.output_airfoil(xx_no_fl_pre,xx_no_fl_suc,yy_no_fl_pre,yy_no_fl_suc,[],[],xte,xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre, flap_cut1, flap_cut2)


        return

    def deploy_simple_flap(self,xx_pre,xx_suc,yy_pre,yy_suc,flap_set,flap_index):
        ''' Deploys a simple trailing edge flap or a droop nose based on a given chord ratio and deflection

            Inputs:
                xx_suc    - airfoil suction side x-coordinates
                yy_suc    - airfoil suction side y-coordinates
                xx_pre    - airfoil pressure side x-coordinates
                yy_pre    - airfoil pressure side y-coordinates
                droop_nose_set.delta_s - droop nose deflection [deg]
                            cs_c    - droop nose chord ratio
                            d_cs    - offset from the hinge

            Outputs:
                xx_suc_dr - airfoil suction side x-coordinates
                yy_suc_dr - airfoil suction side y-coordinates
                xx_pre_dr - airfoil pressure side x-coordinates
                yy_pre_dr - airfoil pressure side y-coordinates            


            Assumptions:

            
        '''

        # Unpack inputs
        delta_s         = flap_set[0]
        cs_c            = flap_set[1]
        d_cs_up         = flap_set[2]
        d_cs_low        = flap_set[3]
        w_conic_seal    = flap_set[4]


        # Split the airfoil 
        xx_suc_aft = []
        yy_suc_aft = []
        xx_pre_aft = []
        yy_pre_aft = []
        xx_suc_for = []
        yy_suc_for = []
        xx_pre_for = []
        yy_pre_for = []
        xx_suc_ds  = []
        yy_suc_ds  = []
        xx_pre_ds  = []
        yy_pre_ds  = []

        for i in range(len(xx_suc)):
            if xx_suc[i] >= cs_c:
                xx_suc_aft.append(xx_suc[i])
                yy_suc_aft.append(yy_suc[i])
            elif xx_suc[i] <= (cs_c-d_cs_up):
                xx_suc_for.append(xx_suc[i])
                yy_suc_for.append(yy_suc[i])
        for i in range(len(xx_pre)):
            if xx_pre[i] >= (cs_c+d_cs_low/2):            # Problem with botom side gap
                xx_pre_aft.append(xx_pre[i])
                yy_pre_aft.append(yy_pre[i])
            elif xx_pre[i] <= (cs_c-d_cs_low/2):
                xx_pre_for.append(xx_pre[i])
                yy_pre_for.append(yy_pre[i])                  

        # Rotate the flap

        if flap_index == 'flap':
            len_xx1 = len(xx_suc_aft)
            len_xx2 = len(xx_pre_aft)
            for i in range(len_xx1):
                xx_suc_ds.append((xx_suc_aft[i]-cs_c)*np.cos(np.radians(-delta_s))-(yy_suc_aft[i])*np.sin(np.radians(-delta_s))+cs_c)
                yy_suc_ds.append((xx_suc_aft[i]-cs_c)*np.sin(np.radians(-delta_s))+(yy_suc_aft[i])*np.cos(np.radians(-delta_s))) 
            for i in range(len_xx2):        
                xx_pre_ds.append((xx_pre_aft[i]-cs_c)*np.cos(np.radians(-delta_s))-(yy_pre_aft[i])*np.sin(np.radians(-delta_s))+cs_c) 
                yy_pre_ds.append((xx_pre_aft[i]-cs_c)*np.sin(np.radians(-delta_s))+(yy_pre_aft[i])*np.cos(np.radians(-delta_s)))  

            # Create points for the upper and lower surface fillers
            points_suc = allocate_line_points_Bezier(xx_suc_ds,yy_suc_ds,xx_suc_for,yy_suc_for,flap_index)
            points_pre = allocate_line_points_Bezier(xx_pre_ds[::-1],yy_pre_ds[::-1],xx_pre_for[::-1],yy_pre_for[::-1],flap_index)

        else:
            len_xx1 = len(xx_suc_for)
            len_xx2 = len(xx_pre_for)
            for i in range(len_xx1):
                xx_suc_ds.append((xx_suc_for[i]-cs_c)*np.cos(np.radians(delta_s))-(yy_suc_for[i])*np.sin(np.radians(delta_s))+cs_c)
                yy_suc_ds.append((xx_suc_for[i]-cs_c)*np.sin(np.radians(delta_s))+(yy_suc_for[i])*np.cos(np.radians(delta_s))) 
            for i in range(len_xx2):        
                xx_pre_ds.append((xx_pre_for[i]-cs_c)*np.cos(np.radians(delta_s))-(yy_pre_for[i])*np.sin(np.radians(delta_s))+cs_c) 
                yy_pre_ds.append((xx_pre_for[i]-cs_c)*np.sin(np.radians(delta_s))+(yy_pre_for[i])*np.cos(np.radians(delta_s)))         

            # Create points for the upper and lower surface fillers         
            points_suc = allocate_line_points_Bezier(xx_suc_ds,yy_suc_ds,xx_suc_aft,yy_suc_aft,flap_index)
            points_pre = allocate_line_points_Bezier(xx_pre_ds[::-1],yy_pre_ds[::-1],xx_pre_aft[::-1],yy_pre_aft[::-1],flap_index)


        # Create a filler of the upper surface
        point2, k, b = compute_line_intersection(points_suc[0,:],points_suc[1,:],points_suc[2,:],points_suc[3,:])

        fill_curve_up  = RationalizedQuadBezier(p0x=points_suc[0,0], p0y=points_suc[0,1], p1x=point2[0], \
                                                p1y=point2[1], p2x=points_suc[2,0], p2y=points_suc[2,1])
        fill_points_up = fill_curve_up.calc_curve([1,w_conic_seal,1],10)


        # Create a filler of the lower surface
        point2, k, b = compute_line_intersection(points_pre[0,:],points_pre[1,:],points_pre[2,:],points_pre[3,:])

        '''print([
                    [points_pre[0,0], points_pre[0,0]+k_Bez[0]*(points_pre[2,0]-points_pre[0,0]), \
                     points_pre[0,0]+k_Bez[1]*(points_pre[0,0]-points_pre[0,0]), points_pre[0,0]],
                    [points_pre[0,1], k[0]*(points_pre[0,0]+k_Bez[0]*(points_pre[0,0]-points_pre[0,0]))+b[0],\
                     k[1]*(points_pre[0,0]+k_Bez[1]*(points_pre[0,0]-points_pre[0,0]))+b[1], points_pre[0,1]],
                    ])'''

        '''nodes = np.asfortranarray([
                    [points_pre[0,0], points_pre[0,0]+k_Bez[0]*(points_pre[2,0]-points_pre[0,0]), \
                     points_pre[0,0]+k_Bez[1]*(points_pre[0,0]-points_pre[0,0]), points_pre[0,0]],
                    [points_pre[0,1], k[0]*(points_pre[0,0]+k_Bez[0]*(points_pre[0,0]-points_pre[0,0]))+b[0],\
                     k[1]*(points_pre[0,0]+k_Bez[1]*(points_pre[0,0]-points_pre[0,0]))+b[1], points_pre[0,1]],
                    ])
        
        curve = bezier.Curve(nodes, degree=3)
        points = np.linspace(0, 1.0, num=30)
        fill_points_low1 = np.zeros((2,30))
        for i in range(len(points)):
            curve_point = curve.evaluate(points[i])
            fill_points_low1[0,i] = curve_point[0]
            fill_points_low1[1,i] = curve_point[1]'''

        fill_curve_low  = RationalizedQuadBezier(p0x=points_pre[0,0], p0y=points_pre[0,1], p1x=point2[0], \
                                                p1y=point2[1], p2x=points_pre[2,0], p2y=points_pre[2,1])
        fill_points_low = fill_curve_low.calc_curve([1,w_conic_seal,1],10)

        #fill_points_low = fill_points_low1.tolist()

        if flap_index == 'flap':
            xx_suc_ds = xx_suc_for + fill_points_up[0][:] + xx_suc_ds 
            yy_suc_ds = yy_suc_for + fill_points_up[1][:] + yy_suc_ds 
            xx_pre_ds = xx_pre_ds + fill_points_low[0][::-1] + xx_pre_for  
            yy_pre_ds = yy_pre_ds + fill_points_low[1][::-1] + yy_pre_for  
        else:
            xx_suc_ds = xx_suc_ds + fill_points_up[0][:] + xx_suc_aft 
            yy_suc_ds = yy_suc_ds + fill_points_up[1][:] + yy_suc_aft 
            xx_pre_ds = xx_pre_aft + fill_points_low[0][::-1] + xx_pre_ds  
            yy_pre_ds = yy_pre_aft + fill_points_low[1][::-1] + yy_pre_ds  


        return xx_pre_ds,xx_suc_ds,yy_pre_ds,yy_suc_ds





    def deploy_flap(self,flap_cut1_x, flap_cut1_y, xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre, flap_setting):
        '''Deploys the flap according to the gap size and the deflection angle
        
            Inputs:
            flap_cut_x   - main airfoil cutout cordinates x
            flap_cut_y   - main airfoil cutout cordinates y
            xx_fl_suc    - flap airfoil suction side x-coordinates
            yy_fl_suc    - flap airfoil suction side y-coordinates
            xx_fl_pre    - flap airfoil pressure side x-coordinates
            yy_fl_pre    - flap airfoil pressure side y-coordinates
            flap_setting.delta_f - flap deflection [deg]
                            x_gap   - x-coordinate offset of the flap wrt the shroud lip
                            y_gap   - y-coordinate offset of the flap wrt the shroud lip 

            Outputs:
            xx_fl_suc_rot    - rotated x-coordinates of the flap suction side
            yy_fl_suc_rot    - rotated y-coordinates of the flap suction side
            xx_fl_pre_rot    - rotated x-coordinates of the flap pressure side
            yy_fl_pre_rot    - rotated y-coordinates of the flap pressure side



            Assumptions:

        '''

        # Unpack inputs
        df    = np.radians(flap_setting[0])
        x_gap = flap_setting[1]
        y_gap = flap_setting[2]


        # Rotate the flap around the leading edge
        XLE = np.min(xx_fl_suc)
        YLE = yy_fl_suc[np.argmin(xx_fl_suc)]
        XTE = np.max(flap_cut1_x)                                  # shroud lip TE x-coordinate
        YTE = flap_cut1_y[np.argmax(flap_cut1_x)]                 # shroud lip TE y-coordinate

        xx_fl_suc_norm = xx_fl_suc - XLE
        yy_fl_suc_norm = yy_fl_suc - YLE
        xx_fl_pre_norm = xx_fl_pre - XLE
        yy_fl_pre_norm = yy_fl_pre - YLE

        xx_fl_suc_rot = xx_fl_suc_norm * np.cos(df) + yy_fl_suc_norm * np.sin(df) + XTE - x_gap
        yy_fl_suc_rot = -xx_fl_suc_norm * np.sin(df) + yy_fl_suc_norm * np.cos(df) 
        xx_fl_pre_rot = xx_fl_pre_norm * np.cos(df) + yy_fl_pre_norm * np.sin(df) + XTE - x_gap

        # Why this strange calculation of the offset for the y gap?
        #y_gap_tot = y_gap + np.abs(np.max(yy_fl_suc_rot)) - np.abs(YLE)
        y_gap_tot = YTE - y_gap
        yy_fl_suc_rot =  yy_fl_suc_rot + y_gap_tot
        yy_fl_pre_rot = -xx_fl_pre_norm * np.sin(df) + yy_fl_pre_norm * np.cos(df) + y_gap_tot



        return xx_fl_suc_rot, yy_fl_suc_rot, xx_fl_pre_rot, yy_fl_pre_rot





    def compute_flap(self,xx_suc,yy_suc,xx_pre,yy_pre,flap_data):
        '''Draw a flap airfoil and cut the flap section of the main airfoil
        
            Inputs:
                xx_suc
                airfoil_data.cf_c        - flap chord ratio
                            ce_c        - conical curve extent wrt the flap chord length
                            csr_c       - shroud length chord ratio wrt the airfoil
                            clip_ext    - shroud lip extent ratio wrt the airfoil
                            r_le_flap   - flap leading edge radius 


            Outputs:
            xx_no_fl_suc - main airfoil suction side x-coordinates
            yy_no_fl_suc - main airfoil suction side y-coordinates
            xx_no_fl_pre - main airfoil pressure side x-coordinates
            yy_no_fl_pre - main airfoil pressure side y-coordinates
            xx_fl_suc    - flap airfoil suction side x-coordinates
            yy_fl_suc    - flap airfoil suction side y-coordinates
            xx_fl_pre    - flap airfoil pressure side x-coordinates
            yy_fl_pre    - flap airfoil pressure side y-coordinates

            Assumptions:
                1. shroud lip extent is small compared to the airfoil size

        '''

        # Unpack inputs
        cf_c        = flap_data[0]
        ce_c        = flap_data[1]
        csr_c       = flap_data[2]
        clip_ext    = flap_data[3]
        r_le_flap   = flap_data[4]
        tc_shr_tip  = flap_data[5]
        w_conic     = flap_data[6]
        xte         = flap_data[-2]
        yte_suc     = flap_data[-1]


        # Cut the airfoil upper surface using the shroud length
        xx_no_fl_suc = []
        yy_no_fl_suc = []
        xx_no_fl_pre = []
        yy_no_fl_pre = []
        for i in range(len(xx_suc)):
            if xx_suc[i] <= csr_c:
                xx_no_fl_suc.append(xx_suc[i])
                yy_no_fl_suc.append(yy_suc[i])
        xx_no_fl_suc.append(csr_c)
        yy_no_fl_suc.append(np.interp(csr_c,xx_suc,yy_suc))

        # Cut the airfoil lower surface using the flap chord ratio
        xx_no_fl_pre.append(1-cf_c)
        yy_no_fl_pre.append(-np.interp(1-cf_c,xx_pre[::-1],np.abs(yy_pre[::-1])))
        max_xx = 1
        for i in range(len(xx_pre)):
            if xx_pre[i] < 1 and xx_pre[i] > (1-cf_c) and xx_pre[i] < max_xx:
                max_xx = xx_pre[i]
            if xx_pre[i] <= (1-cf_c):
                xx_no_fl_pre.append(xx_pre[i])
                yy_no_fl_pre.append(yy_pre[i])


        # Allocate critical points for Bezier curves
        #----------------------------------------------------------------------

        flap_cut1 = np.zeros((2,4))                        # Upper part of the flap cutout
        flap_cut2 = np.zeros((2,2))                        # Side part of the flap cutout

        # shroud lip point and extent
        X_shr_TE = xx_no_fl_suc[-1]
        Y_shr_TE = yy_no_fl_suc[-1] - tc_shr_tip 
        X_sh_ext =  X_shr_TE - clip_ext * cf_c
        Y_sh_ext = np.interp(X_sh_ext,xx_no_fl_suc,yy_no_fl_suc) - tc_shr_tip

        flap_cut1[:,0] = [X_shr_TE,Y_shr_TE]
        flap_cut1[:,1] = [X_sh_ext,Y_sh_ext]

        # conical curve extent point
        X_con_ext = 1 - cf_c + ce_c * cf_c
        Y_cin_ext = Y_sh_ext
        flap_cut1[:,2] = [X_con_ext,Y_cin_ext]

        # Finish the airfoil cutout
        flap_cut1[:,3] = [1-cf_c,Y_cin_ext] 
        flap_cut2[:,0] = [1-cf_c,Y_cin_ext]  
        flap_cut2[:,1] = [xx_no_fl_pre[0],yy_no_fl_pre[0]]

        # Calculate Bezier curves for the flap
        curve2 = QuadBezier(p0x=X_con_ext, p0y=Y_cin_ext, p1x=X_sh_ext, p1y=Y_sh_ext, p2x=xte, p2y=yte_suc)
        flap_points2 = curve2.calc_curve()

        # Define the circular radius using the rationalized Bezier spline
        X0      = xx_no_fl_pre[0]
        Y0      = yy_no_fl_pre[0] + r_le_flap
        X1      = xx_no_fl_pre[0]
        Y1      = yy_no_fl_pre[0]
        Ysl1    = -np.interp(max_xx,xx_pre[::-1],np.abs(yy_pre[::-1]))
        Ysl2    = -np.interp(max_xx+0.01,xx_pre[::-1],np.abs(yy_pre[::-1]))
        gama1   = np.arctan((Ysl2 -Ysl1)/(0.01))
        alpha1  = 0.5*(0.5*np.pi - gama1)
        a_ext   = r_le_flap/np.tan(alpha1)
        X2      = X1 + a_ext*np.cos(gama1)
        Y2      = Y1 + a_ext*np.sin(gama1)  

        curve3 = RationalizedQuadBezier(p0x=X0, p0y=Y0, p1x=X1, p1y=Y1, p2x=X2, p2y=Y2)
        flap_points3 = curve3.calc_curve([1,1,1]) 

        # Define the conical curve
        curve1 = RationalizedQuadBezier(p0x=X0, p0y=Y0, p1x=1-cf_c, p1y=Y_cin_ext, p2x=X_con_ext, p2y=Y_cin_ext)     
        flap_points1 = curve1.calc_curve([1,w_conic,1]) 

        # Draw the pressure side of the flap airfoil
        xx_fl_1 = []
        yy_fl_1 = []  
        for i in range(len(xx_pre)):
            if xx_pre[i] > X2:
                xx_fl_1.append(xx_pre[i])
                yy_fl_1.append(yy_pre[i])
        xx_fl_1.append(X2)
        yy_fl_1.append(Y2)
        flap_points4 = [xx_fl_1, yy_fl_1]

        # Merge surfaces into suction and pressure sides of the flap
        xx_fl_suc = flap_points1[0][:]+flap_points2[0][:]
        yy_fl_suc = flap_points1[1][:]+flap_points2[1][:]
        xx_fl_pre = flap_points4[0][:]+flap_points3[0][::-1]
        yy_fl_pre = flap_points4[1][:]+flap_points3[1][::-1]


        return xx_no_fl_suc, yy_no_fl_suc, xx_no_fl_pre, yy_no_fl_pre, xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre, flap_cut1, flap_cut2



    def compute_airfoil(self,airfoil_data):

        '''Draw an airfoil based on input PARSEC coefficients, draw a flap, and export coordinates into data files
        
            Inputs:
                airfoil_data.rle         - leading edge radius
                            x_pre       - crest x-coordinate for the pressure side
                            y_pre       - crest y-coordinate for the pressure side
                            x_suc       - crest x-coordinate for the suction side
                            y_suc       - crest y-coordinate for the suction side
                            d2ydx2_pre  - curvature at crest for the pressure side
                            d2ydx2_suc  - curvature at crest for the suction side
                            th_pre      - trailing edge angle for the pressure side 
                            th_suc      - trailing edge angle for the suction side 
                            cf_c        - flap chord ratio
                            ce_c        - conical curve extent wrt the flap chord length
                            csr_c       - shroud length chord ratio wrt the airfoil
                            clip_ext    - shroud lip extent ratio wrt the airfoil
                            r_le_flap   - flap leading edge radius 


            Outputs:
                cf_suc - PARSEC cofficients for the suction side
                cf_pre - PARSEC cofficients for the pressure side
                xx_pre - pressure side x-coordinates
                xx_suc - suction side x-coordinates
                yy_pre - pressure side y-coordinates
                yy_suc - suction side y-coordinates

            Assumptions:

        '''

        rle         = airfoil_data[0]
        x_pre       = airfoil_data[1]
        y_pre       = airfoil_data[2]
        d2ydx2_pre  = airfoil_data[3]
        th_pre      = airfoil_data[4]
        x_suc       = airfoil_data[5]
        y_suc       = airfoil_data[6]
        d2ydx2_suc  = airfoil_data[7]
        th_suc      = airfoil_data[8]
        xle         = airfoil_data[-5]
        yle         = airfoil_data[-4]
        xte         = airfoil_data[-3]
        yte_suc     = airfoil_data[-2]
        yte_pre     = airfoil_data[-1]


        # Evaluate pressure (lower) surface coefficients
        cf_pre = pc_func.pcoef(xte,yte_pre,rle,x_pre,y_pre,d2ydx2_pre,th_pre,'pre')

        # Evaluate suction (upper) surface coefficients
        cf_suc = pc_func.pcoef(xte,yte_suc,rle,x_suc,y_suc,d2ydx2_suc,th_suc,'suc')


        # Evaluate pressure (lower) surface points
        xx_pre = 1 - (1 - np.cos(np.linspace(0, 1, int(np.ceil(201/2)))*np.pi)) / 2              #np.linspace(xte,xle,101)
        yy_pre = (cf_pre[0]*xx_pre**(1/2) + cf_pre[1]*xx_pre**(3/2) + cf_pre[2]*xx_pre**(5/2) + 
                cf_pre[3]*xx_pre**(7/2) + cf_pre[4]*xx_pre**(9/2) + cf_pre[5]*xx_pre**(11/2)) 

        # Evaluate suction (upper) surface points
        xx_suc = (1 - np.cos(np.linspace(0, 1, int(np.ceil(201/2)))*np.pi)) / 2 #np.linspace(xle,xte,101)
        yy_suc = (cf_suc[0]*xx_suc**(1/2) + cf_suc[1]*xx_suc**(3/2) + cf_suc[2]*xx_suc**(5/2) + 
                cf_suc[3]*xx_suc**(7/2) + cf_suc[4]*xx_suc**(9/2) + cf_suc[5]*xx_suc**(11/2))      



        return cf_pre, cf_suc, xx_pre, xx_suc, yy_pre, yy_suc 







    def output_airfoil(self,xx_pre,xx_suc,yy_pre,yy_suc,cf_pre,cf_suc,xte,xx_fl_suc,yy_fl_suc,xx_fl_pre,yy_fl_pre, flap_cut1, flap_cut2):

        '''Outputs an airfoil in data and image formats
        
            Inputs:
                xx_pre  - crest x-coordinate for the pressure side
                xx_suc  - crest x-coordinate for the suction side
                yy_pre  - crest y-coordinate for the pressure side
                yy_suc  - crest y-coordinate for the suction side
                cf_pre  - PARSEC coefficients for the pressure side
                cf_suc  - PARSEC coefficients for the suction side
                xte     - trailing edge x-location


            Outputs:
            

            Assumptions:

        '''


        # Use parsecexport to save coordinate file of the original airfoil
        airfoil_num = random.randint(1, 100)
        fpath       = 'main_airfoil_merged_' + str(airfoil_num) + '.dat'
        self.Airfoil.files['merged'] = fpath

        if len(cf_pre) > 0:
            with open(fpath, 'w') as f:
                f.write("Airfoil " + str(airfoil_num) + '\n')
                plain_coords = pc_func.ppointsplain(cf_pre, cf_suc, 121, xte=xte)
                f.write(plain_coords)

        # Plot each part of the airfoil for Pointwise meshing
        fpath = [self.Airfoil.files["upper"],self.Airfoil.files["lower"]]
        pc_func.ppoint_Pointwise(fpath[0], xx_suc, yy_suc)
        pc_func.ppoint_Pointwise(fpath[1], xx_pre, yy_pre)  
        if len(self.TrailingEdgeDevice.PARSEC) != 0: 
            if self.TrailingEdgeDevice.type == 'Slotted':
                TE_device = self.TrailingEdgeDevice
                fpath1 = [TE_device.files["flap cutout"][0],TE_device.files["flap cutout"][1],
                        TE_device.files["upper surface file"],TE_device.files["lower surface file"]]
                pc_func.ppoint_Pointwise(fpath1[0], flap_cut1[0,:], flap_cut1[1,:]) 
                pc_func.ppoint_Pointwise(fpath1[1], flap_cut2[0,:], flap_cut2[1,:]) 
                pc_func.ppoint_Pointwise(fpath1[2], xx_fl_suc, yy_fl_suc) 
                pc_func.ppoint_Pointwise(fpath1[3], xx_fl_pre, yy_fl_pre)             

        # Draw airfoil contour with the flap, if it was defined
        plotwidth=6.3
        plothight=plotwidth*0.4
        plt.figure(figsize=(plotwidth,plothight))
        plt.plot(xx_suc,yy_suc,'r',xx_pre,yy_pre,'b', linewidth=2)
        if len(self.TrailingEdgeDevice.PARSEC) != 0:
            if self.TrailingEdgeDevice.type == 'Slotted':
                plt.plot(flap_cut1[0,:],flap_cut1[1,:])
                plt.plot(flap_cut2[0,:],flap_cut2[1,:])
                plt.plot(xx_fl_suc,yy_fl_suc,'g')
                plt.plot(xx_fl_pre,yy_fl_pre,'k')

        plt.grid(True)
        plt.xlim([0,1])
        #plt.yticks([])
        plt.xticks(np.arange(0,1.4,0.1))
        plt.gca().axis('equal')
        plt.title("Generated high lift geometry")

        # Make room for title automatically
        #plt.tight_layout()
        # plt.ylim(bottom=0.0, top=0.025)
        # plt.xlim(left=-0.1, right=1.1)
        plt.savefig(os.path.join('parsec_airfoil.pdf'))
        plt.savefig(os.path.join('parsec_airfoil.png'),bbox_inches = 'tight')

        # Show the plot
        if self.plot_airfoil is True:
            plt.show()


        return
    

    def append_device(self,device):
        """ Adds a device to the segment

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
        # assert database type
        if not isinstance(device,Data):
            raise Exception('input component must be of type Data()')

        # store data
        self.Segment.append(device)


    class TrailingEdgeDevice():

        def __init__(self):
        
            self.type   = 'Plain'
            self.files  = {}
            self.PARSEC = {}
    


    class LeadingEdgeDevice():

        def __init__(self):
        
            self.type   = 'Droop'
            self.files  = {}
            self.PARSEC = {}