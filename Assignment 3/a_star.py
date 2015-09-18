import math


#record of the path
openList = list()
closedList = list()


def getWorld(Filename):
	ret = []
	f = open(Filename, 'r')
	r = f.read()
	r = r.replace(' ', '')
	lines = r.split('\n')
	for line in lines:
		if(line != ''):
			ret += [list(line)]
	return ret

def printWorld():
	print(str(worldList[0]) + '\n' +
	str(worldList[1]) + '\n' +
	str(worldList[2]) + '\n' +
	str(worldList[3]) + '\n' +
	str(worldList[4]) + '\n' +
	str(worldList[5]) + '\n' +
	str(worldList[6]) + '\n' +
	str(worldList[7]))

class Node:
	def __init__(self, locationi, locationj, distanceToStart, f):
		self.locationi = locationi
		self.locationj = locationj
		self.distanceToStart = distanceToStart
		self.f = f
		self.parent = None

	def setParent(self, parent):
		self.parent = parent

	def getF(self):
		return self.f

def addToOpenList(i, j, oldNode, h, diag, worldList):
	#if it's a wall, do nothing
	if(worldList[i][j] == '2'):
		#print('detected wall')
		return
	#determine cost of moving to new square
	dist = 10
	if(diag):
		dist += 4
	if(worldList[i][j] == '1'):
		dist += 10

	#add it to the open list if it's not closed or already there
	
	#make sure it's not on the closed list
	onClosedList = False
	for node in closedList:
		if(node.locationi == i and node.locationj == j):
			onClosedList = True
	#make sure it's not on the open list
	onOpenList = False
	for node in openList:
		if(node.locationi == i and node.locationj == j):
			onOpenList = True
			#check if this path to the node is better
			if(oldNode.f + dist + h < node.f):
				#print('improving path')
				node.f = oldNode.f + dist
				node.parent = oldNode
	#if it's not on either list, put it on openList
	if(not onOpenList and not onClosedList):
		newNode = Node(i, j, oldNode.distanceToStart + 1, oldNode.f+dist)
		newNode.parent = oldNode
		openList.append(newNode)

def printPath(node):
	currentNode = node
	print('Total path cost: ' + str(currentNode.f))
	print('column: ' + str(currentNode.locationj) + ' row: ' + str(currentNode.locationi))
	while(currentNode.parent != None):
		currentNode = currentNode.parent
		print('column: ' + str(currentNode.locationj) + ' row: ' + str(currentNode.locationi))

def aStarSearch(heuristic, worldList):
	#add start square to the open list
	startSquare = Node(len(worldList)-1, 0, 0, 0)
	openList.append(startSquare) 
	foundPath = False
	while(foundPath == False):
		#print('openList length: ' + str(len(openList)))
		#check to see if we're done, if open list is empty
		if(len(openList) == 0):
			print('No path to target')
			break
		#look for lowest F cost square on the open list, switch it to closed list
		lowestF = None
		for node in openList:
			if (lowestF == None or node.getF < lowestF.getF):
				lowestF = node
		#print('Node with lowest cost: ' + str(lowestF.f))
		#check if we're done - if the current node is the target (in top right)
		if(lowestF.locationi == 0 and lowestF.locationj == len(worldList[0])-1):
			printPath(lowestF)
			foundPath = True
			break
		#print('working with node ' + str(lowestF.locationi) + str(lowestF.locationj))
		openList.remove(lowestF)
		closedList.append(lowestF)

		#store current i and j
		i = lowestF.locationi
		j = lowestF.locationj

		#determine the heuristic value. Assumes start is bottom left and 
		h = 0
		if(heuristic == '1'):
			#manhattan distance
			h = (len(worldList[0])-1) + i - j
			h = h*10
			#print(h)
		elif(heuristic == '2'):
			#print('heuristic 2')
			h = math.sqrt(((i**2) + ((len(worldList[0])-j)**2)))
			h = h*10
			#print(h)
		else:
			print('Invalid heuristic. Enter either 1 or 2.')
		#print(h)
		#for the 8 squares around this one...
		#if there's a node above this one that's not a wall
		if(i > 0):
			addToOpenList(i-1, j, lowestF, h, False, worldList)
			
		#add up-left node to open list
		if(i > 0 and j > 0):
			addToOpenList(i-1, j-1, lowestF, h, True, worldList)

		#add left node to open list
		if(j > 0):
			addToOpenList(i, j-1, lowestF, h, False, worldList)

		#add below-left node to openList
		if(i < len(worldList)-1 and j > 0):
			addToOpenList(i+1, j-1, lowestF, h, True, worldList)

		#add below node to openList
		if(i < len(worldList)-1):
			addToOpenList(i+1, j, lowestF, h, False, worldList)

		#add below-right node to openList
		if(i < len(worldList)-1 and j < len(worldList[i])-1):
			addToOpenList(i+1, j+1, lowestF, h, True, worldList)

		#add right node to openList
		if(j < len(worldList[i])-1):
			addToOpenList(i, j+1, lowestF, h, False, worldList)

		#add right-up node to openList
		if(i > 0 and j < len(worldList[i])-1):
			addToOpenList(i-1, j+1, lowestF, h, True, worldList)


def main():
	worldFile = raw_input("Enter the name of the file to read\n")
	#store the text of the world in a 2d list
	worldList = getWorld(worldFile)
	heuristic = raw_input("Enter 1 for the Manhattan Distance heuristic or\nenter 2 for the diagonal distance heuristic\n")
	aStarSearch(heuristic, worldList)

if __name__ == "__main__":
    main()