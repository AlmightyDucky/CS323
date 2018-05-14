#!/usr/bin/python

import sys
import math

# CS 323 Assignment 2_3, Part 1: Natural Cubic Spline
#
# 4/1/18 Christopher Gonzalez

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
		print result[j] # unqoute to see coefficients printed out
	
	return result

def main():
	n = 6
	xData = [-3, -2, 1, 3, 5, 6, 9]
	yData = [-4, 3, -1, 1, -2, 2, -3]
	NaturalCubicSpline(n, xData, yData)

if __name__ == "__main__":
	main()
