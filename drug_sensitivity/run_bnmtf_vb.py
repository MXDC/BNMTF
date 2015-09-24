"""
Run BNMTF with the Exp priors on the Sanger dataset.
"""

project_location = "/home/tab43/Documents/Projects/libraries/"
import sys
sys.path.append(project_location)

from BNMTF.code.bnmtf_vb import bnmtf_vb
from BNMTF.code.bnmtf_vb_optimised import bnmtf_vb_optimised
from ml_helpers.code.mask import compute_Ms, compute_folds
from load_data import load_Sanger

import numpy, matplotlib.pyplot as plt, random

##########

standardised = False #standardised Sanger or unstandardised
no_folds = 5

iterations = 20
I, J, K, L = 622,139,10,5

init_S = 'random' #'exp' #
init_FG = 'kmeans' #'exp' #
tauFSG = {
    'tauF' : 100*numpy.ones((I,K)),
    'tauS' : 100*numpy.ones((K,L)),
    'tauG' : 100*numpy.ones((J,L))  
}

alpha, beta = 1., 1.
lambdaF = numpy.ones((I,K))
lambdaS = numpy.ones((K,L))/50
lambdaG = numpy.ones((J,L))
priors = { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF, 'lambdaS':lambdaS, 'lambdaG':lambdaG }

# Load in data
(_,X_min,M,_,_,_,_) = load_Sanger(standardised=standardised)

folds_test = compute_folds(I,J,no_folds,M)
folds_training = compute_Ms(folds_test)
(M_train,M_test) = (folds_training[0],folds_test[0])

# Run the Gibbs sampler
#BNMTF = bnmtf_vb(X_min,M,K,L,priors)
BNMTF = bnmtf_vb_optimised(X_min,M,K,L,priors)
BNMTF.initialise(init_S=init_S,init_FG=init_FG,tauFSG=tauFSG)
BNMTF.run(iterations)

# Also measure the performances
performances = BNMTF.predict(M_test)
print performances

# Plot the tau expectation values to check convergence
plt.plot(BNMTF.all_exp_tau)