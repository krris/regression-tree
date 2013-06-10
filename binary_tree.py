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
    
    
    ''' @param minMaxParamValues: dictionary of minValue and maxValue of
        every parameter'''
    def __init__(self, parameters=None, minMaxParamValues=None):
        self.ranges = copy.deepcopy(minMaxParamValues)
        # list of data which fits to current leaf
        self.fittingData = []
        # computed mean values of each parameter (only when node is a leaf)
        self.meanData = {}

            
''' Node of a tree '''    
class Node:
    idCounter = count(0)
#     left, right, parent, data = None, None, None, None

    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None
        self.data = NodeData()
        self.isLeaf = True
        self.id = self.idCounter.next()
        

''' A binary tree '''
class BinaryTree:
    # maximal depth of a tree
    maxDepth = 10
    
    ''' Constructs empty binary tree. '''
    def __init__(self, csvData, parameterToPredict):
        self.root = Node()
        self.root.parent = None
        self.leaves = [self.root]
        self.paramToPredict = parameterToPredict
        
        # A list of available parameters from the datasource
        self.parameters = csvData[0].keys()
        self.csvData = csvData
        
        # Get min and max values of each parameter
        self.minMaxParamValues = self.getMinMaxParameterValue(self.csvData)
        
    ''' Generating random tree of depht = maxSize / 2. '''
    def generate(self):
        while self.getTreeDepth(self.root) != self.maxDepth / 2:
            self.insertRandom()

    ''' Inserts random node choosing random parameter with a random range '''
    def insertRandom(self):
        # leaf chosen to turn into a node
        xNode = self.leaves[random.randint(0, len(self.leaves) - 1)]
        
        xNodeData = NodeData(parameters=self.parameters, 
                             minMaxParamValues=self.minMaxParamValues)
        # copying ranges list from the parent if it's not root
        if xNode.parent:
            xNodeData.ranges = copy.deepcopy(xNode.parent.data.ranges)
            xNode.data = xNodeData
            # ranges list is updated basing on the parent parameter value
            self.updateRanges(xNode)
        else:
            xNode.data = xNodeData
        
        # parameter chosen to be changed
        randParam = self.chooseRandomParameter(self.parameters)            
        # value of the chosen parameter
        randValue = self.chooseRandomValue(xNode, randParam)
        
        # filling node data for a new node
        xNodeData.param = randParam
        xNodeData.value = randValue

        # creating new leaves
        xNode.left = Node()
        xNode.right = Node()
        xNode.left.parent = xNode
        xNode.right.parent = xNode
        self.leaves.append(xNode.left)
        self.leaves.append(xNode.right)
        # xNode is not a leaf anymore
        self.leaves.remove(xNode)
        xNode.isLeaf = False
        
        
    ''' Choose a random parameter out of all available parameters without 
    a parameter which will be predicted. The parameter value can't be a string
    (because we want to generate a regression tree, not a classification tree).
    '''
    def chooseRandomParameter(self, parameters):
        randParam = random.choice(self.parameters)
        # a chosen parameter can't be a string
        while (self.isParameterValue(randParam, basestring) or 
               randParam == self.paramToPredict):   
            randParam = random.choice(self.parameters)
        return randParam
    
    ''' Choose a random value for a given parameter. If parameter value is
    a floating point number, will generate also a floating point number. If 
    parameter value is an integer, will generate an integer.'''
    def chooseRandomValue(self, node, parameter):
        # if parameter value is float
        if self.isParameterValue(parameter, float):
            randValue = random.uniform(
                                   node.data.ranges[parameter]['minValue'], 
                                   node.data.ranges[parameter]['maxValue'])        
            
        # if parameter value is an integer
        elif self.isParameterValue(parameter, int):
            randValue = random.randint(
                                   node.data.ranges[parameter]['minValue'], 
                                   node.data.ranges[parameter]['maxValue'])
        else:
            raise ValueError('''Can't choose random parameter value for variable
                             which is not an integer or float!''')
        return randValue
    
    ''' Check if parameter value is the same type like typeToCompare.'''
    def isParameterValue(self, parameter, typeToCompare):
        return isinstance(self.csvData[0][parameter], typeToCompare)

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
        @param csvData: data loaded with csv_loader 
        @returns Dictionary of parameters and corresponding dictionary with
        minValue and maxValue.'''
    def getMinMaxParameterValue(self, csvData):
        minMaxParamValues = {}
        # find max and min of every parameter
        parameters = csvData[0].keys()
        for param in parameters:
            seq = [x[param] for x in csvData]
            minMaxParamValues[param] = {"minValue": min(seq), "maxValue": max(seq)}
        return minMaxParamValues
    
    ''' Computes mean values for every leaf and saves it into meanData dictionary.'''
    def computeMeanLeavesValues(self):
        for leaf in self.leaves:
            self.computeMeanValuesForNode(leaf)
            
    def computeMeanValuesForNode(self, root):
        if root.isLeaf == False:
            raise ValueError("Can't compute mean values for a node which is not a leaf!")
        for param in self.parameters:
            # can't compute mean when parameter value is a string
            if self.isParameterValue(param, basestring):
                pass
            else:
                seq = [x[param] for x in root.data.fittingData]
                if len(seq) == 0:
                    continue
                root.data.meanData[param] = (sum(seq) / len(seq))   
                 
    def insertDataCollection(self, collection):
        for data in collection:
            self.insertData(data, self.root)
            
    def insertData(self, data, root):
        if root.right == None and root.left == None:
            root.data.fittingData.append(data)
            return
        else:
            if data[root.data.param] < root.data.value:
                self.insertData(data, root.left)
            else:
                self.insertData(data, root.right)
            return
        
                  
    def getTreeDepth(self, root):
        if root.isLeaf == True:
            return 0
        else:
            ldepth = self.getTreeDepth(root.left)
            rdepth = self.getTreeDepth(root.right)
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
    
    def printNode(self, root, graph):
        if root == None:
            pass
        else:
            self.printNode(root.left, graph)
            if root.parent == None:
                pass
            elif root.isLeaf == True:
                parentNodeName = (root.parent.data.param +
                                " id: " + str(root.parent.id) +
                                "\n%.2f" % root.parent.data.value)
                childNodeName = "Leaf" + " id: " + str(root.id) + "\n"
                
                leafParamValue = ""
                if self.isParameterValue(self.paramToPredict, basestring):
                    # if parameter value is a string, print all matching data
                    for data in root.data.fittingData:
                        leafParamValue += data[self.paramToPredict] + '\n'
                elif self.paramToPredict in root.data.meanData: 
                    # print mean valuo of predicted data
                    leafParamValue += ("Mean " + self.paramToPredict + ":\n"
                                 + "%.2f" % root.data.meanData[self.paramToPredict])
                else:
                    leafParamValue += "No fitting data"
                    
                edge = pydot.Edge(parentNodeName, childNodeName + leafParamValue)
                graph.add_edge(edge)
            else:    
                parentNodeName = (root.parent.data.param + 
                                  " id: " + str(root.parent.id) +
                                 "\n%.2f" % root.parent.data.value)
                childNodeName = (root.data.param + " id: " + str(root.id) + 
                                 "\n%.2f" % root.data.value)
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
    
#     paramToPredict = "Weight"
    paramToPredict = "Horsepower"
#     paramToPredict = "Car"
    newTree = BinaryTree(cars, paramToPredict)
    newTree.generate()
    
    # insert data to a tree
    newTree.insertDataCollection(cars)
    newTree.computeMeanLeavesValues()
    
    print newTree.getTreeDepth(newTree.root)
     
    # generate output graph
    newTree.printTree("graph.png")
    