import math
# Custom functions file

def WeibullCDF(x, lmbd, k):
	q = pow(x / lmbd, k)
	return 1.0 - math.exp(-q)

def ProbNede(tid_inne, levetid, weib_shape):
	cdf_start = WeibullCDF(tid_inne, levetid, weib_shape)
	survival_start = 1 - cdf_start
	p_nede = []
	for i in range(tid_inne, levetid):
		p_nede.append((WeibullCDF(i, levetid, weib_shape) - cdf_start) / survival_start)
	return p_nede

def ProbSurvival(tid_inne, levetid, weib_shape):
	survival_start = 1 - WeibullCDF(tid_inne, levetid, weib_shape)
	p_survival = []
	for i in range(tid_inne, levetid):
		p_survival.append((1 - WeibullCDF(i, levetid, weib_shape)))
	return p_survival

def Nedetidskost(kost_defekt, leveringstid, p):
	c = [i * kost_defekt * (leveringstid * 7) for i in p]
	return c