# create_airfoil_and_flap.py
# 
# Created:  Dec 2022, S. Karpuk
# Modified:

"""
Creates an airfoil based on the PARSEC method,
Generates a flap based on multiple Bezier curves,
and exports airfoils in plain coordinate format.
"""


# Import 
import os
import bezier
import numpy as np
import matplotlib.pyplot    as plt
import parsec_functions     as pc_func

from Bezier_curves_airfoil  import QuadBezier, RationalizedQuadBezier



def create_airfoil_and_flap(airfoil_data, flap_setting, flap_flag, droop_nose_flag, droop_nose_set):

    '''Draw an airfoil based on input PARSEC coefficients, draw a flap, and export coordinates into data files
    
        Inputs:
            airfoil_data.rle          Main airfoil LE radius
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

            flap_flag                flag to compute the flap airfoil
            droop_nose_flag          flag to compute the droop nose

        Outputs:
           

        Assumptions:
            1. airfoil tip thickness is assumed 0.0025 from each side

    '''

    # Define TE & LE of airfoil (normalized, chord = 1)
    xle     = 0.0
    yle     = 0.0
    xte     = 1.0
    yte_suc = 0.002
    yte_pre = -0.002
    w_conic_seal = airfoil_data[-1]
    airfoil_data.append(xle)
    airfoil_data.append(yle)
    airfoil_data.append(xte)
    airfoil_data.append(yte_suc)
    airfoil_data.append(yte_pre)


    # Calculate airfoil coordinates using the PARSEC method                                            
    cf_pre,cf_suc,xx_pre,xx_suc,yy_pre,yy_suc = compute_airfoil(airfoil_data)

    # Draw a droop nose
    if droop_nose_flag is True:
        xx_pre,xx_suc,yy_pre,yy_suc = deploy_droop_nose(xx_pre,xx_suc,yy_pre,yy_suc,droop_nose_set,w_conic_seal)


    # Draw a flap
    if flap_flag is True:   
        xx_no_fl_suc, yy_no_fl_suc, xx_no_fl_pre, yy_no_fl_pre, xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre, flap_cut1, flap_cut2 = compute_flap(xx_suc,yy_suc,xx_pre,yy_pre,airfoil_data)
        xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre = deploy_flap(xx_no_fl_suc, yy_no_fl_suc, xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre, flap_setting)
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
    output_airfoil(xx_no_fl_pre,xx_no_fl_suc,yy_no_fl_pre,yy_no_fl_suc,cf_pre,cf_suc,xte,xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre, flap_cut1, flap_cut2, flap_flag)
    #output_airfoil(xx_pre,xx_suc,yy_pre,yy_suc,cf_pre,cf_suc,xte)



    return

def deploy_droop_nose(xx_pre,xx_suc,yy_pre,yy_suc,droop_nose_set,w_conic_seal):
    ''' Deploys the droop nose based on a given chord ratio and deflection

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
    delta_s  = droop_nose_set[0]
    cs_c     = droop_nose_set[1]
    d_cs_up  = droop_nose_set[2]
    d_cs_low = droop_nose_set[3]
    k_Bez    = [droop_nose_set[4],droop_nose_set[5]]


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

    len_xx = len(xx_suc_for)
    for i in range(len(xx_suc)):
        if xx_suc[i] >= cs_c:
            xx_suc_aft.append(xx_suc[i])
            yy_suc_aft.append(yy_suc[i])
        elif xx_suc[i] <= (cs_c-d_cs_up):
            xx_suc_for.append(xx_suc[i])
            yy_suc_for.append(yy_suc[i])

        if xx_pre[i] >= cs_c:
            xx_pre_aft.append(xx_pre[i])
            yy_pre_aft.append(yy_pre[i])
        elif xx_pre[i] <= (cs_c-d_cs_low):
            xx_pre_for.append(xx_pre[i])
            yy_pre_for.append(yy_pre[i])                        

    # Rotate the droop nose
    len_xx1 = len(xx_suc_for)
    len_xx2 = len(xx_pre_for)
    for i in range(len_xx1):
        xx_suc_ds.append((xx_suc_for[i]-cs_c)*np.cos(np.radians(delta_s))-(yy_suc_for[i])*np.sin(np.radians(delta_s))+cs_c)
        yy_suc_ds.append((xx_suc_for[i]-cs_c)*np.sin(np.radians(delta_s))+(yy_suc_for[i])*np.cos(np.radians(delta_s))) 
    for i in range(len_xx2):        
        xx_pre_ds.append((xx_pre_for[i]-cs_c)*np.cos(np.radians(delta_s))-(yy_pre_for[i])*np.sin(np.radians(delta_s))+cs_c) 
        yy_pre_ds.append((xx_pre_for[i]-cs_c)*np.sin(np.radians(delta_s))+(yy_pre_for[i])*np.cos(np.radians(delta_s)))         


    ## Connect two parts into one airfoil 
    # lower surface
    '''xx_pre_ds1  = []
    yy_pre_ds1  = []
    xx_min_pre  = np.min(xx_pre_aft)
    for i in range(len(xx_pre_ds)):
        if xx_pre_ds[i] < xx_min_pre:
            xx_pre_ds1.append(xx_pre_ds[i])
            yy_pre_ds1.append(yy_pre_ds[i])
    xx_pre_ds = xx_pre_aft + xx_pre_ds1
    yy_pre_ds = yy_pre_aft + yy_pre_ds1'''

    # Create a filler of the upper surface
    point1  = [np.max(xx_suc_ds), yy_suc_ds[np.argmax(xx_suc_ds)]] 
    point11 = [xx_suc_ds[np.argmax(xx_suc_ds)-1], yy_suc_ds[np.argmax(xx_suc_ds)-1]]
    point3  = [np.min(xx_suc_aft), yy_suc_aft[np.argmin(xx_suc_aft)]] 
    point31 = [xx_suc_aft[np.argmin(xx_suc_aft)+1], yy_suc_aft[np.argmin(xx_suc_aft)+1]]

    k      = [(point1[1]-point11[1])/(point1[0]-point11[0]), (point31[1]-point3[1])/(point31[0]-point3[0])]
    b      = [point11[1]-k[0]*point11[0], point31[1]-k[1]*point31[0]]
    point2 = [(b[1]-b[0])/(k[0]-k[1]),  k[0]*(b[1]-b[0])/(k[0]-k[1])+b[0]]

    fill_curve_up  = RationalizedQuadBezier(p0x=point1[0], p0y=point1[1], p1x=point2[0], p1y=point2[1], p2x=point3[0], p2y=point3[1])
    fill_points_up = fill_curve_up.calc_curve([1,w_conic_seal,1],10)


    # Create a filler of the lower surface
    point1  = [np.max(xx_pre_ds), yy_pre_ds[np.argmax(xx_pre_ds)]] 
    point11 = [xx_pre_ds[np.argmax(xx_pre_ds)+1], yy_pre_ds[np.argmax(xx_pre_ds)+1]]
    point3  = [np.min(xx_pre_aft), yy_pre_aft[np.argmin(xx_pre_aft)]] 
    point31 = [xx_pre_aft[np.argmin(xx_pre_aft)-1], yy_pre_aft[np.argmin(xx_pre_aft)-1]]

    k      = [(point1[1]-point11[1])/(point1[0]-point11[0]), (point31[1]-point3[1])/(point31[0]-point3[0])]
    b      = [point11[1]-k[0]*point11[0], point31[1]-k[1]*point31[0]]
    point2 = [(b[1]-b[0])/(k[0]-k[1]),  k[0]*(b[1]-b[0])/(k[0]-k[1])+b[0]]


    nodes = np.asfortranarray([
                [point1[0], point1[0]+k_Bez[0]*(point3[0]-point1[0]), point1[0]+k_Bez[1]*(point3[0]-point1[0]), point3[0]],
                [point1[1], k[0]*(point1[0]+k_Bez[0]*(point3[0]-point1[0]))+b[0], k[1]*(point1[0]+k_Bez[1]*(point3[0]-point1[0]))+b[1], point3[1]],
                 ])
    curve = bezier.Curve(nodes, degree=3)
    points = np.linspace(0, 1.0, num=30)
    fill_points_low1 = np.zeros((2,30))
    for i in range(len(points)):
        curve_point = curve.evaluate(points[i])
        fill_points_low1[0,i] = curve_point[0]
        fill_points_low1[1,i] = curve_point[1]

    fill_points_low = fill_points_low1.tolist()

    #fill_curve_low  = RationalizedQuadBezier(p0x=point1[0], p0y=point1[1], p1x=point2[0], p1y=point2[1], p2x=point3[0], p2y=point3[1])
    #fill_points_low = fill_curve_low.calc_curve([1,w_conic_seal,1],10)


    xx_suc_ds = xx_suc_ds + fill_points_up[0][:] + xx_suc_aft 
    yy_suc_ds = yy_suc_ds + fill_points_up[1][:] + yy_suc_aft 
    xx_pre_ds = xx_pre_aft + fill_points_low[0][::-1] + xx_pre_ds  
    yy_pre_ds = yy_pre_aft + fill_points_low[1][::-1] + yy_pre_ds  


    return xx_pre_ds,xx_suc_ds,yy_pre_ds,yy_suc_ds





def deploy_flap(xx_no_fl_suc, yy_no_fl_suc, xx_fl_suc, yy_fl_suc, xx_fl_pre, yy_fl_pre, flap_setting):
    '''Deploys the flap according to the gap size and the deflection angle
    
        Inputs:
           xx_no_fl_suc - main airfoil suction side x-coordinates
           yy_no_fl_suc - main airfoil suction side y-coordinates
           xx_no_fl_pre - main airfoil pressure side x-coordinates
           yy_no_fl_pre - main airfoil pressure side y-coordinates
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
    XTE = np.max(xx_no_fl_suc)                                  # shroud lip TE x-coordinate
    YTE = yy_no_fl_suc[np.argmax(xx_no_fl_suc)]                 # shroud lip TE y-coordinate

    xx_fl_suc_norm = xx_fl_suc - XLE
    yy_fl_suc_norm = yy_fl_suc - YLE
    xx_fl_pre_norm = xx_fl_pre - XLE
    yy_fl_pre_norm = yy_fl_pre - YLE

    xx_fl_suc_rot = xx_fl_suc_norm * np.cos(df) + yy_fl_suc_norm * np.sin(df) + XTE - x_gap
    yy_fl_suc_rot = -xx_fl_suc_norm * np.sin(df) + yy_fl_suc_norm * np.cos(df) + YTE 
    xx_fl_pre_rot = xx_fl_pre_norm * np.cos(df) + yy_fl_pre_norm * np.sin(df) + XTE - x_gap
 
    y_gap_tot = y_gap + np.abs(np.max(yy_fl_suc_rot)) - np.abs(YLE)
    yy_fl_suc_rot -= y_gap_tot
    yy_fl_pre_rot = -xx_fl_pre_norm * np.sin(df) + yy_fl_pre_norm * np.cos(df) + YTE - y_gap_tot



    return xx_fl_suc_rot, yy_fl_suc_rot, xx_fl_pre_rot, yy_fl_pre_rot





def compute_flap(xx_suc,yy_suc,xx_pre,yy_pre,airfoil_data):
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
    cf_c        = airfoil_data[9]
    ce_c        = airfoil_data[10]
    csr_c       = airfoil_data[11]
    clip_ext    = airfoil_data[12]
    r_le_flap   = airfoil_data[13]
    tc_shr_tip  = airfoil_data[14]
    w_conic     = airfoil_data[15]
    xte         = airfoil_data[-3]
    yte_suc     = airfoil_data[-2]


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



def compute_airfoil(airfoil_data):

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







def output_airfoil(xx_pre,xx_suc,yy_pre,yy_suc,cf_pre,cf_suc,xte,xx_fl_suc,yy_fl_suc,xx_fl_pre,yy_fl_pre, flap_cut1, flap_cut2, flap_flag):

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
    fpath = 'parsec_airfoil.dat'
    with open(fpath, 'w') as f:
        plain_coords = pc_func.ppointsplain(cf_pre, cf_suc, 121, xte=xte)
        f.write(plain_coords)

    # Plot each part of the airfoil for Pointwise meshing
    fpath = ['main_airfoil_upper.dat','main_airfoil_lower.dat','main_airfoil_cut1.dat','main_airfoil_cut2.dat','flap_airfoil_upper.dat','flap_airfoil_lower.dat']
    pc_func.ppoint_Pointwise(fpath[0], xx_suc, yy_suc)
    pc_func.ppoint_Pointwise(fpath[1], xx_pre, yy_pre)  
    if flap_flag is True: 
        pc_func.ppoint_Pointwise(fpath[2], flap_cut1[0,:], flap_cut1[1,:]) 
        pc_func.ppoint_Pointwise(fpath[3], flap_cut2[0,:], flap_cut2[1,:]) 
        pc_func.ppoint_Pointwise(fpath[4], xx_fl_suc, yy_fl_suc) 
        pc_func.ppoint_Pointwise(fpath[5], xx_fl_pre, yy_fl_pre)             

    # Plot airfoil contour with the flap, if it was defined
    plt.figure()

    plt.plot(xx_suc,yy_suc,'r',xx_pre,yy_pre,'b', linewidth=2)
    if flap_flag is True:
        plt.plot(flap_cut1[0,:],flap_cut1[1,:])
        plt.plot(flap_cut2[0,:],flap_cut2[1,:])
        plt.plot(xx_fl_suc,yy_fl_suc,'g')
        plt.plot(xx_fl_pre,yy_fl_pre,'k')


    plt.grid(True)
    plt.xlim([0,1])
    #plt.yticks([])
    plt.xticks(np.arange(0,1.4,0.1))
    plt.gca().axis('equal')

    plt.title("PARSEC airfoil")
    # Make room for title automatically
    plt.tight_layout()

    plt.savefig(os.path.join('parsec_airfoil.pdf'))
    plt.savefig(os.path.join('parsec_airfoil.png'))

    # Show & save graphs
    plt.show()


    return





if __name__ == '__main__':

    # Analysis flags
    droop_nose_flag = True
    flap_flag       = True               # A flag to include or exclude a flap
                                            # True  - airfoil has a flap
                                            # False - draws a clean airfoil

    # Sample input
    rle         = .011              # Main airfoil LE radius
    x_pre       = .3                # x-location of the crest on the pressure side
    y_pre       = -0.04             # y-location of the crest on the pressure side
    d2ydx2_pre  = .2                # curvature of the crest on the pressure side
    th_pre      = 2                 # trailing edge angle on the pressure side [deg]
    x_suc       = .4                # x-location of the crest on the suction side        
    y_suc       = .056              # y-location of the crest on the suction side    
    d2ydx2_suc  = -.35              # curvature of the crest on the suction side
    th_suc      = -10               # trailing edge angle on the suction side [deg]

    cf_c        = 0.3               # flap chord ratio
    ce_c        = 0.3               # conical curve extent ratio wrt the flap chord length
    csr_c       = 0.9               # shroud chord ratio
    clip_ext    = 0.3               # shroud lip extent ratio wrt the flap 
    r_le_flap   = 0.01              # flap leading edge radius
    tc_shr_tip  = 0.003             # shroud tip thickness
    w_conic     = 0.5                 # conical parameter for the suction side of the flap airfoil

    delta_f     = 30                # flap deflection [deg]
    x_gap       = 0.02              # x-length gap from the shroud TE (positive value is moving the flap left)
    y_gap       = 0.02              # y-length gap from the shroud TE (positive value is moving the flap down)   

    delta_s     = 25                # droop nose deflection [deg]
    cs_c        = 0.2               # droop nose chord ratio
    d_cs        = 0.02              # droop nose offset from the hinge

    airfoil_data   = [rle, x_pre, y_pre, d2ydx2_pre, th_pre, x_suc, y_suc, d2ydx2_suc, th_suc, cf_c, ce_c, csr_c, clip_ext, r_le_flap, tc_shr_tip, w_conic]
    flap_setting   = [delta_f, x_gap, y_gap]
    droop_nose_set = [delta_s, cs_c, d_cs]

    create_airfoil_and_flap(airfoil_data, flap_setting, flap_flag, droop_nose_flag, droop_nose_set)