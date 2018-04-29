import numpy as np
import sys
from munkres import Munkres, make_cost_matrix, print_matrix

def allocate_d2d(lambda_matrix,maximum_rb_allowed):
    #if multiple resource blocks are allowed for d2d users then repeat the rows
    if(not(maximum_rb_allowed==1)):
        lambda_matrix_new = []
        for i in range(0,len(lambda_matrix)):
            for j in range(0,maximum_rb_allowed):
                lambda_matrix_new.append(lambda_matrix[i])
        print_matrix(lambda_matrix_new, msg='modified matrix:')
        lambda_matrix = lambda_matrix_new

    #convert profit matrix to cost matrix
    cost_matrix = make_cost_matrix(lambda_matrix, lambda cost: sys.maxsize - cost)

    m = Munkres()
    indexes = m.compute(cost_matrix) #indexes contains the 2d indexes of the maximum weight allocations

    allocated_d2d_in_channels = np.zeros(len(lambda_matrix[0]))-1

    d2d_and_indexes = [] #indexes to return

    for row, column in indexes:
        allocated_d2d_in_channels[column] = int(row/maximum_rb_allowed)

    allocated_d2d_in_channels = allocated_d2d_in_channels.astype(int)

    for i in range(0,len(allocated_d2d_in_channels)):
        if(not(allocated_d2d_in_channels[i]==-1)):
            d2d_and_indexes.append([allocated_d2d_in_channels[i],[allocated_d2d_in_channels[i],i]])

    return d2d_and_indexes
