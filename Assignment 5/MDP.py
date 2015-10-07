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
tiles = []
firstPass = True

def getWorld(Filename):
	m = [[],[],[],[],[],[],[],[]]
	i=0
	with open(Filename) as f:
		for line in f:
			data = line.split()
			for num in data:
				m[i].append(int(num))
			i += 1
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
	def __init__(self, locationx, locationy, worldList):
		self.locationy = locationy
		self.locationx = locationx
		self.parent = None
		self.direction = None
		self.reward = 0
		self.utility = 0
		# print("x: " + str(locationx) + " y: " + str(locationy))
		# print("Type: " + str(worldList[locationy][locationx]))
		if(worldList[locationy][locationx] == 50):
			self.utility = 50

		if(worldList[locationy][locationx] == 0):
			self.reward = 0
		if(worldList[locationy][locationx] == 1):
			self.reward = -1
		if(worldList[locationy][locationx] == 3):
			self.reward = -2
		if(worldList[locationy][locationx] == 4):
			self.reward = 1
		if(worldList[locationy][locationx] == 50):
			self.reward = 50



def UtilCalc(worldList, tile):
	global firstPass

	if(worldList[tile.locationy][tile.locationx] == 2):
		return
	# if(worldList[tile.locationy][tile.locationx] == 50):
	#  	return tile.utility

	x = tile.locationx
	y = tile.locationy
	# l_util = 0
	# u_util = 0
	# r_util = 0
	# d_util = 0

	#print(str(x) + " " + str(y))

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
		try:
			r_util = tiles[y][x+1].utility
		except:
			print("Adding new tile")
			tiles[tile.locationy].append(Tile(x+1, y, worldList))
			r_util = tiles[y][x+1].utility
		#check if tile hasn't been created yet
		# if(len(tiles[tile.locationy]) <= x):
		# 	print("Adding new tile")
		# 	tiles[tile.locationy].append(Tile(x+1, y, worldList))
		# 	r_util = tiles[y][x+1].utility
		# else:
		# 	r_util = tiles[y][x+1].utility

	if(y+1 > 7):
		d_util = tile.utility
	else:
		try:
			d_util = tiles[y+1][x].utility
			print("Worked")
		except:
			print("Adding new tile")
			tiles.append([])
			tiles[tile.locationy+1].append(Tile(x, y+1, worldList))
			d_util = tiles[y+1][x].utility
		# if(len(tiles) <= y):
		# 	print("Adding new tile")
		# 	tiles.append([])
		# 	tiles[tile.locationy+1].append(Tile(x, y+1, worldList))
		# 	d_util = tiles[y+1][x].utility
		# else:
		# 	d_util = tiles[y+1][x].utility

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
	#####DEBUGGING
	#if(l_util_prob != 0.0 and u_util_prob != 0.0 and r_util_prob != 0.0 and d_util_prob != 0.0)
	print(str(l_util_prob) + " " + str(u_util_prob) + " " + str(r_util_prob) + " " + str(d_util_prob))
	#print(str(l_util) + " " + str(u_util) + " " + str(r_util) + " " + str(d_util))
	#return the next delta
	return abs(oldUtil - newUtil)

def pathGenerator(epsilon, worldList):
	delta = epsilon+1
	i = 0
	while(delta >= epsilon*(1-gamma)/gamma):
		#print("Delta: " + str(delta) + " eps, gamma, etc: " + str(epsilon*(1-gamma)/gamma))
		delta = 0
		i = 0
		for y in worldList:
			j = 0
			tiles.append([])
			for x in y:
				t = None
				#if this isn't the first pass, don't make new tile objects
				try:
					t = tiles[i][j]
				except:
				 	t = Tile(j, i, worldList)
				 	tiles[i].append(t)	

				# if(len(tiles[i]) <= j):
				# 	t = Tile(j, i, worldList)
				# 	tiles[i].append(t)
				# else:
				# 	print("Using existing tiles")
				# 	t = tiles[i][j]

				nextDelta = UtilCalc(worldList, t)
				print("X: " + str(t.locationx) + " Y: " + str(t.locationy))
				if(nextDelta > delta):
					delta = nextDelta
					#print("X: " + str(t.locationx) + " Y: " + str(t.locationy))
				j += 1
			i += 1

def printPath(worldList):
	x = 0
	y = 7
	t = tiles[y][x]
	while(t.utility != 50):
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
		print("X: " + str(x) + " Y: " + str(y))
		t = tiles[y][x]
	return

def main():
	#worldFile = raw_input("Enter the name of the file to read\n")
	#store the text of the world in a 2d list
	worldList = getWorld('World1MDP.txt')
	printWorld(worldList)
	#UtilCalc(worldList, Tile(8, 0, worldList))
	pathGenerator(.5, worldList)
	#printPath(worldList)

	# t = Tile(9, 0, worldList)
	# print(t.utility)
	# print(t.reward)

if __name__ == "__main__":
    main()