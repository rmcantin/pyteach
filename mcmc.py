# This demo shows how the Metropolis-Hastings algorithm 
# with/without annealing can be used to sample from a 
# mixture of 2 Gaussians if we can sample from a Gaussian 
# proposal. 
#
# You can play and see the effects of the proposal, the 
# annealing and the cooling schedule. Try to define new 
# proposals and target functions.
#
# Depends on numpy and pylab. Tested in Python 2.6
#
# Author: Nando de Freitas (matlab code)
#         Ruben Martinez-Cantin (python port)
#


from pylab import *
from numpy import *
from numpy.random import *


# Target functions
#=================
def fgaussian(x, sigma): return exp(-0.5 * (x)**2 / sigma**2)/(sqrt(2*pi)*sigma)
def fmixture(x,sigma): return 0.3*fgaussian(x,sigma) + 0.7*fgaussian(x-10,sigma)


# DEFINITIONS:
# ============

SA = False                #  If no annealing, the algorithm is exactly MH

N = 5000                  #  Number of iterations.
sigma = 2                 #  Standard deviation of the target components.
x = zeros((N,1))          #  Markov chain (unknowns).
sigma_prop = 10           #  Standard deviation of the Gaussian proposal.
N_bins = 50               #  Number of bins in the histogram.

T_i = 1.0                 #  Initial temperature (only used for annealing)
CS = 0.995                #  Cooling schedule (only used for annealing)

# RUN MCMC:
# =========
x[0,0] = 20*rand(1)       #  Initial point of the Markov Chain.


for i in range(1,N):
     u = rand(1)
     z = sigma_prop * randn(1)
     alpha1 = fmixture(x[i-1]+z,sigma)  # Probability of the sample after the move
     alpha2 = fmixture(x[i-1],sigma)    # Probability of the sample before the move
     alpha = (alpha1/alpha2)

     if SA:
	alpha = alpha**(1/T_i)          # Use annealing if required.
	T_i = T_i*CS                    # Adjust the cooling schedule. (only used for annealing)

     if (u < alpha):
        x[i] = x[i-1] + z               # Accept jump
     else:
        x[i] = x[i-1]                   # Reject jump
        
print x


# PLOT THE HISTOGRAMS:
# ====================
def plot_all( spIndex , mcIndex ):
     subplot(spIndex)
     x_t = linspace(-10,20,1000)
     n, bins, patches = hist(x[0:mcIndex], N_bins, normed=1, facecolor='green', alpha=0.75)
     plot(x_t,fmixture(x_t,sigma),'k',linewidth=2)
     axis([-10, 20, 0, 0.15])
     plot_name = 'Iteration = %d' % mcIndex
     title(plot_name)


plot_all(221,100)
plot_all(222,500)
plot_all(223,1000)
plot_all(224,N)

show()
