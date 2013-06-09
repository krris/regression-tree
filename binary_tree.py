#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import random
import copy
import pydot

''' Data connected with every node
TODO: change maxint/minint to valid max/min value taken from datasource file'''
class NodeData:
    param = None
    value = 0
    
    def __init__(self, parameters):
        self.ranges = {}
        for p in parameters:
            self.ranges[p] = {'minValue': -sys.maxint - 1, 'maxValue': sys.maxint}
            
''' Node of a tree '''    
class Node:
    left, right, parent, data = None, None, None, None

    def __init__(self, data):
        self.left = None
        self.right = None
        self.parent = None
        self.data = data
        self.isLeaf = True

''' A binary tree '''
class BinaryTree:
    
    ''' Constructs empty binary tree 
    @parameters A list of available parameters from the datasource '''
    def __init__(self, parameters):
        self.root = Node(None)
        self.root.parent = None
        self.leaves = [self.root]
        self.parameters = parameters

    ''' Inserts random node choosing random parameter with a random range '''
    def insertRandom(self):
        # leaf chosen to turn into a node
        xNode = self.leaves[random.randint(0, len(self.leaves) - 1)]
        
        xNodeData = NodeData(self.parameters)
        # copying ranges list from the parent if it's not root
        if xNode.parent:
            xNodeData.ranges = copy.deepcopy(xNode.parent.data.ranges)
            xNode.data = xNodeData
            # ranges list is updated basing on the parent parameter value
            self.updateRanges(xNode)
        else:
            xNode.data = xNodeData
        
        # parameter chosen to be changed
        randParam = random.choice(self.parameters)
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
        xNode.isLeaf = False

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
        chosenNode.isLeaf = True
                  
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

    ''' Generate a graph and save it to a file. '''
    def printTree(self, path):
        graph = pydot.Dot(graph_type='graph')
        self.printNode(self.root, graph)
        graph.write_png(path)
    
    ''' TODO: Change printing text to more human-readable style.
        Parameter name has to be added instead of just a number.'''
    def printNode(self, root, graph):
        if root == None:
            pass
        else:
            self.printNode(root.left, graph)
            if root.parent == None:
                pass
            elif root.isLeaf == True:
                edge = pydot.Edge(root.parent.data.param + " " + str(root.parent.data.value),
                                  "Leaf")
                graph.add_edge(edge)
            else:    
                edge = pydot.Edge(root.parent.data.param + " " + str(root.parent.data.value),
                                  root.data.param + " " + str(root.data.value))
                graph.add_edge(edge)
            self.printNode(root.right, graph)


if __name__ == "__main__":

    # binary tree working on 3 parameters
    # makes 4 nodes + 5 empty leaves
    print "binary tree"
    
    parameters = ["param1", "param2", "param3"]
    
    newTree = BinaryTree(parameters)
    newTree.insertRandom()
    newTree.insertRandom()
    newTree.insertRandom()
    newTree.insertRandom()
    # now removes one of possible to remove nodes
    newTree.removeRandom()
    
    # generate output graph
    newTree.printTree("graph.png")
