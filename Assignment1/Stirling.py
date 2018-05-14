#!/usr/bin/python

import sys
import math

# CS 323 Assignment 1, Part 1: Stirling's Approximation
#
# 1/28/18 Christopher Gonzalez

def main():
	print "CS 323 Assignment Part 1: Stirling's Approximation."
	print "Number | Factorial |      Stirling     |   Absolute   |   Relative"

	# n = 1, 2, ... 10 as stated in the assignment
	start = 0
	end = 10

	# first calculate the Stirling Aprroximation
	# then calculate the absoulte and relative errors
	# print out the result in a decently formatted table
	for num in range (start, end + 1):
		result = StirlingApproximation(num)
		absError = AbsoluteError(math.factorial(num), float(result))
		relError = RelativeError(math.factorial(num), float(result))

		print '{0:5d} {1:11d} {2:16.6f} {3:16.6f} {4:14.6f}'.format(num, math.factorial(num), result, absError, relError)

# calculate sqrt(2 * pi * n) * (n / e) ^ n and result the result as a float
def StirlingApproximation(n):
	return float(math.sqrt(2 * math.pi * n) * math.pow((n / math.e),n))

# calculate the relative error by calculating the absolute error divided by
# Xt, the expected value and return the result
def RelativeError(Xt, Xa):
	return AbsoluteError(Xt, Xa) / float(abs(Xt))

# calculate the expected value, Xt, and the value received from the Stirling
# Approximation, Xa, and return the absolute value of the result
def AbsoluteError(Xt, Xa):
	return abs(Xt - Xa)

if __name__ == "__main__":
	main()
