import pylab as pl
import numpy as np

tsym1 = 1e-3
tsym2 = 2.5e-3

# 1 k
a = [1, 1, 1, -1, 1, 1, 1, 1, -1]

# 400
b = [1, -1, -1, 1, 1, -1]

# 100 k
ts = 0.01e-3

total = 9e-3

sig = []
for i in np.arange(0, total, ts):
    sig.append(a[int(i/tsym1)] + b[int(i/tsym2)])


#pl.plot(a)
#pl.plot(b)
pl.plot(np.arange(0, total, ts), sig)
pl.show()
