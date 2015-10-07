#Author - Bryan Connelly

# def getWorld(Filename):
# 	ret = []
# 	f = open(Filename, 'r')
# 	r = f.read()
# 	r = r.replace(' ', '')
# 	lines = r.split('\n')
# 	for line in lines:
# 		if(line != ' '):
# 			ret += [list(line)]
# 	return ret
gamma = 0.9
tiles = [[],[],[],[],[],[],[],[]]
firstPass = True
worldList = []

def getWorld(Filename):
	global tiles
	#global worldList
	m = [[],[],[],[],[],[],[],[]]
	i=0
	j=0
	with open(Filename) as f:
		for line in f:
			data = line.split()
			for num in data:
				tiles[i].append(Tile(j, i, int(num)))
				m[i].append(int(num))
				j+=1
			j=0
			i+=1

	return m

def printWorld(worldList):
	print(str(worldList[0]) + '\n' +
	str(worldList[1]) + '\n' +
	str(worldList[2]) + '\n' +
	str(worldList[3]) + '\n' +
	str(worldList[4]) + '\n' +
	str(worldList[5]) + '\n' +
	str(worldList[6]) + '\n' +
	str(worldList[7]))

class Tile:
	def __init__(self, locationx, locationy, val):
		self.locationy = locationy
		self.locationx = locationx
		self.val = val
		self.parent = None
		self.direction = None
		self.reward = 0
		self.utility = 0

		if(val == 50):
			self.utility = 50

		if(val == 0):
			self.reward = 0
		if(val == 1):
			self.reward = -1
		if(val == 3):
			self.reward = -2
		if(val == 4):
			self.reward = 1
		if(val == 50):
			self.reward = 50



def UtilCalc(worldList, tile):
	global firstPass

	if(worldList[tile.locationy][tile.locationx] == 2):
		return

	x = tile.locationx
	y = tile.locationy

	#check for walls or edges, otherwise set utility for each direction
	if(x-1 < 0):
		l_util = tile.utility
	else:
		l_util = tiles[y][x-1].utility

	if(y-1 < 0):
		u_util = tile.utility
	else:
		u_util = tiles[y-1][x].utility

	if(x+1 > 9):
		r_util = tile.utility
	else:
		r_util = tiles[y][x+1].utility

	if(y+1 > 7):
		d_util = tile.utility
	else:
		d_util = tiles[y+1][x].utility

	#calculate utilities factoring in probability
	l_util_prob = .8*l_util + .1*u_util + .1*d_util
	u_util_prob = .8*u_util + .1*l_util + .1*r_util
	r_util_prob = .8*r_util + .1*u_util + .1*d_util
	d_util_prob = .8*d_util + .1*l_util + .1*r_util

	#get maximum value
	maximum = max(l_util_prob, u_util_prob, r_util_prob, d_util_prob)

	direction = None

	#get direction of that value
	if(maximum == l_util_prob):
		direction = "left"
	elif(maximum == u_util_prob):
		direction = "up"
	elif(maximum == r_util_prob):
		direction = "right"
	elif(maximum == d_util_prob):
		direction = "down"

	oldUtil = tile.utility

	#set the utility and direction to the next tile in the path
	tile.utility = (tile.reward+(gamma*maximum))
	newUtil = tile.utility
	tile.direction = direction
	return abs(oldUtil - newUtil)

def pathGenerator(epsilon, worldList):
	delta = epsilon+1
	i = 0
	while(delta >= epsilon*(1-gamma)/gamma):
		#print("Delta: " + str(delta) + " eps, gamma, etc: " + str(epsilon*(1-gamma)/gamma))
		delta = 0
		i = 0
		for y in worldList:
			j = 9
			for x in y:
				#if we run off the end of the maze, return because we're done
				try:
					t = tiles[i][j]
				except:
					return
				nextDelta = UtilCalc(worldList, t)
				if(nextDelta > delta):
					delta = nextDelta
					#print("X: " + str(t.locationx) + " Y: " + str(t.locationy))
				j -= 1
			i += 1

def printPath(worldList):
	x = 0
	y = 7
	t = tiles[y][x]
	while(t.utility != 50):
		print("At x = " + str(x) + ", y = " + str(7-y) + ", Utility = " + str(t.utility))
		print(t.direction)
		if(t.direction == "left"):
			x -= 1
		elif(t.direction == "up"):
			y -= 1
		elif(t.direction == "right"):
			x += 1
		elif(t.direction == "down"):
			y += 1
		else:
			print("No direction")
		#print("X: " + str(x) + " Y: " + str(y))
		#check if we got to the end
		if(x == 9 and y == 0):
			print("At x = 9, y = 7, finished!")
			return
		else:
			t = tiles[y][x]
	return

def main():
	#worldFile = raw_input("Enter the name of the file to read\n")
	#store the text of the world in a 2d list
	worldList = getWorld('World1MDP.txt')
	pathGenerator(.5, worldList)
	printPath(worldList)


if __name__ == "__main__":
    main()