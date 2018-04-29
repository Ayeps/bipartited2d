import cellsys as cs
import allocate
import channel

import numpy as np

def valid(a):
    for i in range(0,len(a)):
        if(a[i] > 0.25):
            a[i] = 0.25
        elif(a[i] < 0):
            a[i] = 0
    return a

def core(Rc, Pc, bw, N0, tSNR, cellUsers, Nc, Nd, Nrb, d2dDistance, rbPerD2DPair, RWindowSize, simTime):
    g = cs.geom(Rc)
    d2d_tx = []
    d2d_rx = []
    for i in range(0, Nd):
        t,r = g.getD2DInHex(d2dDistance)
        d2d_tx.append(t)
        d2d_rx.append(r)

    totalTime = simTime

    cellR = [1 for x in range(Nc)]
    d2dR = [1 for x in range(Nd)]

    cellRwindow = cs.meanwindow(cellR, RWindowSize)
    d2dRwindow = cs.meanwindow(d2dR, RWindowSize)

    tempRateCell = []
    tempRateD2d = []

    for i in range(totalTime):
        gcB = channel.getGcbMatrix(Nc, cellUsers, Nrb)
        alloc, allocRB, gcBs, rates = allocate.cellAllocate(Nc, Nrb, Pc, bw, N0, gcB, cellRwindow.get())
        Rcell = cellRwindow.update(rates)

        tempRateCell.append(np.sum(rates))

        normize = 1
        nor_rates = []
        rates = []
        g_dTB, g_dTdR, g_CdR = channel.chGains(Nd, Nrb, cellUsers, allocRB, d2d_tx, d2d_rx, Pc, d2dDistance)
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
        alloc = allocate.d2dAllocate(lambdas, rbPerD2DPair)
        d2dRates = [rates[x[1][0]][x[1][1]] for x in alloc]
        d2dRwindow.update(d2dRates)
        tempRateD2d.append(np.sum(d2dRates))
    return np.mean(tempRateCell), np.mean(tempRateD2d)
