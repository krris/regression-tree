#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import pydot

class Data:
    """
    Class with input data.
    """
    
    # dictionary which contains parameters and values
    # example: 
    # paramValues["param1"] = 666
    paramValues = {} 

class Node:
    param = None
    value = 0
    
    # dictionary which contains a range of every parameter
    # example:  
    # paramRanges["param1"] = {"min": 7, "max": 997} 
    paramRanges = {}
    
    # Number of parameters in every Node.
    # Has to be initialized before use of Node class.
    param_num = 0
    
    # child nodes
    left, right, parent = None, None, None
    
    # list of a data which fits to this node (if it's a leaf)
    fitting_data = []


    def __init__(self, parent_node=None):
        self.left = None
        self.right = None

        # copy every parameter range of a parent node
        if (parent_node):
            self.paramRanges = parent_node.paramRanges.copy()

class BinaryTree:
    def __init__(self):
        self.root = None

    def addEmptyNode(self, parent=None):
        # creates a new node and returns it
        return Node(parent)

    def addNode(self, param, value, parent=None):
        node = Node(parent)
        node.param = param
        node.value = value
        return node

    # insert data to suitable leaf
    def insert(self, root, data):
        if (root.left == None and root.right == None):
            root.fitting_data.append(data)
            return
        else:
            # find a place to insert
            # compare value of node to value of data to insert
            if data.paramValues[root.param] < root.value:
                # go to left sub-tree
                self.insert(root.left, data)
            else:
                # go to right sub-tree
                self.insert(root.right, data)
            return

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

    def printGraph(self, root):
        graph = pydot.Dot(graph_type='graph')
        tree.printNode(root, root, graph)
        graph.write_png('graph.png')


    def printNode(self, treeroot, root, graph):
        if root == None:
            pass
        else:
            self.printNode(treeroot, root.left, graph)
            if root.parent == None:    
                edge = pydot.Edge(treeroot.param + " " + str(treeroot.value), root.param + " " + str(root.value))
            else:    
                edge = pydot.Edge(root.parent.param + " " + str(root.parent.value), root.param + " " + str(root.value))
            graph.add_edge(edge)
            self.printNode(treeroot, root.right, graph)


if __name__ == "__main__":

    tree = BinaryTree()

    # set number of parameters
    Node.param_num = 3
    
    # initialize default parameters for every Node
    Node.paramRanges["param1"] = {"min": -sys.maxint - 1, "max": sys.maxint} 
    Node.paramRanges["param2"] = {"min": -sys.maxint - 1, "max": sys.maxint} 
    Node.paramRanges["param3"] = {"min": -sys.maxint - 1, "max": sys.maxint} 

    # root node
    root = tree.addNode("param1", 5)

    # node on the left side
    root.left = tree.addNode("param2", 6)
    root.left.paramRanges["param1"][max] = 5
    root.left.parent = root
    
    # node on the right
    root.right = tree.addNode("param3", 4)
    root.right.paramRanges["param1"][max] = 5
    root.right.parent = root

    data = Data()
    data.paramValues["param1"] = 1
    data.paramValues["param2"] = 4
    data.paramValues["param3"] = 0

    tree.insert(root, data)
    tree.printGraph(root)


