"""
Recover the toy dataset with obvious biclusters.

R = [
    [10 (times 10), 30 (times 10)]  (times 10)
    [40 (times 10), 20 (times 10)]  (times 5)
    [40 (times 10), 50 (times 10)]  (times 5)
]
F = [
    [1,0,0]  (times 10)
    [0,1,0]  (times 5)
    [0,1,1]  (times 5)
]
G = [
    [1,0]  (times 10)
    [0,1]  (times 10)
]
S = [
    [10,30] 
    [40,20]
    [40,50]
]
"""

project_location = "/home/tab43/Documents/Projects/libraries/"
import sys
sys.path.append(project_location)

from BNMTF.code.bnmtf_vb import bnmtf_vb
from ml_helpers.code.mask import generate_M, calc_inverse_M

import numpy, matplotlib.pyplot as plt

##########

F = numpy.array([[1,0,0] for i in range(0,10)] + [[0,1,0] for i in range(0,5)] + [[0,0,1] for i in range(0,5)])
S = numpy.array([[10,30],[40,20],[40,50]])
G = numpy.array([[1,0] for i in range(0,10)] + [[0,1] for i in range(0,10)])

R = numpy.dot(F,numpy.dot(S,G.T))

iterations = 50
init_S = 'random'
init_FG = 'kmeans'
I, J, K, L = 20, 20, 3, 2
fraction_unknown = 0.6

alpha, beta = 1., 1.
lambdaF = numpy.ones((I,K))*1
lambdaS = numpy.ones((K,L))/50
lambdaG = numpy.ones((J,L))*1
priors = { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF, 'lambdaS':lambdaS, 'lambdaG':lambdaG }

M = generate_M(I,J,fraction_unknown)
M_test = calc_inverse_M(M)

# Run the Gibbs sampler
BNMTF = bnmtf_vb(R,M,K,L,priors)
BNMTF.initialise(init_S=init_S,init_FG=init_FG)
BNMTF.run(iterations)

# Also measure the performances
performances = BNMTF.predict(M_test)
print performances

# Plot the tau expectation values to check convergence
plt.plot(BNMTF.all_exp_tau)

print "F: %s." % BNMTF.expF
print "S: %s." % BNMTF.expS
print "G: %s." % BNMTF.expG