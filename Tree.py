# nodes are stored in a list
# their position in the list is their address - 1
# paths on the tree go from root to leaf
# readPath and writePath use 2d lists of blocks

import random
import Util
import Block
import DBFileSys
import time

class Tree:
    def __init__(self, nodeNumber, z, segmentSize):
        self.useRAM = False
            
        if self.useRAM:
            self._buckets = [0] * nodeNumber
        
        assert (nodeNumber % 2 == 1), "tree must have odd number of buckets"
        self._size = nodeNumber
        self._z = z
        self._segmentSize = segmentSize

        self.numGrowth = 0
        self.totalTimeGrowth = 0
        
        for addr in range(1, nodeNumber + 1):
            self.writeBucket(addr, [Block.Block(0, 0, b"")] * z)
    
    def getSize(self):
        return self._size
    
    def randomLeaf(self):
        return random.randint(int(self._size / 2) + 1, self._size)
    
    def readBucket(self, bucketID):
        if self.useRAM:
            return self._buckets[bucketID - 1]
        else:
            return DBFileSys.readBucket(bucketID, self._segmentSize)
    def writeBucket(self, bucketID, blocks):
        if self.useRAM:
            if bucketID > len(self._buckets):
                self._buckets.append(blocks)
            else:
                self._buckets[bucketID - 1] = blocks
        else:
            DBFileSys.writeBucket(bucketID, blocks, self._segmentSize)
    
    def readPath(self, leaf):
        result = []
        for addr in Util.getPathNodes(leaf):
            result.append(self.readBucket(addr))
        return result
    def writePath(self, leaf, blocks):
        for addr in Util.getPathNodes(leaf):
            self.writeBucket(addr, blocks.pop(0))

    def grow(self, numLeaves):
        start = time.clock()
        for addr in range(self._size + 1, self._size + numLeaves + 1):
            self.writeBucket(addr, [Block.Block(0, 0, b"")] * self._z)
        self._size += numLeaves
        timeTaken = time.clock() - start
        self.numGrowth+=1
        self.totalTimeGrowth+=timeTaken

    def shrink(self, numLeaves):
        assert (self._size > numLeaves), "tree cannot shrink further"
        result = []
        self._size -= numLeaves
        for addr in range(self._size + 1, self._size + numLeaves + 1):
            result += self.readBucket(addr)
        return result
