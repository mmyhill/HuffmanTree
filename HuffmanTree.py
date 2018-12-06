class CompNode:
    def __init__(self, val, freq):
        self.val = val
        self.freq = freq
        self.right = None
        self.left = None
    def getFreq(self):
        return self.freq

    def changeVal(self, new):
        self.val = new

    def getVal(self):
        return self.val

    def upFreq(self):
        self.freq += 1

    def setRight(self, toAdd):
        self.right = toAdd

    def setLeft(self, toAdd):
        self.left = toAdd

    def getRight(self):
        return self.right

    def getLeft(self):
        return self.left

    #toString
    def __repr__(self):
        return "[ Val: " + str(self.val) + ", Freq: " + str(self.freq) + " ]"

class HufCompress:
    def __init__(self, str):
      self.str = str
      self.depth = 0
      self.nodes = self.count()
      self.constTree()
      self.compressLen = self.createBinFile()#returns length of compressed file
      print(self.calcCompressRate("CompressedTxt"))

    def isLeaf(self, node):#will tell if given node is leaf in tree
            return self.str.count(str(node.getVal())) > 0

    def count(self):
        nodeArr = [] #dictionary, dont have to import?
        use = self.str
        while(len(use) > 0):
            char = use[0]
            freq = use.count(str(char))
            newNode = CompNode(char, freq)
            nodeArr.append(newNode)
            use = use.replace(char, '')

        #acts as compare to
        def compNodes(node):
                return node.getFreq()

        return sorted(nodeArr, key = compNodes)

    def constTree(self):
        while(len(self.nodes) > 1):#should only have one node in list once all are made into tree
            freq = self.nodes[0].getFreq() + self.nodes[1].getFreq()
            newRoot = CompNode('*', freq)
            newRoot.setLeft(self.nodes[0])
            newRoot.setRight(self.nodes[1])
            self.nodes.pop(0)
            self.nodes.pop(0)#used to be index one, now is index zero
            self.nodes.append(newRoot)
            self.depth += 1
            print(str(self.nodes) + '\n')

            #acts as compare to
            def compNodes(node):
                    return node.getFreq()

            self.nodes = sorted(self.nodes, key = compNodes)
        print(self.__str__(self.nodes[0], depth = 0))

    #toString:
    def __str__(self, currNode, depth=0):#heavily modified code from http://krenzel.org/articles/printing-trees
        ret = ""

        # Right branch
        if currNode.getRight() != None:
            ret += self.__str__(currNode.getRight(), depth + 1)

        # Print own value
        ret += "\n" + ("    "*depth) + str(currNode.getVal()) + " " + str(currNode.getFreq())

        # Print left branch
        if currNode.getLeft() != None:
            ret += self.__str__(currNode.getLeft(), depth + 1)

        return ret

    def createBin(self, ind, possibleParent, map):#ind is ind in string, map is list of bin values detailing left or right
        #0 for taken left, 1 for taken right
        if(possibleParent.getVal() == self.str[ind]):#node has been found
            return map

        if(possibleParent.getRight() != None and possibleParent.getLeft() != None):
            return self.createBin(ind, possibleParent.getRight(), map + str('1')) + str(self.createBin(ind, possibleParent.getLeft(), map + str('0')))

        elif(possibleParent.getLeft() != None):
            return self.createBin(ind, possibleParent.getLeft(), map + str('0'))

        elif(possibleParent.getRight() != None):
            return self.createBin(ind, possibleParent.getRight(), map + str('1'))

        else:
            return ''#if reached bottom of tree and node has not been found, return blank

    def createBinFile(self):
        addLen = 0
        newFile = open("CompressedTxt.txt","w")
        for x in range (len(self.str)):
            addLen += len(self.createBin(x, self.nodes[0], ''))
            newFile.write(self.createBin(x, self.nodes[0], '') + " ")
        return addLen


    def calcCompressRate(self, fileName):
        ogBin = 8 * len(self.str) * 1.0
        return (self.compressLen/ogBin) * 100

def main():
    myStr = HufCompress(open("LoveSongOfJAlfredPrufrock.txt", 'r').read())

main()
