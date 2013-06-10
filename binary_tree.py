#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import random
import copy
import pydot
from itertools import count
import math

import csv_loader

class NodeData:
    ''' Data connected with every node'''
    param = None
    value = 0
    
    def __init__(self, parameters=None, minMaxParamValues=None):
        ''' @param minMaxParamValues: dictionary of minValue and maxValue of
        every parameter'''
        
        self.ranges = copy.deepcopy(minMaxParamValues)
        # list of data which fits to current leaf
        self.fittingData = []
        # computed mean values of each parameter (only when node is a leaf)
        self.meanData = {}
  
class Node:
    ''' Node of a tree.'''  
    idCounter = count(0)

    def __init__(self):
        self.left = None
        self.right = None
        self.parent = None
        self.data = NodeData()
        self.isLeaf = True
        self.id = self.idCounter.next()

class BinaryTree:
    ''' A binary tree.'''
    # maximal depth of a tree
    maxDepth = 10
    
    def __init__(self, csvData, parameterToPredict):
        ''' Constructs empty binary tree. '''
        self.root = Node()
        self.root.parent = None
        self.leaves = [self.root]
        self.paramToPredict = parameterToPredict
        
        # A list of available parameters from the datasource
        self.parameters = csvData[0].keys()
        self.csvData = csvData
        
        # Get min and max values of each parameter
        self.minMaxParamValues = self.getMinMaxParameterValue(self.csvData)
        
    def generate(self):
        ''' Generating random tree of depht = maxSize / 2.'''
        while self.getTreeDepth(self.root) != self.maxDepth / 2:
            self.insertRandom()

    def insertRandom(self):
        ''' Inserts random node choosing random parameter with a random range'''
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
        
        
    def chooseRandomParameter(self, parameters):
        ''' Choose a random parameter out of all available parameters without 
        a parameter which will be predicted. The parameter value can't be a 
        string (because we want to generate a regression tree, not a 
        classification tree). '''

        randParam = random.choice(self.parameters)
        # a chosen parameter can't be a string
        while (self.isParameterValue(randParam, basestring) or 
               randParam == self.paramToPredict):   
            randParam = random.choice(self.parameters)
        return randParam
    
    def chooseRandomValue(self, node, parameter):
        ''' Choose a random value for a given parameter. If parameter value is
        a floating point number, will generate also a floating point number. If 
        parameter value is an integer, will generate an integer.'''
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
    
    def isParameterValue(self, parameter, typeToCompare):
        ''' Check if parameter value is the same type like typeToCompare.'''
        return isinstance(self.csvData[0][parameter], typeToCompare)

    def updateRanges(self, node):
        ''' Updates ranges list of a node basing on its parent 
        @param node must not be None! '''
        
        parentNode = node.parent
        parentValue = parentNode.data.value
        parentParam = parentNode.data.param
        ranges = node.data.ranges
        
        # check if node is left or right son
        if node == parentNode.left:
            ranges[parentParam]['maxValue'] = parentValue
        else:
            ranges[parentParam]['minValue'] = parentValue
       
    def removeRandom(self):
        ''' Removes random node. Only leaf parent or root can be removed. '''
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
        
    def getMinMaxParameterValue(self, csvData):    
        ''' Get minValue and maxValue of parameters.
        @param csvData: data loaded with csv_loader 
        @returns Dictionary of parameters and corresponding dictionary with
        minValue and maxValue.'''

        minMaxParamValues = {}
        # find max and min of every parameter
        parameters = csvData[0].keys()
        for param in parameters:
            seq = [x[param] for x in csvData]
            minMaxParamValues[param] = {"minValue": min(seq), "maxValue": max(seq)}
        return minMaxParamValues
    
    def computeMeanLeavesValues(self):
        ''' Computes mean values for every leaf and saves it into meanData 
        dictionary.'''
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
#         if root.right == None and root.left == None:
        if root.isLeaf:
            root.data.fittingData.append(data)
            return
        else:
            if data[root.data.param] < root.data.value:
                self.insertData(data, root.left)
            else:
                self.insertData(data, root.right)
#             return

    def getMeanSquaredError(self):
        ''' Compute MSE.
        MSE = 1/n * sum_n (prediction_i - trueValue_i)^2'''
        parameter = self.paramToPredict
        sum_n = 0
        for dataRow in self.csvData:
            predictionValue = self.predictValue(dataRow, parameter, self.root)
            trueValue = dataRow[parameter]
            sum_n += math.pow(predictionValue - trueValue, 2)
        
        n = len(self.csvData)
        mse = sum_n / n
        return mse
    
    def predictValue(self, dataRow, parameter, root):
        '''Get prediction value of a given parameter to predict.'''
        
        if root.isLeaf:
            if parameter in root.data.meanData.keys():
                value = root.data.meanData[parameter]
                return value
            else:
                # just in case if there is no parameter mean value in a leaf
                return 0
        else:
            if dataRow[root.data.param] < root.data.value:
                return self.predictValue(dataRow, parameter, root.left)
            else:
                return self.predictValue(dataRow, parameter, root.right)
         
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

    def printTree(self, path):
        ''' Generate a graph and save it to a file. '''
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
                    # print mean value of predicted data
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
    cars = csv_loader.loadCars("cars.csv")
     
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
    
    print "Mean squared error:"
    print newTree.getMeanSquaredError()
     
    # generate output graph
    newTree.printTree("graph.png")
    