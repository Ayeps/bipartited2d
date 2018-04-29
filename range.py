import cellsys as cs
import numpy as np
import pylab as pl
import random
from channel import *
from bipartite import *

# channel gains are in one time slot

# running average

# fading is the reason for the MS having
# different channel gain in different RBs

# radius of hexagon
Rc = 500
ntiers = 0

# Tx power from CU
Pc = 0.25

# Bandwidth
BW = 180e3
bw = 160e3

#  Noise PSD in dBm
N_dBm =  -174
N0 = (10**(N_dBm / 10)) * 10**(-3)
N0 = N0 * bw

# Target SNR at BS from CU (dB)
tSNR_dB = 7.7
tSNR = 10**(tSNR_dB / 10)

# no. of cell users
Nc = 20

# no of D2D pairs
Nd = 20

# no. of resource blocks
nRB = 25

# Rb per D2D pair
rbPerD2DPair = 2

# max window
RWindowSize = 100

brush = cs.draw(0.1)
g = cs.geom(Rc)

# # # # # # # # # # # # # # # # # # # ## # # # # # # # # # # # # # # # # # # # #
# Take Cell users and D2D users in a cell

cellUsers = []
d2d_tx = []
d2d_rx = []

cellUsers = [g.getRandomPointInHex() for i in range(Nc)]

def valid(a):
    for i in range(0,len(a)):
        if(a[i] > 0.25):
            a[i] = 0.25
        elif(a[i] < 0):
            a[i] = 0
    return a

def initAllocate(msCh = [], preAv = []):
    assignment = [[] for x in range(Nc)]
    assignmentRB = [-1 for x in range(nRB)]
    assigned = []
    currentRates = np.asarray([0 for x in range(Nc)])

    lambdas = []
    rates = []
    for ms,R in zip(msCh, preAv):
        rates.append(chGainsToRates(ms, Pc, bw, N0))
        lambdas.append(chGainsToRates(ms, Pc, bw, N0) / R)
    lambdast = lambdas
    lambdas = np.transpose(lambdas)

    # for each RB that is
    for i in range(len(lambdas)):
        sortedLambdas = np.argsort(lambdas[i])
        toAssign = len(sortedLambdas) - 1
        while(sortedLambdas[toAssign] in assigned):
            toAssign -= 1
        if(len(assignment[sortedLambdas[toAssign]]) == 0):
            if(i > 0):
                assigned.append(assignmentRB[i - 1])
        assignment[sortedLambdas[toAssign]].append(i)
        assignmentRB[i] = sortedLambdas[toAssign]
    for i in range(Nc):
        for y in assignment[i]:
            #currentRates[i] += lambdast[i][y]
            currentRates[i] += rates[i][y]
        if(len(assignment[i]) == 0):
            currentRates[i] = 1
    gcBs = [msCh[assignmentRB[i]][i] for i in range(len(assignmentRB))]
    return assignment, assignmentRB, gcBs, currentRates

rateVariationCell = []
rateVariationD2d = []

for dist in range(20, 110, 10):
    for i in range(0, Nd):   # D2D Users
        t,r = g.getD2DInHex(dist)
        d2d_tx.append(t)
        d2d_rx.append(r)

    # totalTime = 1800 * 1000
    totalTime = 200

    cellR = [1 for x in range(Nc)]
    d2dR = [1 for x in range(Nd)]

    cellRwindow = cs.meanwindow(cellR, RWindowSize)
    d2dRwindow = cs.meanwindow(d2dR, RWindowSize)

    tempRateCell = []
    tempRateD2d = []

    for i in range(totalTime):
        gcB = getGcbMatrix(Nc, cellUsers, nRB)
        alloc, allocRB, gcBs, rates = initAllocate(gcB, cellRwindow.get())
        Rcell = cellRwindow.update(rates)

        tempRateCell.append(np.sum(rates))

        normize = 1
        nor_rates = []
        rates = []
        g_dTB, g_dTdR, g_CdR = chGains(Nd, nRB, cellUsers, allocRB, d2d_tx, d2d_rx, Pc, dist)
        g_CB = np.asarray(gcBs)
        for d in range(Nd):
            P_dT =  (((Pc * g_CB) / (tSNR * g_dTB[d])) - (N0 / g_dTB[d]))
            # Power of D2D transmitter for all RBs  (checking for all RB occupied by cell users)
            P_dT = valid(P_dT)
            #print(" A. Power that can be sent by d2d Txs", d, ": ", P_dT)
            r = (1 + ((P_dT * g_dTdR) / (N0 + (Pc * g_CdR[d]))))
            r_d2d = bw * np.log2(r)
            r_d2dN = r_d2d / normize
            # Rate achievable by D2D for all K s.
            #print(" B. Rate achievable by D2D",d,": ", r_d2d)
            #print("\n")

            nor_rates.append(list(r_d2dN))
            rates.append(list(r_d2d))
        lambdas = []
        for ratelist,Rd2d in zip(rates, d2dRwindow.get()):
            lambdas.append(ratelist / Rd2d)
        alloc = allocate_d2d(lambdas, rbPerD2DPair)
        d2dRates = [rates[x[1][0]][x[1][1]] for x in alloc]
        d2dRwindow.update(d2dRates)
        tempRateD2d.append(np.sum(d2dRates))
    rateVariationCell.append(np.mean(tempRateCell))
    rateVariationD2d.append(np.mean(tempRateD2d))

pl.plot(range(20, 110, 10), rateVariationCell)
pl.plot(range(20, 110, 10), rateVariationD2d)
pl.show()
