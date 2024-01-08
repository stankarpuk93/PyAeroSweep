# miscellaneous_geometry.py
# 
# Created:  Dec 2023, S. Karpuk
# Modified:


"""
    Miscellaneous functions for geometric pre-processing activities
"""

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
import numpy as np


def compute_line_intersection(point1,point11,point3,point31):   

    ''' Computes an intersection between two line
    
        Inputs:
            point1, point11 - points on the first line
            point3, point31 - points on the second line

        Outputs:
            point2 - intersection point


        Assumptions:

    '''

    k      = [(point1[1]-point11[1])/(point1[0]-point11[0]), (point31[1]-point3[1])/(point31[0]-point3[0])]
    b      = [point11[1]-k[0]*point11[0], point31[1]-k[1]*point31[0]]
    point2 = [(b[1]-b[0])/(k[0]-k[1]),  k[0]*(b[1]-b[0])/(k[0]-k[1])+b[0]]


    return point2, k, b


def allocate_line_points_Bezier(xx_ds,yy_ds,xx,yy,flap_flag):
    
    ''' allocates points on two lines that create a corner for a Bezier curve
    
        Inputs:
            xx_ds, yy_ds - x- and y-coordinates of a leading- or trailing-edge device
            xx, yy       - airfoil x- and y-coordinates
            flap_flag    - flag for a leading- or trailing edge device

        Outputs:
            points - array of sorted airfoil coordinates


        Assumptions:

    '''

    points = np.zeros((4,2))
    if flap_flag == 'flap':
        points[2,:] = [np.min(xx_ds), yy_ds[np.argmin(xx_ds)]] 
        points[3,:] = [xx_ds[np.argmin(xx_ds)+1], yy_ds[np.argmin(xx_ds)+1]]
        points[0,:] = [np.max(xx), yy[np.argmax(xx)]] 
        points[1,:] = [xx[np.argmax(xx)-1], yy[np.argmax(xx)-1]]        
    else:
        points[0,:] = [np.max(xx_ds), yy_ds[np.argmax(xx_ds)]] 
        points[1,:] = [xx_ds[np.argmax(xx_ds)-1], yy_ds[np.argmax(xx_ds)-1]]
        points[2,:] = [np.min(xx), yy[np.argmin(xx)]] 
        points[3,:] = [xx[np.argmin(xx)+1], yy[np.argmin(xx)+1]]

    return points

