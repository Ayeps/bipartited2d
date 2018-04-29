import numpy as np
import random
import pylab as pl

def bpsk():
	# BPSK Modulation
	# Every frame 1ms : i.e 500 symbols are being transmitted (CU Rate=500kbps, required)

	# 4 cell users/RBs, 2 D2D txs
	RB = 4  # No. of RBs

	RB_Cell = [0,1,2,3]			# RB allotment for Cell users
	P_cell	= 0.25				# Power Tx by cell users
	g_CB    = [0.22,0.34,1.2,0.78]			# Gain CU->BS
	g_CdT	= [0.56,0.78,0.23,0.98]			# Gain D2D TX->BS

	RB_D2D	= [0,-  1,  1,-1]		# RB allotment for Cell users
	P_D2D	= [0.20,0,0.05,0]		# Power Tx by D2D Tx
	g_dTdR	= [0.56,0,0.23,0]			# Gain D2d Tx-> D2d Rx
	g_CdR	= [0.56,0.78,0.23,0.98]			# Gain CU->D2D Rx

	# sampling freq
	fs = 3e6
	ts = 1/fs
	dur = 1e-3
	signal = []

	tcell = 1 / 500e3
	ncell = int(dur / tcell)
	#for r in range(0,RB):
	datacell	= np.random.randint(2, size=ncell)
	datacell	= 1-2*datacell

	d2d_rate = 50e3
	td2d = 1 / d2d_rate
	nd2d = int(dur / td2d)
	datad2d = np.random.randint(2, size=nd2d)
	datad2d	= 1-2*datad2d

	for i in np.arange(0, dur, ts):
		signal.append(datacell[int(i / tcell)] + (0.3) * datad2d[int(i / td2d)] + np.random.random(1))

	nsamp = int(tcell / ts)
	decoded = []

	prev = 0
	store = []
	j = 0
	for i in np.arange(0, dur, ts):
		if(int(i / tcell) > prev):
			if(np.mean(store) > 0):
				decoded.append(1)
			else:
				decoded.append(-1)
			#decoded.append(np.mean(store))
			store = [signal[j]]
			prev = int(i / tcell)
		else:
			store.append(signal[j])
		j += 1
	if(np.mean(store) > 0):
		decoded.append(1)
	else:
		decoded.append(-1)

	err = np.asarray(datacell) - np.asarray(decoded)
	errors = 0
	for i in err:
		if(i != 0):
			errors += 1
	print(errors)

for i in range(100):
	bpsk()
