class HanoiTowerSolver:
	def __init__(self, numRods, initialState, destinationState):
		self.visitedStates = set()
		self.initialState = initialState
		self.destinationState = destinationState
		self.numRods = numRods
		self.queue = [(initialState, 0)]

	def getMinSteps(self):
		while len(self.queue) > 0:
			(currentState, minStep) = self.queue.pop(0)
			print(currentState)
			print(minStep)

			if currentState[0] == 0:
				self.visitedStates = set()
				destList = list(self.destinationState)
				destList.pop(0)
				self.destinationState = tuple(destList)
				initList = list(currentState)
				initList.pop(0)
				self.initialState = tuple(initList)
				self.queue = [(self.initialState, minStep)]
				return self.getMinSteps()

			states = self.getAllPosibleNextStates(currentState)
			for state in states:
				if state == self.destinationState:
					return minStep + 1
				equivalentStates = self.getEquivalentStates(state, 0)
				isStateVisited = False
				for equivalentState in equivalentStates:
					if equivalentState in self.visitedStates:
						isStateVisited = True
						break
				if isStateVisited:
					continue
				self.queue.append((state, minStep + 1))
			self.visitedStates.add(currentState)

	def getAllPosibleNextStates(self, currentState):
		movableDiskIndice = self.getMovableDiskIndice(currentState)
		emptyRods = self.getEmptyRods(currentState)
		allPosibleNextStates = set()

		for movableDiskIndex in movableDiskIndice:
			for emptyRod in emptyRods:
				lst = list(currentState)
				lst[movableDiskIndex] = emptyRod
				allPosibleNextStates.add(tuple(lst))

		for movableDiskIndex in movableDiskIndice:
			for i in range(0, movableDiskIndex):
				if i in movableDiskIndice:
					lst = list(currentState)
					lst[movableDiskIndex] = currentState[i]
					allPosibleNextStates.add(tuple(lst))

		return allPosibleNextStates

	def getMovableDiskIndice(self, currentState):
		movableDiskIndice = set()
		length = len(currentState)
		for i in range(0, length):
			if i == length - 1:
				movableDiskIndice.add(i)
				continue
			isMovable = True
			for j in range(i+1, length):
				if currentState[i] == currentState[j]:
					isMovable = False
					break
			if isMovable:
				movableDiskIndice.add(i)
		return movableDiskIndice

	def getEmptyRods(self, currentState):
		emptyRods = set()
		for i in range(0, self.numRods):
			emptyRods.add(i)
		for i in range(0, len(currentState)):
			emptyRods.discard(currentState[i])
		return emptyRods

	def getEquivalentStates(self, currentState, lastUnchangableRod):
		equivalentStates = set()
		equivalentStates.add(currentState)
		if lastUnchangableRod >= self.numRods - 2:
			return equivalentStates
		for i in range(lastUnchangableRod+2, self.numRods):
			state = list(currentState)
			for j in range(0, len(currentState)):
				if state[j] == lastUnchangableRod+1:
					state[j] = i
				elif state[j] == i:
					state[j] = lastUnchangableRod+1
			equivalentStates.update(self.getEquivalentStates(tuple(state), lastUnchangableRod+1))
		return equivalentStates

if __name__== "__main__":
	solver = HanoiTowerSolver(4, (0,1,1,0), (0,0,0,0))
	# solver = HanoiTowerSolver(3, (1,2,0,1,1,0,2,2,1,1), (0,0,0,0,0,0,0,0,0,0))
	# solver = HanoiTowerSolver(4, (1,2,0,1,3,0,3,2,1,1,0,3,2), (0,0,0,0,0,0,0,0,0,0,0,0,0))
	# solver = HanoiTowerSolver(3, (1,2,0,1,1,0,2,2,1,1,2,1,1,0,2), (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))
	# solver = HanoiTowerSolver(4, (1,2,0,1,3,0,3,2,1,1,0,3,2,2), (0,0,0,0,0,0,0,0,0,0,0,0,0,0))
	result = solver.getMinSteps()
	print(result)
	f = open("hanoi_result.txt", "w")
	f.write(str(result))
	f.close()
