# This demo shows how the Slice sampling algorithm can be used to
# sample from a mixture of 2 Gaussians if we can sample from a
# Gaussian proposal.
#
# Depends on numpy and pylab. Tested in Python 2.6
#
# Author: Ruben Martinez-Cantin
#


import pylab as pl
import numpy as np
from numpy.random import rand, randn



# Target functions
#=================
def fgaussian(x, sigma):
    return np.exp(-0.5 * (x)**2 / sigma**2)/(np.sqrt(2*np.pi)*sigma)

def fmixture(x, sigma):
    return 0.3*fgaussian(x,sigma) + 0.7*fgaussian(x-10,sigma)

def sweep(f,x,y,w,params):
    #step out
    r = rand(1)
    xl = x - r*w
    xr = x + (1-r)*w
    
    while f(xl,params)>y:
        xl -= w;

    while f(xr,params)>y:
        xr += w;

    #shrink
    modified = True
    while modified:
        x_new = (xr-xl) * rand(1) + xl
        if f(x_new,params) < y:
            if x_new > x:
                xr = x_new
            elif x_new < x:
                xl = x_new
            else:
                print "Error. Slice colapsed!"
                modified=False
        else:
            modified=False

    return x_new, xl, xr

# DEFINITIONS:
# ============
N = 5000                  #  Number of iterations.
sigma = 2                 #  Standard deviation of the target components.
x = np.zeros((N,1))       #  Markov chain (unknowns).
sigma_prop = 100           #  Standard deviation of the Gaussian proposal.
N_bins = 50               #  Number of bins in the histogram.

# RUN MCMC:
# =========
x[0,0] = 20*rand(1)       #  Initial point of the Markov Chain.


for i in range(1,N):
    y_max = fmixture(x[i-1],sigma)
    u = rand(1)*y_max
    x[i],xl,xr = sweep(fmixture,x[i-1],u,sigma_prop,sigma)

print x


# PLOT THE HISTOGRAMS:
# ====================
def plot_all( spIndex , mcIndex ):

    pl.subplot(spIndex)
    x_t = np.linspace(-10,20,1000)
    n, bins, patches = pl.hist(x[0:mcIndex], N_bins, normed=1, facecolor='green', alpha=0.75)
    pl.plot(x_t,fmixture(x_t,sigma),'k',linewidth=2)
    pl.axis([-10, 20, 0, 0.15])
    plot_name = 'Iteration = %d' % mcIndex
    pl.title(plot_name)


plot_all(221,100)
plot_all(222,500)
plot_all(223,1000)
plot_all(224,N)

pl.show()
