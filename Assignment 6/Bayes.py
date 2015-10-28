import getopt, sys

class Node:
	def __init__(self):
		self.type = ''
		self.conditionals = {}
		self.parents = []
		self.children = []
		self.marginal = 0

def generateNetwork():
	#create the nodes in the network
	pNode = Node()
	sNode = Node()
	cNode = Node()
	xNode = Node()
	dNode = Node()

	#set their names, parents, children, and marginal probabilities
	pNode.type = 'p'
	sNode.type = 's'
	cNode.type = 'c'
	xNode.type = 'x'
	dNode.type = 'd'

	cNode.parents.append(pNode)
	cNode.parents.append(sNode)
	xNode.parents.append(cNode)
	dNode.parents.append(cNode)

	pNode.children.append(cNode)
	sNode.children.append(cNode)
	cNode.children.append(xNode)
	cNode.children.append(dNode)

	pNode.marginal = 0.9
	sNode.marginal = 0.3

	#save the values of all the conditional probabilities
	#low polution, smoker
	cNode.conditionals['ps'] = 0.03
	#high polution, smoker
	cNode.conditionals['~ps'] = 0.05
	#low polution, not smoker
	cNode.conditionals['p~s'] = 0.001
	#high polution, not smoker
	cNode.conditionals['~p~s'] = 0.02

	#cancer
	xNode.conditionals['c'] = 0.9
	#no cancer
	xNode.conditionals['~c'] = 0.2

	#cancer
	dNode.conditionals['c'] = 0.3
	#no cancer
	dNode.conditionals['~c'] = 0.65

	#return the network as a dictionary
	net = {'Pollution': pNode, 'Smoker': sNode, 'Cancer': cNode, 'XRay': xNode, 'Dyspnoea': dNode}
	return net

#return the marginal probability of the requested node
def calcMarginal(network, arg):
	#print "Not" for ~
	if(arg[0] == '~'):
		marg = calcMarginal(network, arg[1])
		return('~' + str(marg[0]), 1 - marg[1])

	#marginals for smoker and pollution don't rely on anything else
	if(arg == 'P' or arg == 'p'):
		return('Pollution', network['Pollution'].marginal)

	elif(arg == 'S' or arg == 's'):
		return('Smoker', network['Smoker'].marginal)

	#marginal for Cancer depends on Pollution and Cancer
	elif(arg == 'C' or arg == 'c'):
		node = network['Cancer']
		conditionals = node.conditionals
		pollution = network['Pollution']
		smoker = network['Smoker']
		#marginal is sum of conditionals
		marginal = (conditionals['ps']*(1-pollution.marginal)*smoker.marginal) + (conditionals['~ps']*pollution.marginal*smoker.marginal) + (conditionals['p~s']*(1-pollution.marginal)*(1-smoker.marginal)) + (conditionals['~p~s']*pollution.marginal*(1-smoker.marginal))
		return('Cancer', marginal)

	#marginal for xray depends on cancer's marginal
	elif(arg == 'X' or arg == 'x'):
		node = network['XRay']
		conditionals = node.conditionals
		cMarginal = calcMarginal(network, 'C')
		marginal = conditionals['c']*cMarginal[1] + conditionals['~c']*(1-cMarginal[1])
		return('XRay', marginal)

	#marginal for dyspnoea depends on cancer's marginal
	elif(arg == 'D' or arg == 'd'):
		node = network['Dyspnoea']
		conditionals = node.conditionals
		cMarginal = calcMarginal(network, 'C')
		marginal = conditionals['c']*cMarginal[1] + conditionals['~c']*(1-cMarginal[1])
		return('Dyspnoea', marginal)
	else:
		print('Unknown argument, cannot compute marginal')

def calcJointDist(network, arg):
	probs = {}
	for var in arg:
		probs[var] = calcJointProb(network, var)
	return probs

def calcJointProb(network, arg):
	prob = 1
	length = len(arg)
	i = 0
	while(i < length):
		if arg[i] == '~':
			i += 1
			newArg = '~' + arg[i]
			prob = prob * calcCond(network, newArg, arg[i+1:])[1]
		else:
			prob = prob * calcCond(network, arg[i], arg[i+1:])[1]
		i += 1
	return prob

def calcCond(network, arg, cond):
	#variable used to remember if "~" was used
	probNot = False
	if(arg[0] == '~'):
		probNot = True
		#adjust the argument so that it excludes the ~ symbol
		arg = arg[1]

	node = None

	#set the node based on the arg
	if(arg == 's' or arg == 'S'):
		node = network['Smoker']
	elif(arg == 'p' or arg == 'P'):
		node = network['Pollution']
	elif(arg == 'c' or arg == 'C'):
		node = network['Cancer']
	elif(arg == 'd' or arg == 'D'):
		node = network['Dyspnoea']
	elif(arg == 'x' or arg == 'X'):
		node = network['XRay']
	else:
		print('Unknown argument, cannot compute conditional')
		return(None, None)

	#set to -1 so we can detect if it never gets assigned
	conditional = -1
	if(len(cond) == 0):
		conditional = calcMarginal(network, arg)[1]
	elif(cond in node.conditionals):
		conditional = node.conditionals[cond]
	#if "conditional" never got assigned, there's no data about the 
	#probability of the event given the condition
	if(conditional == -1):
		print("No value for that condition on that variable")
		return (None, None)
	if(probNot):
		return (node.type, (1-conditional))
	else:
		return (node.type, conditional)

#sets the marginal probability of Pollution or Smoker
def setPrior(network, arg, val):
	if(arg == 's' or arg == 'S'):
		node = network['Smoker']
		node.marginal = val
	elif arg == 'p' or arg == 'P':
		node = network['Pollution']
		node.marginal = val
	else:
		print('Cannot set the prior for this variable')

def main():
    net = generateNetwork()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        sys.exit(2)
    for o, a in opts:
		if o in ("-p"):
			# print "flag", o
			# print "args", a
			# print a[0]
			# print float(a[1:])
			#setting the prior here works if the Bayes net is already built
			setPrior(net, a[0], float(a[1:]))
		elif o in ("-m"):
			# print "flag", o
			# print "args", a
			# print type(a)
			marginal = calcMarginal(net, a)
			print('Marginal Probability of ' + str(marginal[0]) + ': ' + str(marginal[1]))
			#calcMarginal(a)
		elif o in ("-g"):
			# print "flag", o
			# print "args", a
			# print type(a)
			# '''you may want to parse a here and pass the left of |
			# and right of | as arguments to calcConditional
			# '''
			p = a.find("|")
			# print a[:p]
			# print a[p+1:]
			conditional = calcCond(net, a[:p], a[p+1:])
			#make sure the return was valid
			if(conditional == (None, None)):
				continue
			print(str(conditional[0]) + ' conditional probability: ' + str(conditional[1]))
			#calcCond(a[:p], a[p+1:])
		elif o in ("-j"):
			# print "flag", o
			# print "args", a
			joint = calcJointDist(net, a)
			print(joint)
		else:
			assert False, "unhandled option"



if __name__ == "__main__":
    main()