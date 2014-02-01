#!/usr/bin/env python
"""
This script is used to show the Central Limit Theorem based on the sume of
several dices/coins. It can also be seen as a Galton Board simulator.

Author: Ruben Martinez-Cantin <rmcatin@unizar.es>
"""
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.animation as animation

# ********************* Configuration parameters ****************************
# For the Galton board simulator, used a 2 face dice (coin). Then, the
# number of dices represents the number of pivot rows.
faces = 2
dices = 20
iters = 2000
# ***************************************************************************

fig, ax = plt.subplots()


center = np.array(range(dices-1,faces*dices))
left = center+0.5
right = center+1.5
bottom = np.zeros(len(left))
nrects = len(left)

# histogram our data with numpy
data = np.asarray([np.sum(np.random.random_integers(faces,size=(dices,1))) for i in xrange(iters)])
n, bins = np.histogram(data, np.append(left,right[-1]))

# We precompute the top values to get the axis limits
top = bottom + n


# here comes the tricky part -- we have to set up the vertex and path
# codes arrays using moveto, lineto and closepoly

# for each rect: 1 for the MOVETO, 3 for the LINETO, 1 for the
# CLOSEPOLY; the vert for the closepoly is ignored but we still need
# it to keep the codes aligned with the vertices
nverts = nrects*(1+3+1)
verts = np.zeros((nverts, 2))
codes = np.ones(nverts, int) * path.Path.LINETO
codes[0::5] = path.Path.MOVETO
codes[4::5] = path.Path.CLOSEPOLY
verts[0::5,0] = left
verts[0::5,1] = bottom
verts[1::5,0] = left
verts[1::5,1] = top
verts[2::5,0] = right
verts[2::5,1] = top
verts[3::5,0] = right
verts[3::5,1] = bottom

barpath = path.Path(verts, codes)
patch = patches.PathPatch(barpath, facecolor='blue', edgecolor='cyan', alpha=0.75)
ax.add_patch(patch)

ax.set_xlim(left[0], right[-1])
ax.set_ylim(bottom.min(), top.max())

def animate(i):
    # simulate new data coming in
    x = data[1:i]
    n, bins = np.histogram(x, np.append(left,right[-1]))
    top = bottom + n
    verts[1::5,1] = top
    verts[2::5,1] = top

ani = animation.FuncAnimation(fig, animate, iters, interval=5, repeat=False)
plt.show()
