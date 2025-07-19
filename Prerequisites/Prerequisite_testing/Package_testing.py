import numpy
import scipy
import matplotlib
import pyiges
import pygeo
import xlsxwriter
import pandas
import cython
from mpi4py import MPI



# This code tests the import of all necessary libraries and executes 
# a sample code which tests paraller computations

# To run the code, execute from the terminal in the Prerequisites directory
# mpiexec -n 4 python Package_testing.py

'''
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
print(f"Hello from rank {rank}")
'''