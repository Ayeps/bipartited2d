import numpy as np
import random
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)

Pc = 0.25
number_of_channels = 10
g1 = np.random.rayleigh(1,number_of_channels)
g_CB = np.zeros(number_of_channels)

N_dBm = -174
bw = 160e3
N0 = (10**(N_dBm / 10)) * 10**(-3)
N0 = N0 * bw

d_CB = []
snr = []
target_snr = [7.7] * number_of_channels

a = [144,144]

for i in range(0, number_of_channels):
    d_CB.append(np.sqrt(a[0]**2 + a[1]**2) / 1000)

pL = 128.1 + 37.6 * np.log10(d_CB)
pl = 10**(pL / 10)

for i in range(0, number_of_channels):
        g_CB[i] = (g1[i]**2) / pl[i]

for i in range(0, number_of_channels):
    snr.append((10*np.log10((Pc * g_CB[i]) / N0))-25)

print(snr)
ax.grid(linestyle=':', linewidth='0.5', color='black')
ax.set_axisbelow(True)

plt.bar(np.arange(1,(number_of_channels+1),1), snr, color='#45B248', label='Cell user SNR')
plt.bar(np.arange(1,(number_of_channels+1),1), target_snr, color='#2E76EB', label='Target SNR')

plt.xticks(np.arange(1,(number_of_channels+1),1))
ax.set_xlabel('Resource Blocks')
ax.set_ylabel('SNR (in dB)')
plt.legend(loc='upper left')
plt.show()
