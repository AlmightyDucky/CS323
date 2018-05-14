#!/usr/bin/python

import sys
import math

# CS 323 Assignment 1, Part 2: Rootfinding Functions
#
# 1/28/18 Christopher Gonzalez

# the function used in the methods (hardcoded in since it was allowed)
# to switch functions, type in the correct number for the function you
# want to use in the arguments
# 1 --> e^2 - sin(x) - 2
# 2 --> x^2 -4x + 4 - ln(x)
def func(x, fNum):
	if (fNum == 1):
		return math.exp(x) - math.sin(x) - 2
	elif (fNum == 2):
		return math.pow(x,2) - 4*x + 4 - math.log(x)
	else:
		print 'Invalid function number.'
		sys.exit()

# the derivative of the function used in the newton method
# the correct function is chosen based on the function
# number received
def funcDr(x, fNum):
	if (fNum == 1):
		return math.exp(x) - math.cos(x)
	elif (fNum == 2):
		return 2 * x - 4 - (1/float(x))
	else:
		print 'Invalid function derivative number.'
		sys.exit()

# a root finding method that works by using secant lines in order
# to converge to a root
# returns the root found by the methof
def secantMethod(x0, x1, errorTol, iters, funcNum):
	# 1) calculate x2 = x1 - (x0 - x1) * f(x1) / (f(x0) - f(x1))
	# 2) while the absolute value of x2 - x1 is greater than the
	#    error tolerance, set x0 = x1, x1 = x2 and calculate x2 again
	# 3) if the previous step is false, return x2

	maxIteration = iters
	x2 = x1 - ((x0 - x1) * func(x1, funcNum)) / (func(x0, funcNum) - func(x1, funcNum))

	for i in range(0, maxIteration):
		if (abs(x2 - x1) > errorTol):
			print 'x0 = %.11f, x1 = %.11f, x2 = %.11f' % (x0, x1, x2)
			x0 = x1
			x1 = x2
			x2 = x1 - ((x0 - x1) * func(x1, funcNum)) / (func(x0, funcNum) - func(x1, funcNum))
		else:
			break
	print 'Stopped after %d iterations.' % (i + 1)
	return x2

# a root finding method that works by using the tangent line of
# a function to converge to a root
# returns the root found by the method
def newtonMethod(x0, errorTol, iters, funcNum):
	# 1) calculate F(x0)
	# 2) for the number of iterations check if F(xn) is less than
	#    the error tolerance; break out of loop early if true
	# 3) if previous step is false, calculate f'(xn) and set
	#    xn = xn - f(xn)/f'(xn) and repeat 2)
	# 4) return xn

	maxIteration = iters
	xn = x0
	fResult = func(xn, funcNum)
	
	for i in range(0, maxIteration):
		if (abs(fResult) > errorTol):
			fPrimeResult = funcDr(xn, funcNum)
			print "Xn = %.11f, f(Xn) = %.11f, f'(Xn) = %.11f," % (xn, fResult, fPrimeResult), 
			xn = xn - (fResult/fPrimeResult)
			print "Xn - (f(Xn)/f'(Xn) = %.11f" % (xn)
			fResult = func(xn, funcNum)
		else:
			break
	print 'Stopped after %d iterations.' % (i + 1)
	return xn

# a root finding method that works by dividing an interval until
# you converge to a root
# returns the root found by the method
def bisectionMethod(a, b, errorTol, iters, funcNum):
	# 1) c = (a + b) / 2
	# 2) for the number of iterations check if b-c is less than/equal 
	#    to error tolerance; break out of loop early if true
	# 3) if previous step is false, determine which part of interval
	#    to swap with c by the sign of f(b) * f(c), calculate c
	#    again and repeat 2)
	# 4) return c

	maxIteration = iters
	c = (a + b) / 2.0
		
	for i in range(0, maxIteration):
		print 'A = %.11f, B = %.11f, C = %.11f, B-C = %.11f, E = %.11f' % (a, b, c, b-c, errorTol)
		if ((b - c) > errorTol):
			if (func(b, funcNum) * func(c, funcNum) <= 0):
				a = c
			elif (func(b, funcNum) * func(c, funcNum) > 0):
				b = c
		else:
			break
		c = (a + b) / 2.0
	print 'Stopped after %d iterations.' % (i + 1)
	return c

# a program that showcases three different rootfinding methods:
# Bisection, Newton and Secant methods
# a user can enter in which method they want to use and the required
# arguments in order to find a root for a hardcoded function
def main(argv):
	# error checks to determine if the user entered in the correct
	# arguments for the method they want to use
	if (len(sys.argv) != 6 and len(sys.argv) != 7):
		argError(1)
		sys.exit()

	if (sys.argv[1] == 'bisection' and len(sys.argv) != 7):
		argError(2)
		sys.exit()
	elif (sys.argv[1] == 'newton' and len(sys.argv) != 6):
		argError(3)
		sys.exit()
	elif (sys.argv[1] == 'secant' and len(sys.argv) != 7):
		argError(4)
		sys.exit()
	
	root = 0.0

	if (sys.argv[1] == 'bisection'):
		# check if interval changes sign
		if ((func(float(sys.argv[2]), 1) >= 0 and func(float(sys.argv[3]), 1) <= 0)
			or (func(float(sys.argv[2]), 1) <= 0 and func(float(sys.argv[3]), 1) >= 0)):
			root = bisectionMethod(float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
		else:
			print 'The interval [%s,%s] does not change sign. Cannot approximate a root.' % (sys.argv[2],sys.argv[3])
			sys.exit()
	elif (sys.argv[1] == 'newton'):
		root = newtonMethod(float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
	elif (sys.argv[1] == 'secant'):
		root = secantMethod(float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
	else:
		argError(1)
		sys.exit()

	funcStr = ''
	if (sys.argv[1] != 'newton'):
		if (int(sys.argv[6]) == 1):
			funcStr = 'e^x - sin(x) - 2'
		elif (int(sys.argv[6]) == 2):
			funcStr = 'x^2 -4x + 4 - ln(x)'
	else:
		if (int(sys.argv[5]) == 1):
			funcStr = 'e^x - sin(x) - 2'
		elif (int(sys.argv[5]) == 2):
			funcStr = 'x^2 -4x + 4 - ln(x)'

	print 'The root of the function %s with the %s method is %.11f' % (funcStr, sys.argv[1], root)

# tells the user the correct way to enter in the arguments
def argError(code):
	use1 = 'Usage1: python Assign1P2 bisection <a> <b> <error_tolerance> <max_iterations> <function_number>'
	use2 = 'Usage2: python Assign1P2 newton <x0> <error_tolerance> <max_iterations> <function_number>'
	use3 = 'Usage3: python Assign1P2 secant <point1> <point2> <error_tolerance> <max_iterations> <function_number>'

	if (code == 1):
		print use1
		print use2
		print use3
	elif (code == 2):
		print use1
	elif (code == 3):
		print use2
	elif (code == 4):
		print use3

if __name__ == "__main__":
	main(sys.argv[1:])

