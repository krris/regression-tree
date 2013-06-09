#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import random
import copy
import pydot
from itertools import count

import csv_loader

''' Data connected with every node'''
class NodeData:
    param = None
    value = 0
    
    ''' @param min_max_param_values: dictionary of minValue and maxValue of
        every parameter'''
    def __init__(self, parameters, min_max_param_values):
        self.ranges = copy.deepcopy(min_max_param_values)
            
''' Node of a tree '''    
class Node:
    left, right, parent, data = None, None, None, None
    idCounter = count(0)

    def __init__(self, data):
        self.left = None
        self.right = None
        self.parent = None
        self.data = data
        self.isLeaf = True
        self.id = self.idCounter.next()
        

''' A binary tree '''
class BinaryTree:
    maxSize = 30
    
    ''' Constructs empty binary tree '''
    def __init__(self, csv_data):
        self.root = Node(None)
        self.root.parent = None
        self.leaves = [self.root]
        
        # A list of available parameters from the datasource
        self.parameters = csv_data[0].keys()
        self.csv_data = csv_data
        
        # Get min and max values of each parameter
        self.minMaxParamValues = self.getMinMaxParameterValue(self.csv_data)
        
    ''' Generating random tree of depht = maxSize / 2. '''
    def generate(self):
        while self.maxDepth(self.root) != self.maxSize / 2:
            self.insertRandom()

    ''' Inserts random node choosing random parameter with a random range '''
    def insertRandom(self):
        # leaf chosen to turn into a node
        xNode = self.leaves[random.randint(0, len(self.leaves) - 1)]
        
        xNodeData = NodeData(self.parameters, self.minMaxParamValues)
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
        # a chosen parameter can't be a string
        while isinstance(xNode.data.ranges[randParam]['minValue'], basestring):    
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
        
    ''' Get minValue and maxValue of parameters.
        @param csv_data: data loaded with csv_loader 
        @returns Dictionary of parameters and corresponding dictionary with
        minValue and maxValue.'''
    def getMinMaxParameterValue(self, csv_data):
        minMaxParamValues = {}
        # find max and min of every parameter
        parameters = csv_data[0].keys()
        for param in parameters:
            seq = [x[param] for x in csv_data]
            minMaxParamValues[param] = {"minValue": min(seq), "maxValue": max(seq)}
        return minMaxParamValues
                  
    def maxDepth(self, root):
        if root.isLeaf == True:
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
        parentId = 0
        childId = 1
        self.printNode(self.root, graph)
        graph.write_png(path)
    
    def printNode(self, root, graph):
        if root == None:
            pass
        else:
            self.printNode(root.left, graph)
            if root.parent == None:
                pass
            elif root.isLeaf == True:
                parentNodeName = (root.parent.data.param + 
                                " %.2f" % root.parent.data.value + 
                                " id: " + str(root.parent.id))
                childNodeName = "Leaf" + " id: " + str(root.id)
                edge = pydot.Edge(parentNodeName, childNodeName)
                graph.add_edge(edge)
            else:    
                parentNodeName = (root.parent.data.param + 
                                 " %.2f" % root.parent.data.value + 
                                 " id: " + str(root.parent.id))
                childNodeName = (root.data.param + " %.2f" % root.data.value + 
                                " id: " + str(root.id))
                edge = pydot.Edge(parentNodeName, childNodeName)
                graph.add_edge(edge)
            self.printNode(root.right, graph)


if __name__ == "__main__":

    print "binary tree"
    
    # load csv_file
    cars = csv_loader.loadCars("small_cars.csv")
     
    # get parameters of csv_file
    parameters = cars[0].keys()
    
    print "Parameters:"
    print parameters
    
    print "Csv data:"
    for car in cars:
        print car
    
    newTree = BinaryTree(cars)
    newTree.generate()
#     newTree.insertRandom()
#     newTree.insertRandom()
#     newTree.insertRandom()
#     newTree.insertRandom() 
#     newTree.insertRandom()
#     newTree.insertRandom()
    # now removes one of possible to remove nodes
#     newTree.removeRandom()
    
    print newTree.maxDepth(newTree.root)
    
     
    # generate output graph
    newTree.printTree("graph.png")
    