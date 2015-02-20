#
#	It is an implementation of the famous Quine-McCluskey Algorithm
#	for minimization of minterms
#	Written By:  ma_anjum95
#	Date: December 7' 2014
#

#	Returns reverse binary representation
def revBinaryRepresentation(number, maxBits):
	toReturn = []
	for i in range(0, maxBits):
		temp = number % 2
		number = number // 2
		toReturn.append(temp)

	return toReturn
	
#	Returns the revered binary array passed in as a parameter
def revBinaryArray(array):
	toReturn = []
	n = len(array)
	for i in range(0, n):
		toReturn.append(array[n-i-1])
	return toReturn

def binaryArray(value, maxBits):
	return revBinaryArray(revBinaryRepresentation(value, maxBits))

class bit:
	#	The basic element in the minterm an individual bit
	def __init__(self, value=None):	
		if value == 1 or value == 0:
			self.is_dash = False
			self.value = value
		else:
			self.is_dash = True
			self.value = -1
		
	def __str__(self):
		if not self.is_dash:
			return str(self.value)
		else:
			return '_'

	def getValue(self):
		return self.value

	def isDash(self):
		return self.is_dash

class minterm:
	#	This method makes a bit representation of the given minterm
	#	the dashes given in the sequence from the right, with first position being '0'
	#	It returns the bit representation
	def makeBitArray(self, value, maxBits, dash=None):
		toReturn = []
		binaryRep = binaryArray(value[0], maxBits)
		for i in range(0, maxBits):
			if dash and (maxBits - i - 1) in dash:
				toReturn.append(bit())
			else:
				toReturn.append(bit(binaryRep[i]))

		return toReturn

	#	Finds group of the minterm based on its number of 1s
	#	eg 0 belongs to 0 group 
	#	5 belongs to 2 group
	def findGroup(self, value, maxBits):
		temp = binaryArray(value, maxBits)
		group = 0
		for i in range(0, len(temp)):
			if temp[i] == 1:
				group += 1
		return group

	#	Here the value represents the values that made up a minterm and it should always be an array
	#	the maxBits the max number of bits to show
	#	the dash the position of dash in individual places starting 
	#	from right with 0 as the first index
	def __init__(self, value, maxBits, dash=None):
		self.value = value
		self.maxBits = maxBits
		if dash:
			self.dash = dash
		else:
			self.dash = []
		self.isPI = True
		self.group = self.findGroup(value[0], maxBits)
		self.bitArray = self.makeBitArray(value, maxBits, dash)
		
	def __str__(self):
		toReturn = ""
		toReturn += str(self.value) + " "

		for i in range(0, self.maxBits):
			toReturn += str(self.bitArray[i]) + " "
		return toReturn

	#	This methods compares the object minterm with another minterm passed in as a parameter
	#	If there is only one difference in them then a new object is created and returned else
	#	Nothing is returned
	def compare(self, toCompare):
		diffBits = [] # array of the differences
		for i in range(0, self.maxBits):
			if self.bitArray[i].getValue() != toCompare.bitArray[i].getValue():
				diffBits.append(self.maxBits - i - 1)
		
		if (len(diffBits) == 1):
			self.isPI = False
			toCompare.isPI = False
			return minterm(self.value + toCompare.value, self.maxBits, diffBits + self.dash)
		else:
			return None

	def getGroup(self):
		return self.group

	def isAPI(self):
		return self.isPI

class quineMcCluckey:
	#	Finds the maximum number of bits required to represent the largest number
	def findMaxBitLength(self, minterms):
		MAX = 0
		for i in range(0, len(minterms)):
			temp = minterms[i]
			n = 0
			while temp != 0:
				temp = temp // 2
				n += 1
			if  n > MAX:
				MAX = n
		return MAX

	#	Takes in a array of minterms and returns the object array of class 'minterm'
	def makeMintermRepresentation(self, minterms):
		toReturn = []
		maxBits = self.findMaxBitLength(minterms)
		for i in range(0, len(minterms)):
			toReturn.append(minterm([minterms[i]], maxBits))
		return toReturn

	#	Creates the columns of the Quine-McCluskey
	def makeColumns(self, minterms):
		foundPairs = True
		toReturn = []
		toReturn.append(minterms)
		column = 0
		while foundPairs:
			foundPairs = False			
			temp = []
			colLength = len(toReturn[column])
			for i in range(0, colLength):
				for j in range(i + 1, colLength):
					toAdd = toReturn[column][i].compare(toReturn[column][j])
					if toAdd:
						temp.append(toAdd)
						foundPairs = True
			column += 1
			if temp:
				toReturn.append(temp)
		return toReturn
	
	#	Make an array of the minterms in the colums which remain unchecked
	def findPIs(self, columns):
		toReturn = []
		for i in range(0, len(columns)):
			for j in range(0, len(columns[i])):
				if columns[i][j].isAPI():
					toReturn.append(columns[i][j])
		return toReturn

	#	we provide an array of minterms and the rest itself and we provide outside functionality
	#	This method does all the work inside and simply making an object of this class makes,
	#	call to all the functions to get the required result.
	#	Individual columns and minterms can the accessed by the getter methods defined at the end.
	def __init__(self, minterms):
		self.minterms = self.makeMintermRepresentation(minterms)
		self.columns = self.makeColumns(self.minterms) # the tables which will be formed later
		self.PIs = self.findPIs(self.columns) # the array of PIs

	def __str__(self):
		toReturn = ""
		toReturn += "Minterms given: \n"
		for i in range(0, len(self.minterms)):
			toReturn += str(self.minterms[i]) + "\n"
		toReturn += "\n"

		for i in range(0, len(self.columns)):
			toReturn += "Column " + str(i) + " :\n"
			for j in range(0, len(self.columns[i])):
				toReturn += str(self.columns[i][j]) + "\n"
		toReturn += "\n"

		toReturn += "Prime Implicants are:\n"
		for i in range(0, len(self.PIs)):
			toReturn += str(self.PIs[i]) + "\n"
		return toReturn

	def getMinterms(self):
		return self.minterms

	def getColumn(self):
		return self.columns

	def getPIs(self):
		return self.PIs

test = quineMcCluckey([0, 1, 2, 3, 6]) # write minterms Here

print test