#
#   EE 764
#   Wireless & Mobile Communication
#   Simulation Assignment 4
#
#   Single Cell Scenario
#
#   Author: Ritesh
#   RollNo: 163079001
#
# # # # # # # # # # # # # # # # # # # # #

import cellsys as cs
import sys
import numpy as np
import pylab as pl
import math

Rc = 500
ntiers = 1

Nc = 20

brush = cs.draw(Rc)
g = cs.geom(Rc)

fig1 = pl.figure()
cells = brush.drawTiers(ntiers, (0, 0), fig1, "#EEEEEE")
cells = g.ijtoxy(cells)
ax = fig1.gca()
figsz = math.ceil((2 * (ntiers + 0.6)) * brush.redge)
ax.set_xlim(-figsz, figsz)
ax.set_ylim(-figsz, figsz)
ax.set_aspect('equal')

nMobStatsPerCell = 100

cellUsers = []
for i in range(0, Nc):
    p = g.getRandomPointInHex()
    cellUsers.append(p)
    pl.scatter(p[0], p[1], s=2, color="#00FF00", zorder=2)

pl.show()
