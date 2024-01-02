# Bezier_curves_airfoil.py
# 
# Created:  Dec 2022, S. Karpuk
# Modified:

"""
Functions to create Bezier curves 
"""

import random
import matplotlib.pyplot as plt
import math
import random


class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def random(self, min= 0, max= 1):
        self.x = random.uniform(min,max)
        self.y = random.uniform(min,max)


#
#=============Quadratic Bezier curve====================
#
class QuadBezier(object):
    def __init__(self, p0x= 0, p0y= 0, p1x= 0, p1y= 0, p2x= 0, p2y= 0):
        self.p0 = Point(p0x, p0y)
        self.p1 = Point(p1x, p1y)
        self.p2 = Point(p2x, p2y)
        self.obstacles = []

    def random(self,min= 0, max= 1):
        'Create a random quadratic Bezier curve within [min, max] limits. Default [0,1].'
        self.p0.random(min, max)
        self.p1.random(min, max)
        self.p2.random(min, max)

    def max_k(self, granuality=100):
        'Calculate maximal curvature of the quadratic Bezier curve.'
        k = 0
        for t in range(0, granuality):
            t = t / granuality
            x_d = 2 * (t - 1)*(self.p1.x - self.p0.x) + 2 * t * (self.p2.x - self.p1.x)
            y_d = 2 * (t - 1)*(self.p1.y - self.p0.y) + 2 * t * (self.p2.y - self.p1.y)
            x_dd = 2 * (self.p2.x - 2 * self.p1.x + self.p0.x)
            y_dd = 2 * (self.p2.y - 2 * self.p1.y + self.p0.y)
            k = max(k,abs(x_d*y_dd - y_d*x_dd)/math.pow(x_d**2 + y_d**2, 3/2))
        return k

    def calc_curve(self, granuality=100):
        'Calculate the quadratic Bezier curve with the given granuality.'
        B_x = []
        B_y = []
        for t in range(0, granuality+1):
            t = t / granuality
            x = self.p1.x + (1 - t)**2 * (self.p0.x-self.p1.x) + t**2 * (self.p2.x - self.p1.x)
            y = self.p1.y + (1 - t)**2 * (self.p0.y-self.p1.y) + t**2 * (self.p2.y - self.p1.y)
            B_x.append(x)
            B_y.append(y)
        return [B_x, B_y]

    def plot(self, granuality=100):
        'Plot the quadratic Bezier curve.'
        B = self.calc_curve(granuality)
        plt.plot(B[0], B[1])
        plt.scatter([self.p0.x,self.p1.x,self.p2.x], [self.p0.y,self.p1.y,self.p2.y])
        for i in range(len(self.obstacles)):
            plt.gcf().gca().add_artist(plt.Circle((self.obstacles[i][0].x, self.obstacles[i][0].y), self.obstacles[i][1], color='r'))
        plt.axis('equal')
        plt.show()

    def arc_len(self, granuality=1000):
        'Calculate the arc-length of the quadratic Bezier curve.'
        B = self.calc_curve(granuality=granuality)
        a_l = 0
        for i in range(1,len(B[0])):
            a_l += math.sqrt((B[0][i]-B[0][i-1])**2 + (B[1][i]-B[1][i-1])**2)
        return a_l



    def clear(self):
        'Re-initialize the curve.'
        self.__init__()


#
#=============Rationalized Quadratic Bezier curve====================
#
class RationalizedQuadBezier(object):
    def __init__(self, p0x= 0, p0y= 0, p1x= 0, p1y= 0, p2x= 0, p2y= 0):
        self.p0 = Point(p0x, p0y)
        self.p1 = Point(p1x, p1y)
        self.p2 = Point(p2x, p2y)
        self.obstacles = []



    def calc_curve(self, w, granuality=30):
        'Calculate the rationalized quadratic Bezier curve with the given granuality.'
        B_x = []
        B_y = []
        for t in range(0, granuality+1):
            t = t / granuality

            B20 = (1-t)**2
            B21 = 2*t*(1-t)
            B22 = t**2

            denumR = w[0]*B20+w[1]*B21+w[2]*B22
            R20    = w[0]*B20/denumR
            R21    = w[1]*B21/denumR
            R22    = w[2]*B22/denumR

            x = self.p0.x * R20 + self.p1.x * R21 + self.p2.x * R22
            y = self.p0.y * R20 + self.p1.y * R21 + self.p2.y * R22

            B_x.append(x)
            B_y.append(y)

        return [B_x, B_y]


    def plot(self, w, granuality=100):
        'Plot the quadratic Bezier curve.'
        B = self.calc_curve(w,granuality)
        plt.plot(B[0], B[1])
        plt.scatter([self.p0.x,self.p1.x,self.p2.x], [self.p0.y,self.p1.y,self.p2.y])
        for i in range(len(self.obstacles)):
            plt.gcf().gca().add_artist(plt.Circle((self.obstacles[i][0].x, self.obstacles[i][0].y), self.obstacles[i][1], color='r'))
        plt.axis('equal')
        plt.show()



        
    def clear(self):
        'Re-initialize the curve.'
        self.__init__()