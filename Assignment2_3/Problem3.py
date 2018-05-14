#!/usr/bin/python

import sys
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# CS 323 Assignment 2_3, Part 3: Ruddy Duck Plot
#
# 4/2/18 Christopher Gonzalez

# Modification of python's range function that accepts float values
# as arguments for the step
def frange(start, stop, step):
	i = start
	while i < stop:
		yield i
		i += step

# this function calculates the coefficients for a cubic spline function
def NaturalCubicSpline(n, lstX, lstFn):
	if (len(lstX) != (n+1) or len(lstFn) != (n+1)):
		print 'Error: the length of the list of X values and/or F(x) values is not equal to n+1.'
		return -1

	# 1) for i = 0, 1, ..., n - 1, set Hi = Xi+1 - Xi
	lstH = []
	for i in range (n):
		lstH.append(float(lstX[i+1]) - float(lstX[i]))

	# 2) for i = 1, 2, ..., n - 1, set A'i = (3/Hi) * (Ai+1 - Ai) - (3/Hi-1) * (Ai - Ai-1)
	lstA = [0]
	for i in range (1, n):
		lstA.append((3 / float(lstH[i])) * (lstFn[i+1] - lstFn[i]) - (3 / float(lstH[i-1])) * (lstFn[i] - lstFn[i-1]))

	# 3) set Lo = 1; Uo = 0; Zo = 0
	lstL = [1]
	lstU = [0]
	lstZ = [0]
	
	# 4) for i = 1, 2, ..., n - 1 set
	#	Li = 2(Xi+1 - Xi-1) - Hi-1 * Ui-1
	#	Ui = Hi / Li
	#	Zi = (Ai - Hi-1 * Zi-1) / Li
	for i in range (1, n):
		lstL.append(2 * (lstX[i+1] - lstX[i-1]) - (lstH[i-1] * lstU[i-1]))
		lstU.append(lstH[i] / float(lstL[i]))
		lstZ.append((lstA[i] - lstH[i-1] * lstZ[i-1]) / float(lstL[i]))

	# 5) set Ln = 1; Zn = 0; Cn = 0
	lstL.append(1)
	lstZ.append(0)
	lstC = [0 for x in range(n+1)]
	
	# 6) for j = n -1, n - 2, ..., 0 set
	#	Cj = Zj - Uj * Cj+1
	#	Bj = (F(j+1) - F(j)) / Hj - Hj(Cj+1 + 2 * Cj) / 3
	#	Dj = (Cj+1 - Cj) / (3 * Hj)
	lstB = [None] * (n+1)
	lstD = [None] * (n+1)
	for j in range (n - 1, -1, -1):
		lstC[j] = lstZ[j] - lstU[j] * lstC[j+1]
		lstB[j] = (lstFn[j+1] - lstFn[j]) / lstH[j] - lstH[j] * (lstC[j+1] + 2 * lstC[j]) / 3
		lstD[j] = (lstC[j+1] - lstC[j]) / (3 * lstH[j])

	# 7) OUTPUT (F(j), Bj, Cj, Dj for j = 0, 1, ..., n - 1)
	#	result = [[F(0), B0, C0, D0], [F(1), B1, C1, D1], ..., [F(n-1), Bn-1, Cn-1, Dn-1]]
	result = []

	for j in range (n):
		result.append([lstFn[j], lstB[j], lstC[j], lstD[j]])
	#	print result[j] # unquote to see coefficients printed out
	
	return result

# generates a list of Y-values in order to plot the Natural Cubic Spline
# a user can enter in the space between points to create a smoother or
# rougher curve
def SplineFunctionYValues(lstCoef, lstItrvls, step):
	result = []
	for i in range(0, len(lstCoef)):
		flag = lstItrvls[i] < lstItrvls[i+1]
		for x in frange(lstItrvls[i], lstItrvls[i+1], (step if flag else -step)):
			xPoint = (x - lstItrvls[i])
			result.append(lstCoef[i][0] + lstCoef[i][1] * xPoint + lstCoef[i][2] * xPoint**2 + lstCoef[i][3] * xPoint**3)
	
	return result

# this function calculates the coefficients of Newton's Divided
# Differences
def DividedDifferences(lstX, lstFn):
	if (len(lstX) != len(lstFn)):
		'Error: there are missing x points or y points; the lists are not the same length'
		exit(-1)
	
	n = len(lstX)
	lstFij = [[0 for col in range(n)] for row in range(n)]

	for index in range(0, n):
		lstFij[index][0] = lstFn[index]

	# 1) for i = 1, 2, ..., n
	#	for j = 1, 2, ..., i
	#		set Fi,j = (Fi,j-1 - Fi-1,j-1) / (Xi - Xi-j)
	for i in range(1, n):
		for j in range(1, i+1):
			lstFij[i][j] = (lstFij[i][j-1] - lstFij[i-1][j-1]) / float(lstX[i] - lstX[i-j])
	
	# 2) OUTPUT (F0,0, F1,1, ..., Fn,n)
	#	result = [F0,0, F1,1, ..., Fn,n]
	result = [None] * n
	for num in range(0, n):
		result[num] = lstFij[num][num]
	#	print result[num] # uncomment to see coefficients printed out

	return result

# generates a list of Y-values in order to plot the interpolating polynomial
# a user can enter in the space between points to create a smoother or rougher
# curve
def InterpolPolyYValues(lstCoef, lstFn, lstItrvls, step):
	result = []
	for i in range(0, len(lstItrvls)-1):
		flag = lstItrvls[i] < lstItrvls[i+1]
		for x in frange(lstItrvls[i], lstItrvls[i+1], (step if flag else -step)):
			result.append(lstCoef[0] + \
		lstCoef[1]*(x - lstItrvls[0]) + \
		lstCoef[2]*(x - lstItrvls[0])*(x - lstItrvls[1]) + \
		lstCoef[3]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2]) + \
		lstCoef[4]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3]) + \
		lstCoef[5]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3])*(x - lstItrvls[4]) + \
		lstCoef[6]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3])*(x - lstItrvls[4])*(x - lstItrvls[5]) + \
		lstCoef[7]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3])*(x - lstItrvls[4])*(x - lstItrvls[5])*(x - lstItrvls[6]) + \
		lstCoef[8]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3])*(x - lstItrvls[4])*(x - lstItrvls[5])*(x - lstItrvls[6])*(x - lstItrvls[7]) + \
		lstCoef[9]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3])*(x - lstItrvls[4])*(x - lstItrvls[5])*(x - lstItrvls[6])*(x - lstItrvls[7])*(x - lstItrvls[8]) + \
		lstCoef[10]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3])*(x - lstItrvls[4])*(x - lstItrvls[5])*(x - lstItrvls[6])*(x - lstItrvls[7])*(x - lstItrvls[8])*(x - lstItrvls[9]) + \
		lstCoef[11]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3])*(x - lstItrvls[4])*(x - lstItrvls[5])*(x - lstItrvls[6])*(x - lstItrvls[7])*(x - lstItrvls[8])*(x - lstItrvls[9])*(x - lstItrvls[10]) + \
		lstCoef[12]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3])*(x - lstItrvls[4])*(x - lstItrvls[5])*(x - lstItrvls[6])*(x - lstItrvls[7])*(x - lstItrvls[8])*(x - lstItrvls[9])*(x - lstItrvls[10])*(x - lstItrvls[11]) + \
		lstCoef[13]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3])*(x - lstItrvls[4])*(x - lstItrvls[5])*(x - lstItrvls[6])*(x - lstItrvls[7])*(x - lstItrvls[8])*(x - lstItrvls[9])*(x - lstItrvls[10])*(x - lstItrvls[11])*(x - lstItrvls[12]) + \
		lstCoef[14]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3])*(x - lstItrvls[4])*(x - lstItrvls[5])*(x - lstItrvls[6])*(x - lstItrvls[7])*(x - lstItrvls[8])*(x - lstItrvls[9])*(x - lstItrvls[10])*(x - lstItrvls[11])*(x - lstItrvls[12])*(x - lstItrvls[13]) + \
		lstCoef[15]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3])*(x - lstItrvls[4])*(x - lstItrvls[5])*(x - lstItrvls[6])*(x - lstItrvls[7])*(x - lstItrvls[8])*(x - lstItrvls[9])*(x - lstItrvls[10])*(x - lstItrvls[11])*(x - lstItrvls[12])*(x - lstItrvls[13])*(x - lstItrvls[14]) + \
		lstCoef[16]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3])*(x - lstItrvls[4])*(x - lstItrvls[5])*(x - lstItrvls[6])*(x - lstItrvls[7])*(x - lstItrvls[8])*(x - lstItrvls[9])*(x - lstItrvls[10])*(x - lstItrvls[11])*(x - lstItrvls[12])*(x - lstItrvls[13])*(x - lstItrvls[14])*(x - lstItrvls[15]) + \
		lstCoef[17]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3])*(x - lstItrvls[4])*(x - lstItrvls[5])*(x - lstItrvls[6])*(x - lstItrvls[7])*(x - lstItrvls[8])*(x - lstItrvls[9])*(x - lstItrvls[10])*(x - lstItrvls[11])*(x - lstItrvls[12])*(x - lstItrvls[13])*(x - lstItrvls[14])*(x - lstItrvls[15])*(x - lstItrvls[16]) + \
		lstCoef[18]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3])*(x - lstItrvls[4])*(x - lstItrvls[5])*(x - lstItrvls[6])*(x - lstItrvls[7])*(x - lstItrvls[8])*(x - lstItrvls[9])*(x - lstItrvls[10])*(x - lstItrvls[11])*(x - lstItrvls[12])*(x - lstItrvls[13])*(x - lstItrvls[14])*(x - lstItrvls[15])*(x - lstItrvls[16])*(x - lstItrvls[17]) + \
		lstCoef[19]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3])*(x - lstItrvls[4])*(x - lstItrvls[5])*(x - lstItrvls[6])*(x - lstItrvls[7])*(x - lstItrvls[8])*(x - lstItrvls[9])*(x - lstItrvls[10])*(x - lstItrvls[11])*(x - lstItrvls[12])*(x - lstItrvls[13])*(x - lstItrvls[14])*(x - lstItrvls[15])*(x - lstItrvls[16])*(x - lstItrvls[17])*(x - lstItrvls[18]) + \
		lstCoef[20]*(x - lstItrvls[0])*(x - lstItrvls[1])*(x - lstItrvls[2])*(x - lstItrvls[3])*(x - lstItrvls[4])*(x - lstItrvls[5])*(x - lstItrvls[6])*(x - lstItrvls[7])*(x - lstItrvls[8])*(x - lstItrvls[9])*(x - lstItrvls[10])*(x - lstItrvls[11])*(x - lstItrvls[12])*(x - lstItrvls[13])*(x - lstItrvls[14])*(x - lstItrvls[15])*(x - lstItrvls[16])*(x - lstItrvls[17])*(x - lstItrvls[18])*(x - lstItrvls[19]))	

	return result


def main():
	fd = 'report.pdf'
	
	xDataPoints = [0.9,1.3,1.9,2.1,2.6,3.0,3.9,4.4,4.7,5.0,6.0,7.0,8.0,9.2,10.5,11.3,11.6,12.0,12.6,13.0,13.3]
	yDataPoints = [1.3,1.5,1.85,2.1,2.6,2.7,2.4,2.15,2.05,2.1,2.25,2.3,2.25,1.95,1.4,0.9,0.7,0.6,0.5,0.4,0.25]
	step = 0.02
	n = len(xDataPoints)

	print 'computing cubic spline'
	cubicSplineResult = NaturalCubicSpline(20, xDataPoints, yDataPoints)
	
	splineY = SplineFunctionYValues(cubicSplineResult,xDataPoints, step)
	splineX = []
	for i in range(0, n-1):
		for j in frange(xDataPoints[i], xDataPoints[i+1], step):
			splineX.append(j)

	print 'computing interpolating polynomial'
	polynomialResult = DividedDifferences(xDataPoints, yDataPoints)

	polyY = InterpolPolyYValues(polynomialResult, yDataPoints, xDataPoints, step)
	polyX = splineX

	print 'plotting data'
	plt.figure(1)
	# plot the data points
	plt.title('(4c) the figure from Problem 3')
	plt.plot(xDataPoints, yDataPoints, 'ro')
	# plot the cubic spline
	plt.plot(splineX, splineY)
	# plot the interpolating polynomial
	plt.plot(polyX, polyY)
	plt.axis([0, 14, -6, 4])	
	plt.savefig(fd)

	print 'plotting complete. data located in %s' % fd


if __name__ == "__main__":
	main()
