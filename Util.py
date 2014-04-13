def levelNumber(leaf):          # returns the level the leaf is on (used in getMaxLevel)
    level = 0
    while leaf > 1:
        level+=1
        leaf = int (leaf / 2)
        #leaf = leaf >> 1
		# Comment: you can use right-shift (>> 1) instead of division by 2, then you can remove all the other int()
    return level

def getMaxLevel(leaf1, leaf2):
    if levelNumber(leaf1) > levelNumber(leaf2):
        leaf1/=2
    elif levelNumber(leaf1) < levelNumber(leaf2):
        leaf2/=2

    # now leaf1 and leaf2 are on the same level
    
    b = leaf1 ^ leaf2	      # bitwise difference
    diff = 0

    while b > 0:
        b = int(b / 2)
        diff+=1
    
    maxLevel = levelNumber(leaf1) - diff
	
    return maxLevel

def getPathNodes(leaf):           # returns a list of node numbers that are on the given path
    result = []
    while (leaf > 0):
        result.insert(0, leaf)
        leaf = int(leaf / 2)
    return result
