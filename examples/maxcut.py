#!/usr/bin/python
import cvxpy as cvx
import qcqp
import numpy as np

n = 30
np.random.seed(1)

# Make adjacency matrix.
W = np.random.binomial(1, 0.2, size=(n, n))
W = np.asmatrix(W)

x = cvx.Variable(n)
obj = 0.25*(cvx.sum_entries(W) - cvx.quad_form(x, W))
cons = [cvx.square(x) == 1]
prob = cvx.Problem(cvx.Maximize(obj), cons)

ub = prob.solve(method='sdp-relax', solver=cvx.MOSEK)
print ('Upper bound: %.3f' % ub)

x_round = np.sign(np.random.randn(n, 1))
lb = 0.25*(np.sum(W) - (x_round.T*W*x_round)[0, 0])
print ('Simple lower bound: %.0f' % lb)

lb = prob.solve(method='coord-descent', solver=cvx.MOSEK, num_samples=10)
print ('Coordinate descent lower bound: %.0f' % lb)
