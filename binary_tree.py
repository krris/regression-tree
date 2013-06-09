#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import random
import copy

''' Data connected with every node
TODO: change maxint/minint to valid max/min value taken from datasource file'''
class NodeData:
    param = None
    value = 0
    ranges = None

    def __init__(self, param_no):
        self.ranges = [] 
        for i in range(param_no):
            self.ranges.append({'minValue': -sys.maxint - 1, 'maxValue': sys.maxint})
            
''' Node of a tree '''    
class Node:
    left, right, parent, data = None, None, None, None

    def __init__(self, data):
        self.left = None
        self.right = None
        self.parent = None
        self.data = data

''' A binary tree '''
class BinaryTree:
    
    ''' Constructs empty binary tree 
    @param param_no number of parameters in the datasource '''
    def __init__(self, param_no):
        self.root = Node(None)
        self.root.parent = None
        self.leaves = [self.root]
        self.param_no = param_no

    ''' Inserts random node choosing random parameter with a random range '''
    def insertRandom(self):
        # leaf chosen to turn into a node
        xNode = self.leaves[random.randint(0, len(self.leaves) - 1)]
        
        xNodeData = NodeData(self.param_no)
        # copying ranges list from the parent if it's not root
        if xNode.parent:
            xNodeData.ranges = copy.deepcopy(xNode.parent.data.ranges)
            xNode.data = xNodeData
            # ranges list is updated basing on the parent parameter value
            self.updateRanges(xNode)
        else:
            xNode.data = xNodeData
        
        # parameter chosen to be changed
        randParam = random.randint(0, self.param_no - 1)
        # value of the chosen parameter
        randValue = random.uniform(
                                   xNode.data.ranges[randParam]['minValue'], 
                                   xNode.data.ranges[randParam]['maxValue'])
            
        # filling node data for a new node
        xNodeData.param = randParam
        xNodeData.value = randValue

        # creating new leaves
        xNode.left = Node(None)
        xNode.right = Node(None)
        xNode.left.parent = xNode
        xNode.right.parent = xNode
        self.leaves.append(xNode.left)
        self.leaves.append(xNode.right)
        # xNode is not a leaf anymore
        self.leaves.remove(xNode)

    ''' Updates ranges list of a node basing on its parent 
    @param node must not be None! '''
    def updateRanges(self, node):
        
        parentNode = node.parent
        parentValue = parentNode.data.value
        parentParam = parentNode.data.param
        ranges = node.data.ranges
        
        # check if node is left or right son
        if node == parentNode.left:
            ranges[parentParam]['maxValue'] = parentValue
        else:
            ranges[parentParam]['minValue'] = parentValue
       
    ''' Removes random node
        Only leaf parent or root can be removed. '''
    def removeRandom(self):
        # len(leaves) == 1 means tree is empty 
        if len(self.leaves) == 1:
            return
        
        # list of candidates to remove
        # we can remove only nodes which two sons are leaves
        nodes = []
        for leaf in self.leaves:
            
            if leaf.parent.right.data == None and leaf.parent.left.data == None:
                if nodes.count(leaf.parent) == 0:
                    nodes.append(leaf.parent)
        
        # choose a node and turn it into a leaf
        chosenNode = nodes[random.randint(0, len(nodes) - 1)]
        chosenNode.data = None;
        chosenNode.left = None;
        chosenNode.right = None;
        self.leaves.append(chosenNode)
                  
    def maxDepth(self, root):
        if root == None:
            return 0
        else:
            ldepth = self.maxDepth(root.left)
            rdepth = self.maxDepth(root.right)
            return max(ldepth, rdepth) + 1

    def size(self, root):
        if root == None:
            return 0
        else:
            return self.size(root.left) + 1 + self.size(root.right)

    ''' TODO: how to print NodeData ? '''
    def printTree(self, root):
        if root == None:
            pass
        else:
            self.printTree(root.left)
            print root.data,
            self.printTree(root.right)


if __name__ == "__main__":

    # binary tree working on 3 parameters
    # makes 4 nodes + 5 empty leaves
    print "binary tree"
    newTree = BinaryTree(3)
    newTree.insertRandom()
    newTree.insertRandom()
    newTree.insertRandom()
    newTree.insertRandom()
    # now removes one of possible to remove nodes
    newTree.removeRandom()
