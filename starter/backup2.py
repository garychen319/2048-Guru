from random import randint
from BaseAI import BaseAI
import sys
import time
import math



class PlayerAI(BaseAI):

	def getMove(self, grid):

		nextstate = PlayerAI.decision(grid)
		#convert from nextstate to move direction number
		dirs = [UP, DOWN, LEFT, RIGHT] = range(4)
		direction = -1
		availableMoves = [0,1,2,3]

		for movenum in availableMoves:
			gridclone = grid.clone()
			gridclone.move(movenum)
			same = 1
			for i in range (0,4):
				for j in range (0,4):
					if (gridclone.map[i][j] != nextstate.map[i][j]):
						same = 0
			if same == 1:
				direction = movenum

		#refers to grid below
		"""
		print("Utility: ", PlayerAI.getUtility(nextstate)[0])
		print("largest_in_corner: ", PlayerAI.getUtility(nextstate)[1])
		print("fsAdjacent: ", PlayerAI.getUtility(nextstate)[2])
		print("largeEdge: ", PlayerAI.getUtility(nextstate)[3])
		print("cascading: ", PlayerAI.getUtility(nextstate)[4])
		print("openSquares: ", PlayerAI.getUtility(nextstate)[5])
		print("rank: ", PlayerAI.getUtility(nextstate)[6])
		print("adjValInv: ", PlayerAI.getUtility(nextstate)[7])
		
		print("Utility: ", PlayerAI.getUtility(nextstate)[0])
		print("cornerLargest: ", PlayerAI.getUtility(nextstate)[1])
		print("topEdgeCascading: ", PlayerAI.getUtility(nextstate)[2])
		print("openSquares: ", PlayerAI.getUtility(nextstate)[3])
		print("secondIsLargest: ", PlayerAI.getUtility(nextstate)[4])
		print("thirdIsLargest: ", PlayerAI.getUtility(nextstate)[5])
		print("fourthIsLargest: ", PlayerAI.getUtility(nextstate)[6])
		print("sumAdjVal: ", PlayerAI.getUtility(nextstate)[7])
		print("diff0_1: ", PlayerAI.getUtility(nextstate)[8])
		print("diff1_2: ", PlayerAI.getUtility(nextstate)[9])
		print("diff2_3: ", PlayerAI.getUtility(nextstate)[10])
		"""

		print("Utility: ", PlayerAI.getUtility(nextstate)[0])
		print("Weight: ", PlayerAI.getUtility(nextstate)[1])
		print("AdjDiff: ", PlayerAI.getUtility(nextstate)[2])

		

		return direction	


	def decision(grid):
		
		timeout = time.time() + 0.19
		alpha = -sys.maxsize
		beta = sys.maxsize
		"""
		initialDepth = 4
		return PlayerAI.maximize(grid, timeout, alpha, beta, initialDepth)[0]
		"""
		
		initialDepth = 2
		prevState = None
		while time.time() < timeout:
			initialDepth += 1
			currState = PlayerAI.maximize(grid, timeout, alpha, beta, initialDepth)
			if(currState[0] != None):
				prevState = currState[0]
		
		return prevState
		


	def minimize(grid, timeout, alpha, beta, depth):
		if time.time() > timeout:
			return (None, None)
 
		depth -= 1
		if depth <= 0: #stop (terminal test)
			return (None, PlayerAI.getUtility(grid)[0])

		minC = None
		minU = sys.maxsize

		for movenum in grid.getAvailableMoves():
			child = grid.clone()
			child.move(movenum)
			util = PlayerAI.maximize(child, timeout, alpha, beta, depth)[1]

			if util < minU:
				minC = child
				minU = util

			if minU <= alpha:
				break
			if minU < beta:
				beta = minU

		return (minC, minU)


	def maximize(grid, timeout, alpha, beta, depth):
		if time.time() > timeout:
			return (None, None)

		depth -= 1
		if depth <= 0: #stop (terminal test)
			return (None, PlayerAI.getUtility(grid)[0])

		maxC = None
		maxU = -sys.maxsize

		for movenum in grid.getAvailableMoves():
			child = grid.clone()
			child.move(movenum)

			util = PlayerAI.minimize(child, timeout, alpha, beta, depth)[1]

			if util > maxU:
				maxC = child
				maxU = util

			if maxU >= beta:
				break
			if maxU > alpha:
				alpha = maxU

		return (maxC, maxU)


	def getUtility(grid):

		"""
		largest_in_corner = 0
		cascading = 0 
		openSquares = 0
		fsAdjacent = 0
		cornervals = [grid.map[0][0], grid.map[0][3], grid.map[3][0], grid.map[3][3]]


		#whether largest val in corner
		largest_in_corner = PlayerAI.largestInCorner(grid)

		if largest_in_corner:
			#find largest corner
			mcIndex = PlayerAI.findLargestCorner(grid)[0]
			mcVal = cornervals[mcIndex]

			#check if cascading
			cascading = 0
			if mcIndex != -1:
				if mcIndex == 0:
					if PlayerAI.topIsCascading(grid) or PlayerAI.leftIsCascading(grid):
						cascading = 1
				if mcIndex == 1:
					if PlayerAI.topIsCascading(grid) or PlayerAI.rightIsCascading(grid):
						cascading = 1
				if mcIndex == 2:
					if PlayerAI.botIsCascading(grid) or PlayerAI.leftIsCascading(grid):
						cascading = 1
				if mcIndex == 3:
					if PlayerAI.botIsCascading(grid) or PlayerAI.rightIsCascading(grid):
						cascading = 1

			#check if value next to corner is 2nd largest
			fsAdjacent = PlayerAI.firstSecondAdjacent(grid)
		
		#count open squares
		openSquares = PlayerAI.openSquares(grid)

		#edge greater than all other squares combined
		largeEdge = PlayerAI.largeEdge(grid)

		#rank = largest log base 2 (largest num)
		rank = PlayerAI.findRank(grid)

		#adjValInv = inverse of difference between adjance squares
		adjValInv = (PlayerAI.adjacentDifference(grid)+1) 

		#utility = 63*grid.map[0][0] + 31*grid.map[0][1] + 15*grid.map[0][2] + 7*grid.map[0][3] + 3*grid.map[1][3] + grid.map[1][2]
		largest_in_corner = 7 * largest_in_corner
		fsAdjacent = 3 * fsAdjacent * pow(1.3, rank)
		largeEdge = 6 * largeEdge
		cascading = 2 * (cascading * pow(1.3, rank))
		openSquares =  (openSquares * 2)
		adjValInv = (10/adjValInv) * pow(1.5, rank)

		#utility = largest_in_corner + fsAdjacent + largeEdge + cascading + openSquares + adjValInv
		#return (utility, largest_in_corner, fsAdjacent, largeEdge, cascading, openSquares, rank, adjValInv)

		"""
		"""
		#Initialization
		cornerLargest = 0
		topEdgeCascading = 0
		openSquares = 0
		secondIsLargest = 0
		thirdIsLargest = 0
		fourthIsLargest = 0
		sumAdjVal = 0
		rank = 0


		#Declarations
		cornerLargest = PlayerAI.topLeftLargest(grid)
		topEdgeCascading = PlayerAI.topEdgeCascading(grid)
		openSquares = PlayerAI.openSquares(grid)
		secondIsLargest = PlayerAI.largerThan3Rows(grid, grid.map[0][1])
		thirdIsLargest = PlayerAI.largerThan3Rows(grid, grid.map[0][2])
		fourthIsLargest = PlayerAI.largerThan3Rows(grid, grid.map[0][3])
		sumAdjVal = (PlayerAI.adjacentDifference(grid)+1)
		rank = PlayerAI.findRank(grid)
		diff0_1 = abs(grid.map[0][0] - grid.map[0][1])
		diff1_2 = abs(grid.map[0][1] - grid.map[0][2])
		diff2_3 = abs(grid.map[0][2] - grid.map[0][3])

		

		#Weights
		cornerLargest = 200 * cornerLargest
		topEdgeCascading = 200 * topEdgeCascading
		openSquares = 1 * openSquares
		secondIsLargest = 5 * secondIsLargest
		thirdIsLargest = 3 * thirdIsLargest
		fourthIsLargest = 1 * fourthIsLargest
		sumAdjVal = math.log(sumAdjVal, 2) / pow(2, rank)

		
		#if diff0_1 != 0:
		#	diff0_1 = math.log(diff0_1, 2)
		#if diff1_2 != 0:
		#	diff1_2 = math.log(diff1_2, 2)
		#if diff2_3 != 0:
		#	diff2_3 = math.log(diff2_3, 2)
		
		

		utility =  (cornerLargest + topEdgeCascading + openSquares + secondIsLargest 
		+ thirdIsLargest + fourthIsLargest - sumAdjVal - diff0_1 - diff1_2 - diff2_3)
		return (utility, cornerLargest, topEdgeCascading, openSquares, secondIsLargest,
			thirdIsLargest, fourthIsLargest, sumAdjVal, diff0_1, diff1_2, diff2_3)
		"""

		openSpaces = len(grid.getAvailableCells())
		weight = PlayerAI.weightScore(grid)
		adjDiff = PlayerAI.adjacentDifference(grid)
		utility = weight-adjDiff + openSpaces
		return (utility, weight, adjDiff)


		


	def weightScore(grid):
		score = 0
		score += 6 * grid.map[0][0]
		score += 5 * grid.map[0][1]
		score += 4 * grid.map[0][2]
		score += 3 * grid.map[0][3]

		score += 5 * grid.map[1][0]
		score += 4 * grid.map[1][1]
		score += 3 * grid.map[1][2]
		score += 2 * grid.map[1][3]

		score += 4 * grid.map[2][0]
		score += 3 * grid.map[2][1]
		score += 2 * grid.map[2][2]
		score += 1 * grid.map[2][3]

		score += 3 * grid.map[3][0]
		score += 2 * grid.map[3][1]
		score += 1 * grid.map[3][2]
		score += 0 * grid.map[3][3]
		return score


	def topLeftLargest(grid):
		largest = -1
		gridclone = grid.clone()
		gridclone.map[0][0] = 0
		for i in range (0,4):
			for j in range (0,4):
				if gridclone.map[i][j] > largest:
					largest = gridclone.map[i][j]

		if grid.map[0][0] > largest:
			return 1
		return 0


	def topEdgeCascading(grid):
		if PlayerAI.topLeftLargest(grid):
			if grid.map[0][0] >= grid.map[0][1] >= grid.map[0][2] >= grid.map[0][3]:
				if grid.map[0][0] != 0 and grid.map[0][3] != 0:
					return 1
		return 0

	def largerThan3Rows(grid, val):
		largest = 1
		for i in range (1,4):
			for j in range (0,4):
				if  val < grid.map[i][j]:
					largest = 0
		return largest



	def adjacentDifference(grid):
		diff_value = 0
		for i in range(0,3):
			for j in range(0,4):
				diff_value += abs(grid.map[i+1][j] - grid.map[i][j])
		for i in range (0,4):
			for j in range (0,3):
				diff_value += abs(grid.map[i][j+1] - grid.map[i][j])
		return diff_value

	#fix
	def firstSecondAdjacent(grid):
		cornervals = [grid.map[0][0], grid.map[0][3], grid.map[3][0], grid.map[3][3]]
		index = PlayerAI.findLargestCorner(grid)[0]
		largestVal = PlayerAI.findLargestCorner(grid)[1]

		if index != -1:
			gridclone = grid.clone()
			if(index == 0):
				gridclone.map[0][0] = 0
				if PlayerAI.isLargestEq(grid, gridclone.map[0][1]) or PlayerAI.isLargest(grid, gridclone.map[1][0]):
					return 1
			if(index == 1):
				gridclone.map[0][3] = 0
				if PlayerAI.isLargestEq(grid, gridclone.map[0][2]) or PlayerAI.isLargest(grid, gridclone.map[1][3]):
					return 1
			if(index == 2):
				gridclone.map[3][0] = 0
				if PlayerAI.isLargestEq(grid, gridclone.map[2][0]) or PlayerAI.isLargest(grid, gridclone.map[3][1]):
					return 1
			if(index == 3):
				gridclone.map[3][3] = 0
				if PlayerAI.isLargestEq(grid, gridclone.map[3][2]) or PlayerAI.isLargest(grid, gridclone.map[2][3]):
					return 1
		return 0
	
	#fix
	def largeEdge(grid):
		topMax = max(grid.map[0][0], grid.map[0][1], grid.map[0][2], grid.map[0][3]) 
		leftMax = max(grid.map[0][0], grid.map[1][0], grid.map[2][0], grid.map[3][0])
		rightMax = max(grid.map[0][3], grid.map[1][3], grid.map[2][3], grid.map[3][3])
		botMax = max(grid.map[3][0], grid.map[3][1], grid.map[3][2], grid.map[3][3])
		
		oneEdgeIsLargest = 1
		for i in range(1, 3):
			for j in range (0, 4):
				if topMax < grid.map[i][j]:
					oneEdgeIsLargest = 0
		for i in range(0, 4):
			for j in range (1, 4):
				if leftMax < grid.map[i][j]:
					oneEdgeIsLargest = 0
		for i in range(0, 4):
			for j in range (0, 3):
				if rightMax < grid.map[i][j]:
					oneEdgeIsLargest = 0
		for i in range(0, 3):
			for j in range (0, 4):
				if botMax < grid.map[i][j]:
					oneEdgeIsLargest = 0
		return oneEdgeIsLargest


	def findRank(grid):
		largest = 0
		for row in grid.map:
			for num in row:
				if num > largest:
					largest = num
		return math.log(largest, 2)

	def isLargest(grid, val):
		largest = 1
		for row in grid.map:
			for num in row:
				if val < num:
					largest = 0
		return largest

	def isLargestEq(grid, val):
		largest = 1
		for row in grid.map:
			for num in row:
				if val < num:
					largest = 0
		return largest


	def largestInCorner(grid): #returns 1/0 if largest val in corner
		cornervals = [grid.map[0][0], grid.map[0][3], grid.map[3][0], grid.map[3][3]]
		for val in cornervals:
			largest_test = 1
			for row in grid.map:
				for num in row:
					if val < num:
						largest_test = 0
			if largest_test:
				return 1
		return 0

	def findLargestCorner(grid):
		maxindex = -1
		maxCornerVal = -1
		cornervals = [grid.map[0][0], grid.map[0][3], grid.map[3][0], grid.map[3][3]]

		if(cornervals[0] == cornervals[1] and cornervals[1] == cornervals[2]
			and cornervals[2] == cornervals[3]): #all equal
			return -1

		for i in range (0,4):
			val = cornervals[i]
			if val > maxCornerVal:
				maxindex = i
				maxCornerVal = val
		return (maxindex, maxCornerVal)

				
		#not cascading
	def topIsCascading(grid): #returns 1/0 if edge is cascading
		if PlayerAI.orderTest(grid.map[0][0], grid.map[0][1], grid.map[0][2], grid.map[0][3]):
			return 1
		return 0
	def leftIsCascading(grid):
		if PlayerAI.orderTest(grid.map[0][0], grid.map[1][0], grid.map[2][0], grid.map[3][0]):
			return 1
		return 0
	def botIsCascading(grid):
		if PlayerAI.orderTest(grid.map[3][3], grid.map[3][2], grid.map[3][1], grid.map[3][0]):
			return 1
		return 0
	def rightIsCascading(grid):
		if PlayerAI.orderTest(grid.map[3][3], grid.map[2][3], grid.map[1][3], grid.map[0][3]):
			return 1
		return 0

	def orderTest(a, b, c, d):
		if(a >= b >= c >= d and (a != 0 and d != 0)):
			return 1
		elif(a <= b <= c <= d and (a != 0 and d != 0)):
			return 1
		else:
			return 0


	def openSquares(grid): #returns # of open squares
		openSquares = 0
		for row in grid.map:
			for num in row:
				if num == 0:
					openSquares += 1
		return openSquares

