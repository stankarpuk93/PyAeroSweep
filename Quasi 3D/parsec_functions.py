# parsec_functions.py
# 
# Created:  Dec 2022, S. Karpuk
# Modified:

"""
Creates an airfoil based on the PARSEC method and exports it in plain coordinate format.
"""

# ----------------------------------------------------------------------
#   Imports
# ----------------------------------------------------------------------
from __future__ import division
from math import sqrt, tan, pi
import numpy as np



def ppointsplain(*args, **kwargs):
    
    ''' Alias for ppoints that returns a string with plain data format
    
        Inputs:


        Outputs:
            list of coordinates

        Assumptions:
    '''

    coords = ppoints(*args, **kwargs)

    # Iterate over coordinates, making a list of strings
    coordstrlist = ["{:.6f} {:.6f}".format(coord[0], coord[1])
                    for coord in coords]

    # Now join these strings with linebreaks in between
    return '\n'.join(coordstrlist)


def ppoint_Pointwise(fpath, xx, yy):
    
    ''' writes an airfoil file with the Pointwise format
    
        Inputs:


        Outputs:
            list of coordinates

        Assumptions:
    '''

    with open(fpath, 'w') as f:
        f.write(str(len(xx))+ '\n')
        for i in range(len(xx)):
            x_str   =   str('%8.5f'   % xx[i])     + '\t'
            y_str   =   str('%8.5f'   % yy[i])     + '\t'
            z_str   =   str('%8.5f'   % 0.0)     + '\n'
            f.write(x_str + y_str + z_str)

    f.close()

    # Join these strings with linebreaks in between
    return 


def ppoints(cf_pre, cf_suc, npts=121, xte=1.0):

    ''' Takes PARSEC coefficients, number of points, and returns list of
        [x,y] coordinates starting at trailing edge pressure side.
        Assumes trailing edge x position is 1.0 if not specified.
        Returns 121 points if 'npts' keyword argument not specified.
    
        Inputs:
            cf_pre - PARSEC coefficients for the pressure side
            cf_suc - PARSEC coefficients for the suction side

        Outputs:
            arrays of X- and Y-coordinates

        Assumptions:

    '''

    # Using cosine spacing to concentrate points near TE and LE,
    # see http://airfoiltools.com/airfoil/naca4digit
    xpts = (1 - np.cos(np.linspace(0, 1, int(np.ceil(npts/2)))*np.pi)) / 2

    # Take TE x-position into account
    xpts *= xte

    # Powers to raise coefficients to
    pwrs = (1/2, 3/2, 5/2, 7/2, 9/2, 11/2)

    # Make [[1,1,1,1],[2,2,2,2],...] style array
    xptsgrid = np.meshgrid(np.arange(len(pwrs)), xpts)[1]

    # Evaluate points with concise matrix calculations. One x-coordinate is
    # evaluated for every row in xptsgrid
    evalpts = lambda cf: np.sum(cf*xptsgrid**pwrs, axis=1)

    # Move into proper order: start at TE, over bottom, then top
    # Avoid leading edge pt (0,0) being included twice by slicing [1:]
    ycoords = np.append(evalpts(cf_pre)[::-1], evalpts(cf_suc)[1:])
    xcoords = np.append(xpts[::-1], xpts[1:])

    # Return 2D list of coordinates [[x,y],[x,y],...] by transposing .T
    return np.array((xcoords, ycoords)).T


def pcoef(xte,yte,rle,x_cre,y_cre,d2ydx2_cre,th_cre,surface):

    '''Evaluate the PARSEC coefficients
    
        Inputs:
            xte         - trailing edge x-coordinate
            yte         - trailing edge y-coordinate
            rle         - leading edge radius
            x_cre       - crest x-coordinate
            y_cre       - crest y-coordinate
            d2ydx2_cre  - curvature at crest
            th_cre      - trailing edge angle
            surface     - upper or lower surface flag 

        Outputs:
            coef - coefficients of the PARSEC airfoil

        Assumptions:

    '''


    # Initialize coefficients
    coef = np.zeros(6)


    # 1st coefficient depends on surface (pressure or suction)
    if surface.startswith('p'):
        coef[0] = -sqrt(2*rle)
    else:
        coef[0] = sqrt(2*rle)
 
    # Form system of equations
    A = np.array([
                 [xte**1.5, xte**2.5, xte**3.5, xte**4.5, xte**5.5],
                 [x_cre**1.5, x_cre**2.5, x_cre**3.5, x_cre**4.5,x_cre**5.5],
                 [1.5*sqrt(xte), 2.5*xte**1.5, 3.5*xte**2.5,4.5*xte**3.5, 5.5*xte**4.5],
                 [1.5*sqrt(x_cre), 2.5*x_cre**1.5, 3.5*x_cre**2.5,4.5*x_cre**3.5, 5.5*x_cre**4.5],
                 [0.75*(1/sqrt(x_cre)), 3.75*sqrt(x_cre), 8.75*x_cre**1.5,15.75*x_cre**2.5, 24.75*x_cre**3.5]
                 ]) 

    B = np.array([
                 [yte - coef[0]*sqrt(xte)],
                 [y_cre - coef[0]*sqrt(x_cre)],
                 [tan(th_cre*pi/180) - 0.5*coef[0]*(1/sqrt(xte))],
                 [-0.5*coef[0]*(1/sqrt(x_cre))],
                 [d2ydx2_cre + 0.25*coef[0]*x_cre**(-1.5)]
                 ])
    

    # Solve system of linear equations
    X = np.linalg.solve(A,B) 


    # Gather all coefficients
    coef[1:6] = X[0:5,0]


    # Return coefficients
    return coef



def _example():
    '''Runs some examples. Underscore means it's a local function
    
        Inputs:

        Outputs:

        Assumptions:

    '''

    # Sample coefficients
    rle = .011
    x_pre = .3
    y_pre = -0.04
    d2ydx2_pre = .2
    th_pre = 2
    x_suc = .4
    y_suc = .056
    d2ydx2_suc = -.35
    th_suc = -10

    # Trailing edge x and y position
    xte = 1.0
    yte = -0.00

    # Evaluate pressure (lower) surface coefficients
    cf_pre = pcoef(xte, yte, rle,x_pre, y_pre, d2ydx2_pre, th_pre,'pre')

    # Evaluate suction (upper) surface coefficients
    cf_suc = pcoef(xte, yte, rle,x_suc, y_suc, d2ydx2_suc, th_suc,'suc')

    # Get and print plain list of coordinates
    print(ppointsplain(cf_pre, cf_suc, 121, xte=xte))

    # Get list of coordinates
    pts = ppoints(cf_pre, cf_suc, 121, xte=xte)

    # Plot this airfoil, transposing pts to get list of x's and list of y's
    import matplotlib.pyplot as plt
    plt.plot(pts.T[0], pts.T[1], 'o--')
    plt.gca().axis('equal')
    plt.show()


# If this file is run, execute example
if __name__ == "__main__":
    _example()
