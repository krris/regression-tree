#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys

# A binary tree
class ParamRange:
    param = None 
    min_value = 0 
    max_value = sys.maxint 

class NodeData:
    param = None
    value = 0
    ranges = []

    def __init__(self, param_no):
        for i in range(param_no):
            self.ranges.append(ParamRange())
            

class Node:
    left, right = None, None
    data = 0

    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

class BinaryTree:
    def __init__(self):
        self.root = None

    def addNode(self, data):
        # creates a new node and returns it
        return Node(data)

    def insert(self, root, data):
        if root == None:
            # if there is no data, add the new one
            return self.addNode(data)
        else:
            # find a place to insert
            if data <= root.data:
                # go to left sub-tree
                root.left = self.insert(root.left, data)
            else:
                # go to right sub-tree
                root.right = self.insert(root.right, data)
            return root

    def isInserted(self, root, data_to_find):
        # check if data is inserted into a tree
        if root == None:
            return False
        else:
            # we found it!
            if data_to_find == root.data:
                return True
            else:
                if data_to_find < root.data:
                    # left sub-tree
                    return self.isInserted(root.left, data_to_find)
                else:
                    # right sub-tree
                    return self.isInserted(root.right, data_to_find)

    def minValue(self, root):
        while(root.left != None):
            root = root.left
        return root.data

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

    def printTree(self, root):
        if root == None:
            pass
        else:
            self.printTree(root.left)
            print root.data,
            self.printTree(root.right)


if __name__ == "__main__":
    p = ParamRange()
    n = NodeData(9)
    print "max value"
    print n.ranges[1].max_value


    tree = BinaryTree()
    root = tree.addNode(3)
    for i in range(1, 5):
        tree.insert(root, i)

    print "Binary tree: "
    tree.printTree(root)
    print
    print "Depth: ", tree.maxDepth(root)
    print "Size: ", tree.size(root)
