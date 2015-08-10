"""
Tests for the BNMF Variational Bayes algorithm.
"""

import numpy, math, pytest, itertools, random
from BNMTF.code.bnmf_vb import bnmf_vb


""" Test constructor """
def test_init():
    # Test getting an exception when R and M are different sizes, and when R is not a 2D array.
    R1 = numpy.ones(3)
    M = numpy.ones((2,3))
    I,J,K = 5,3,1
    lambdaU = numpy.ones((I,K))
    lambdaV = numpy.ones((J,K))
    alpha, beta = 3, 1    
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }
    
    with pytest.raises(AssertionError) as error:
        bnmf_vb(R1,M,K,priors)
    assert str(error.value) == "Input matrix R is not a two-dimensional array, but instead 1-dimensional."
    
    R2 = numpy.ones((4,3,2))
    with pytest.raises(AssertionError) as error:
        bnmf_vb(R2,M,K,priors)
    assert str(error.value) == "Input matrix R is not a two-dimensional array, but instead 3-dimensional."
    
    R3 = numpy.ones((3,2))
    with pytest.raises(AssertionError) as error:
        bnmf_vb(R3,M,K,priors)
    assert str(error.value) == "Input matrix R is not of the same size as the indicator matrix M: (3, 2) and (2, 3) respectively."
    
    # Similarly for lambdaU, lambdaV
    R4 = numpy.ones((2,3))
    lambdaU = numpy.ones((2+1,1))
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }
    with pytest.raises(AssertionError) as error:
        bnmf_vb(R4,M,K,priors)
    assert str(error.value) == "Prior matrix lambdaU has the wrong shape: (3, 1) instead of (2, 1)."
    
    lambdaU = numpy.ones((2,1))
    lambdaV = numpy.ones((3+1,1))
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }
    with pytest.raises(AssertionError) as error:
        bnmf_vb(R4,M,K,priors)
    assert str(error.value) == "Prior matrix lambdaV has the wrong shape: (4, 1) instead of (3, 1)."
    
    # Test getting an exception if a row or column is entirely unknown
    lambdaU = numpy.ones((2,1))
    lambdaV = numpy.ones((3,1))
    M1 = [[1,1,1],[0,0,0]]
    M2 = [[1,1,0],[1,0,0]]
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }
    
    with pytest.raises(AssertionError) as error:
        bnmf_vb(R4,M1,K,priors)
    assert str(error.value) == "Fully unobserved row in R, row 1."
    with pytest.raises(AssertionError) as error:
        bnmf_vb(R4,M2,K,priors)
    assert str(error.value) == "Fully unobserved column in R, column 2."
    
    # Finally, a successful case
    I,J,K = 3,2,2
    R5 = 2*numpy.ones((I,J))
    lambdaU = numpy.ones((I,K))
    lambdaV = numpy.ones((J,K))
    M = numpy.ones((I,J))
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }
    BNMF = bnmf_vb(R5,M,K,priors)
    
    assert numpy.array_equal(BNMF.R,R5)
    assert numpy.array_equal(BNMF.M,M)
    assert BNMF.I == I
    assert BNMF.J == J
    assert BNMF.K == K
    assert BNMF.size_Omega == I*J
    assert BNMF.alpha == alpha
    assert BNMF.beta == beta
    assert numpy.array_equal(BNMF.lambdaU,lambdaU)
    assert numpy.array_equal(BNMF.lambdaV,lambdaV)
    
    
""" Test initialing parameters """
def test_initialise():
    I,J,K = 5,3,2
    R = numpy.ones((I,J))
    M = numpy.ones((I,J))
    
    lambdaU = 2*numpy.ones((I,K))
    lambdaV = 3*numpy.ones((J,K))
    alpha, beta = 3, 1
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }
    
    # Initialisation without custom values
    BNMF = bnmf_vb(R,M,K,priors)
    BNMF.initialise()
    
    assert BNMF.alpha_s == alpha
    assert BNMF.beta_s == beta
    for i,k in itertools.product(xrange(0,I),xrange(0,K)):
        assert BNMF.tauU[i,k] == 1.
        assert BNMF.muU[i,k] == 1./lambdaU[i,k]
    for j,k in itertools.product(xrange(0,J),xrange(0,K)):
        assert BNMF.tauV[j,k] == 1.
        assert BNMF.muV[j,k] == 1./lambdaV[j,k]
        
    # Test whether the expectation and variance values are correctly computed
    assert BNMF.exptau == alpha/beta
    for i,k in itertools.product(xrange(0,I),xrange(0,K)):
        assert abs(BNMF.expU[i,k] - (0.5 + 0.352065 / (1-0.3085))) < 0.0001
    for j,k in itertools.product(xrange(0,J),xrange(0,K)):
        assert abs(BNMF.expV[j,k] - (1./3. + 0.377383 / (1-0.3694))) < 0.0001
    
    # Then initialise with predefined values. First override muU, tauV, alpha_s
    values1 = {
        'muU' : numpy.ones((I,K))*100, 
        'tauV' : numpy.ones((J,K))*5, 
        'alpha_s' : 12.
    
    }
    BNMF = bnmf_vb(R,M,K,priors)
    BNMF.initialise(values1)
    
    assert BNMF.alpha_s == 12.
    assert BNMF.beta_s == beta
    for i,k in itertools.product(xrange(0,I),xrange(0,K)):
        assert BNMF.tauU[i,k] == 1.
        assert BNMF.muU[i,k] == 100.
    for j,k in itertools.product(xrange(0,J),xrange(0,K)):
        assert BNMF.tauV[j,k] == 5.
        assert BNMF.muV[j,k] == 1./lambdaV[j,k]
        
    # Then override tauU, muV, beta_s
    values2 = {
        'tauU' : numpy.ones((I,K))*10,
        'muV' : numpy.ones((J,K))*200,
        'beta_s' : 13.
    }
    BNMF = bnmf_vb(R,M,K,priors)
    BNMF.initialise(values2)
    
    assert BNMF.alpha_s == alpha
    assert BNMF.beta_s == 13.
    for i,k in itertools.product(xrange(0,I),xrange(0,K)):
        assert BNMF.tauU[i,k] == 10.
        assert BNMF.muU[i,k] == 1./lambdaU[i,k]
    for j,k in itertools.product(xrange(0,J),xrange(0,K)):
        assert BNMF.tauV[j,k] == 1.
        assert BNMF.muV[j,k] == 200.
        
        
""" Test computing the ELBO. """
def test_elbo():
    #TODO:
    return
    
        
""" Test updating parameters U, V, tau """          
I,J,K = 5,3,2
R = numpy.ones((I,J))
M = numpy.ones((I,J))
M[0,0], M[2,2], M[3,1] = 0, 0, 0

lambdaU = 2*numpy.ones((I,K))
lambdaV = 3*numpy.ones((J,K))
alpha, beta = 3, 1
priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }

def test_exp_square_diff():
    BNMF = bnmf_vb(R,M,K,priors)
    BNMF.expU = 1./lambdaU #[[1./2.]]
    BNMF.expV = 1./lambdaV #[[1./3.]]
    BNMF.varU = numpy.ones((I,K))*2 #[[2.]]
    BNMF.varV = numpy.ones((J,K))*3 #[[3.]]
    # expU * expV.T = [[1./3.]]. (varU+expU^2)=2.25, (varV+expV^2)=3.+1./9.
    exp_square_diff = 172.66666666666666 #12.*(4./9.) + 12.*(2*(2.25*(3.+1./9.)-0.25/9.)) 
    assert BNMF.exp_square_diff() == exp_square_diff

def test_update_tau():
    BNMF = bnmf_vb(R,M,K,priors)
    BNMF.expU = 1./lambdaU #[[1./2.]]
    BNMF.expV = 1./lambdaV #[[1./3.]]
    BNMF.varU = numpy.ones((I,K))*2 #[[2.]]
    BNMF.varV = numpy.ones((J,K))*3 #[[3.]]
    BNMF.update_tau()
    assert BNMF.alpha_s == alpha + 12./2.
    assert BNMF.beta_s == beta + 172.66666666666666/2.
    
def test_update_U():
    for i,k in itertools.product(xrange(0,I),xrange(0,K)):
        BNMF = bnmf_vb(R,M,K,priors)
        BNMF.muU = numpy.zeros((I,K))
        BNMF.tauU = numpy.zeros((I,K))
        BNMF.expU = 1./lambdaU #[[1./2.]]
        BNMF.expV = 1./lambdaV #[[1./3.]]
        BNMF.varU = numpy.ones((I,K))*2 #[[2.]]
        BNMF.varV = numpy.ones((J,K))*3 #[[3.]]
        BNMF.exptau = 3.
        BNMF.update_U(i,k)
        assert BNMF.tauU[i,k] == 3. * (M[i] * ( BNMF.expV[:,k]*BNMF.expV[:,k] + BNMF.varV[:,k] )).sum()
        assert BNMF.muU[i,k] == (1./(3. * (M[i] * ( BNMF.expV[:,k]*BNMF.expV[:,k] + BNMF.varV[:,k] )).sum())) * \
                                ( -2. + BNMF.exptau * (M[i]*( (BNMF.R[i] - numpy.dot(BNMF.expU[i],BNMF.expV.T) + BNMF.expU[i,k]*BNMF.expV[:,k])*BNMF.expV[:,k] )).sum() )

def test_update_V():
    for j,k in itertools.product(xrange(0,J),xrange(0,K)):
        BNMF = bnmf_vb(R,M,K,priors)
        BNMF.muV = numpy.zeros((J,K))
        BNMF.tauV = numpy.zeros((J,K))
        BNMF.expU = 1./lambdaU #[[1./2.]]
        BNMF.expV = 1./lambdaV #[[1./3.]]
        BNMF.varU = numpy.ones((I,K))*2 #[[2.]]
        BNMF.varV = numpy.ones((J,K))*3 #[[3.]]
        BNMF.exptau = 3.
        BNMF.update_V(j,k)
        assert BNMF.tauV[j,k] == 3. * (M[:,j] * ( BNMF.expU[:,k]*BNMF.expU[:,k] + BNMF.varU[:,k] )).sum()
        assert BNMF.muV[j,k] == (1./(3. * (M[:,j] * ( BNMF.expU[:,k]*BNMF.expU[:,k] + BNMF.varU[:,k] )).sum())) * \
                                ( -3. + BNMF.exptau * (M[:,j]*( (BNMF.R[:,j] - numpy.dot(BNMF.expU,BNMF.expV[j]) + BNMF.expU[:,k]*BNMF.expV[j,k])*BNMF.expU[:,k] )).sum() )


""" Test computing expectation, variance U, V, tau """     
def test_update_exp_U():
    for i,k in itertools.product(xrange(0,I),xrange(0,K)):
        BNMF = bnmf_vb(R,M,K,priors)
        values = { 'tauU' : 4*numpy.ones((I,K)) }
        BNMF.initialise(values) # muU = [[0.5]], tauU = [[4.]]
        BNMF.update_exp_U(i,k) #-mu*sqrt(tau) = -0.5*2 = -1. lambda(1) = 0.241971 / (1-0.1587) = 0.2876155949126352. gamma = 0.37033832534958433
        assert abs(BNMF.expU[i,k] - (0.5 + 1./2. * 0.2876155949126352)) < 0.00001
        assert abs(BNMF.varU[i,k] - 1./4.*(1.-0.37033832534958433)) < 0.00001

def test_update_exp_V():
    for j,k in itertools.product(xrange(0,J),xrange(0,K)):
        BNMF = bnmf_vb(R,M,K,priors)
        values = { 'tauV' : 4*numpy.ones((I,K)) }
        BNMF.initialise(values) # muV = [[1./3.]], tauV = [[4.]]
        BNMF.update_exp_V(j,k) #-mu*sqrt(tau) = -2./3., lambda(..) = 0.319448 / (1-0.2525) = 0.4273551839464883, gamma = 
        assert abs(BNMF.expV[j,k] - (1./3. + 1./2. * 0.4273551839464883)) < 0.00001
        assert abs(BNMF.varV[j,k] - 1./4.*(1. - 0.4675359092102624)) < 0.00001
    
def test_update_exp_tau():
    BNMF = bnmf_vb(R,M,K,priors)
    BNMF.initialise()  
    BNMF.update_exp_tau()
    assert BNMF.exptau == 3.
    assert BNMF.explogtau == 0.9227843350984671393934879099175975689578406640600764 - 0.
    

""" Test two iterations of run(), and that all values have changed. """
def test_run():
    I,J,K = 10,5,2
    R = numpy.ones((I,J))
    M = numpy.ones((I,J))
    M[0,0], M[2,2], M[3,1] = 0, 0, 0
    R[0,1], R[0,2] = 2., 3.
    
    lambdaU = 2*numpy.ones((I,K))
    lambdaV = 3*numpy.ones((J,K))
    alpha, beta = 3, 1
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }
    
    iterations = 2
    
    BNMF = bnmf_vb(R,M,K,priors)
    BNMF.initialise()
    BNMF.run(iterations)
    
    for i,k in itertools.product(xrange(0,I),xrange(0,K)):
        assert BNMF.muU[i,k] != 1./lambdaU[i,k]
        assert BNMF.tauU[i,k] != 1.
        assert BNMF.expU[i,k] != numpy.inf and not math.isnan(BNMF.expU[i,k])
        assert BNMF.tauU[i,k] != numpy.inf and not math.isnan(BNMF.tauU[i,k])
    for j,k in itertools.product(xrange(0,J),xrange(0,K)):
        assert BNMF.muV[j,k] != 1./lambdaV[j,k]
        assert BNMF.tauV[j,k] != 1.
        assert BNMF.expV[j,k] != numpy.inf and not math.isnan(BNMF.expV[j,k])
        assert BNMF.tauV[j,k] != numpy.inf and not math.isnan(BNMF.tauV[j,k])
    assert BNMF.alpha_s != alpha
    assert BNMF.beta_s != beta
    assert BNMF.exptau != numpy.inf and not math.isnan(BNMF.exptau)
    assert BNMF.explogtau != numpy.inf and not math.isnan(BNMF.explogtau)
    

""" Test computing the performance of the predictions using the expectations """
def test_predict():
    (I,J,K) = (5,3,2)
    R = numpy.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12],[13,14,15]],dtype=float)
    M = numpy.ones((I,J))
    K = 3
    lambdaU = 2*numpy.ones((I,K))
    lambdaV = 3*numpy.ones((J,K))
    alpha, beta = 3, 1
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }
    
    expU = numpy.array([[125.,126.],[126.,126.],[126.,126.],[126.,126.],[126.,126.]])
    expV = numpy.array([[84.,84.],[84.,84.],[84.,84.]])
    
    M_test = numpy.array([[0,0,1],[0,1,0],[0,0,0],[1,1,0],[0,0,0]]) #R->3,5,10,11, P_pred->21084,21168,21168,21168
    MSE = (444408561. + 447872569. + 447660964. + 447618649) / 4.
    R2 = 1. - (444408561. + 447872569. + 447660964. + 447618649) / (4.25**2+2.25**2+2.75**2+3.75**2) #mean=7.25
    Rp = 357. / ( math.sqrt(44.75) * math.sqrt(5292.) ) #mean=7.25,var=44.75, mean_pred=21147,var_pred=5292, corr=(-4.25*-63 + -2.25*21 + 2.75*21 + 3.75*21)
    
    BNMF = bnmf_vb(R,M,K,priors)
    BNMF.expU = expU
    BNMF.expV = expV
    performances = BNMF.predict(M_test)
    
    assert performances['MSE'] == MSE
    assert performances['R^2'] == R2
    assert performances['Rp'] == Rp
       
        
""" Test the evaluation measures MSE, R^2, Rp """
def test_compute_statistics():
    R = numpy.array([[1,2],[3,4]],dtype=float)
    M = numpy.array([[1,1],[0,1]])
    I, J, K = 2, 2, 3
    lambdaU = 2*numpy.ones((I,K))
    lambdaV = 3*numpy.ones((J,K))
    alpha, beta = 3, 1
    priors = { 'alpha':alpha, 'beta':beta, 'lambdaU':lambdaU, 'lambdaV':lambdaV }
    
    BNMF = bnmf_vb(R,M,K,priors)
    
    R_pred = numpy.array([[500,550],[1220,1342]],dtype=float)
    M_pred = numpy.array([[0,0],[1,1]])
    
    MSE_pred = (1217**2 + 1338**2) / 2.0
    R2_pred = 1. - (1217**2+1338**2)/(0.5**2+0.5**2) #mean=3.5
    Rp_pred = 61. / ( math.sqrt(.5) * math.sqrt(7442.) ) #mean=3.5,var=0.5,mean_pred=1281,var_pred=7442,cov=61
    
    assert MSE_pred == BNMF.compute_MSE(M_pred,R,R_pred)
    assert R2_pred == BNMF.compute_R2(M_pred,R,R_pred)
    assert Rp_pred == BNMF.compute_Rp(M_pred,R,R_pred)
    