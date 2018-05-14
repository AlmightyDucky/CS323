#!/usr/bin/python

import sys
import math

# CS 323 Assignment 2_3, Part 2: Divided Differences
#
# 4/1/18 Christopher Gonzalez

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
	result = []
	for num in range(0, n):
		result = lstFij[num][num]
		print result # uncomment to see coefficients printed out

	return result

def main():
	xData = [1, 1.01, 1.02, 1.03, 1.04, 1.05]
	yData = [1, 1.005, 1.01, 1.0149, 1.0198, 1.0247]
	DividedDifferences(xData, yData)

if __name__ == "__main__":
	main()
