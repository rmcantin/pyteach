#!/usr/bin/env python
"""
This demo shows how the Metropolis-Hastings algorithm 
with/without annealing can be used to sample from a 
mixture of 2 Gaussians if we can sample from a Gaussian 
proposal. 

You can play and see the effects of the proposal, the 
annealing and the cooling schedule. Try to define new 
proposals and target functions.

Depends on numpy and pylab. Tested in Python 2.6

Author: Nando de Freitas (matlab code)
        Ruben Martinez-Cantin (python port)
"""


import time
import numpy as np
import matplotlib.pylab as pl

#Target distribution is a mixture of Gaussians.
def fgaussian(x,sigma):
    return np.exp(-0.5 * (x)**2 / sigma**2)/(np.sqrt(2*np.pi)*sigma)

def fmixture(x):
    sigma = 2      #  Standard deviation of the target components.
    return 0.3*fgaussian(x,sigma) + 0.7*fgaussian(x-10,sigma)

# Metropolis-Hasting
###################################################################
# MH proposal is a zero mean Gaussian.
def sample_proposal(sigma):
    return sigma * np.random.randn(1)

def mh_step(x,sigma_prop,Temp=1.0):
    u = np.random.rand(1)
    z = sample_proposal(sigma_prop)
    alpha1 = fmixture(x+z)  # Prob. of the sample after the move
    alpha2 = fmixture(x)    # Prob. of the sample before the move
    alpha = (alpha1/alpha2)

    if Temp!=1.0:
        alpha = alpha**(1.0/Temp)      # Use annealing if required.
    
    if (u < alpha):
        return x + z               # Accept jump
    else:
        return x                   # Reject jump

# Slice sampling
###################################################################
def sweep(f,x,y,w):
    #step out
    r = np.random.rand(1)
    xl = x - r*w
    xr = x + (1-r)*w
    
    while f(xl)>y: xl -= w;
    while f(xr)>y: xr += w;

    #shrink
    modified = True
    while modified:
        x_new = (xr-xl) * np.random.rand(1) + xl
        if f(x_new) < y:
            if x_new > x:
                xr = x_new
            elif x_new < x:
                xl = x_new
            else:
                print("Error. Slice colapsed!")
                modified=False
        else:
            modified=False

    return x_new, xl, xr

def slice_step(x,sigma_prop):
    y_max = fmixture(x)
    u = np.random.rand(1)*y_max
    x_new,xl,xr = sweep(fmixture,x,u,sigma_prop)
    return x_new
        


# Main function
def mcmc(sampler,n_samples):
    sigma_prop = 10         #  Standard deviation of the Gaussian proposal.
    T_i = 1.0               #  Initial temperature (only used for annealing)
    CS = 0.995              #  Cooling schedule (only used for annealing)
    x = np.zeros((n_samples,1))  #  Markov chain (unknowns).
    x[0] = 20*np.random.rand(1)       #  Initial point of the Markov Chain.

    for i in range(1,n_samples):
        if sampler == 'mh':
            x[i] = mh_step(x[i-1],sigma_prop)
        elif sampler == 'sa':
            x[i] = mh_step(x[i-1],sigma_prop,T_i)
            T_i = T_i*CS    # Adjust the cooling schedule.
        elif sampler == 'slice':
            x[i] = slice_step(x[i-1],sigma_prop)
        else:
            print("Error. Sampler not supported.")
            break
        
    return x


def plot_all(x, spIndex , mcIndex ):
    N_bins = 50               #  Number of bins in the histogram.
    pl.subplot(spIndex)
    x_t = np.linspace(-10,20,1000)
    n, bins, patches = pl.hist(x[0:mcIndex], N_bins,
                               density=1, facecolor='green', alpha=0.75)
    pl.plot(x_t,fmixture(x_t),'k',linewidth=2)
    pl.axis([-10, 20, 0, 0.15])
    plot_name = 'Iteration = %d' % mcIndex
    pl.title(plot_name)


N = 5000                #  Number of iterations.
sampler_name = 'mh'
begin = time.process_time()
particles = mcmc(sampler_name,N)

print(particles)
print(time.process_time()-begin)

plot_all(particles,221,100)
plot_all(particles,222,500)
plot_all(particles,223,1000)
plot_all(particles,224,N)

pl.suptitle(sampler_name+' sampler')
pl.show()
