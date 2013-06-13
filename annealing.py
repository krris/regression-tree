#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from binarytree import BinaryTree
import csvloader

import copy
import math
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import random
import os
import sys
import getopt

def simulatedAnnealing(csvData, paramToPredict, temperature=1000, maxDepth=20, 
                       step=1):
    # a list of all computed Mean Squared Errors
    allMSE = []
    # a list of all temperature values
    allTemp = []
   
    # a list of decisions MSE, when a worse decision was chosen
    worseDecisionMSE= []
    # a list of decisions temperature, when a worse decision was chosen
    worseDecisionTemp = []
    
    theWorstMSE = 0
    
    # best fitting tree
    bestTree = None
    bestMSE = None
    bestTreeTemp = None
    
    temp = temperature 
    # set initial tree
    BinaryTree.maxDepth = maxDepth
    tree = BinaryTree(csvData, paramToPredict)
    tree.generate()
    tree.insertDataCollection(csvData)
    tree.computeMeanLeavesValues()
    treeMSE = tree.getMeanSquaredError()
    
    while temp > 0:
        # get a neighbouring tree
        newTree = tree.generateNeighbouringTree()
        newTree.clearAllFittingData()
        newTree.insertDataCollection(csvData)
        newTree.computeMeanLeavesValues()
        newTreeMSE = newTree.getMeanSquaredError()

        # save the worst result (just for plotting)
        if treeMSE > theWorstMSE:
            theWorstMSE = treeMSE
        if newTreeMSE > theWorstMSE:
            theWorstMSE = newTreeMSE
        
        # check if newTree gives better result than bestTree
        if newTreeMSE < bestMSE or bestMSE == None:
            bestTree = copy.deepcopy(newTree)
            bestMSE = newTreeMSE
            bestTreeTemp = temp
            
        delta = (newTreeMSE - treeMSE)
        if delta <= 0:
            tree = copy.deepcopy(newTree)
            treeMSE = newTreeMSE
        else:
            x = random.uniform(0,1)
            if x < math.exp(-delta/temp):
                worseDecisionMSE.append(newTreeMSE)
                worseDecisionTemp.append(temp)
                tree = copy.deepcopy(newTree)
                treeMSE = newTreeMSE
        print "Temp: ", temp
        
        allMSE.append(treeMSE)
        allTemp.append(temp)
        temp = changeTemperature(temp, step)

    result = {"bestTree": bestTree, "allMSE": allMSE, "allTemp":allTemp, 
              "temperature":temperature, "step":step, "theWorstMSE":theWorstMSE,
              "bestMSE":bestMSE, "worseDecisionMSE":worseDecisionMSE, 
              "worseDecisionTemp":worseDecisionTemp, "bestTreeTemp": bestTreeTemp}
    return result

def plotResult(result, xlabel, ylabel, pathToSave=None):
    allMSE = result["allMSE"]
    theWorstMSE = result["theWorstMSE"]
    bestMSE = result['bestMSE']
    tempRange = result['allTemp']
    worseDecisionChosenMSE = result['worseDecisionMSE']
    worseDecisionChosenTemp = result['worseDecisionTemp']
    
    # clear last image
    plt.clf()
    
    # plot every result
    plt.plot(tempRange, allMSE)
    
    # plot when the worse decision was chosen
    plt.scatter(worseDecisionChosenTemp, worseDecisionChosenMSE, s=10, 
                color='m', marker='s', label="Worse decision is chosen")
    
    # plot best result
    plt.plot([result['bestTreeTemp']], [result['bestMSE']], "ro", 
             label="Best solution")
    
    # set axis length
    plt.axis([tempRange[0],0, bestMSE - (0.05 * bestMSE), 
              theWorstMSE + (0.05 * theWorstMSE)])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)   

    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(prop = fontP, loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True)
    
    if pathToSave == None:
        plt.show()
    else:
        plt.savefig(pathToSave)

def changeTemperature(temp, step):
    temp -= step
    return temp

def usage():
    print("""Usage: %s -i input.csv -o output.png -p paramToPredict 
        [-t arg] [-s arg ] [-d arg] [-g treeGraph.png]""" % sys.argv[0])
    print ""
    print "-i: input CSV file"
    print "-o: output graph"
    print "-p: parameter to predict"
    print "-t: temperature value (default: 100)"
    print "-s: one step size (default: 1)" 
    print "-d: max tree depth (default: 20)" 
    print "-g: generate tree graph"
    
    print "\nExample:"
    print "$ python annealing.py -i cars.csv -p Weight -t 5 -s 0.01 -d 10 -o plotting.png -g treegraph.png"
        
if __name__ == "__main__":
    
    ifile = ''
    ofile = ''
    paramToPredict = ''
    temperature = 100
    step = 1
    maxDepth = 20
    treeGraphPath = ''
    
    # i - inputfile
    # o - output plotting
    # p - parameter
    # t - temperature
    # s - step size
    # d - max depth
    # g - output tree graph
    myopts, args = getopt.getopt(sys.argv[1:], "i:o:p:t:s:d:g:")
    
    minArg = 7
    if len(sys.argv) < minArg:
        usage()
        sys.exit(0)
         
    for option, arg in myopts:
        if option == '-i':
            ifile = arg
        elif option == '-o':
            ofile = arg
        elif option == '-p':
            paramToPredict = arg
        elif option == '-t':
            temperature = int(arg)
        elif option == '-s':
            step = float(arg)
        elif option == '-d':
            maxDepth = int(arg)
        elif option == '-g':
            treeGraphPath = arg   
        else:
            usage()
                         
    print ("""Input csv :  %s\nparam: %s\ntemp: %d\nstep: %f\nmaxDepth: %d""" 
           % (ifile, paramToPredict, temperature, step, maxDepth))
     
    # load csv_file (camera.csv or cars.csv only)
    if ifile == "cars.csv":
        csvData = csvloader.loadCars(ifile)
        csvDir = "cars/"
    else:
        csvData = csvloader.loadCameras(ifile)
        csvDir = "cameras/"
 
    result = simulatedAnnealing(csvData, paramToPredict, temperature=temperature, 
                                    maxDepth=maxDepth, step=step)
     
    print "Result for: ", paramToPredict, " and csv: ", ifile
    print "Solution (best MSE): ", result['bestMSE']
    print "found, when temperature was: ", result['bestTreeTemp']
          
    if len(ofile) == 0:
        # if the directory does not exist, create it
        directory = "img/" + csvDir + "temp" + str(temperature) + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
             
        path = (directory + paramToPredict + 
            "_max_depth_" + str(maxDepth) + ".png")
          
    else:
        path = ofile
    plotResult(result, "Temperature", paramToPredict + " Mean Squared Error",
                         pathToSave=path)
    print "Function plotting saved in: ", path
     
    # save output graph
    if len(treeGraphPath) != 0:
        bestTree = result['bestTree']
        bestTree.printTree(treeGraphPath)            
        print "Graph saved in: ", treeGraphPath



