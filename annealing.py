#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from binarytree import BinaryTree
import csvloader

import copy
import math
import matplotlib.pyplot as plt
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

        # save the worse result (just for plotting)
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
    plt.plot(tempRange, allMSE, marker='.', linestyle='--' )
    
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
    plt.legend()
    
    if pathToSave == None:
        plt.show()
    else:
        plt.savefig(pathToSave)

def changeTemperature(temp, step):
    temp -= step
    return temp
        
if __name__ == "__main__":
    
    ifile = ''
    ofile = ''
    paramToPredict = ''
    temperature = 100
    step = 1
    maxDepth = 20
    
    # i - inputfile
    # p - parameter
    # t - temperature
    # s - step size
    # d - max depth
    myopts, args = getopt.getopt(sys.argv[1:], "i:o:p:t:s:d:")
    
    for option, arg in myopts:
        if option == '-i':
            ifile = arg
        elif option == '-p':
            paramToPredict = arg
        elif option == '-t':
            temperature = int(arg)
        elif option == '-s':
            step = float(arg)
        elif option == '-d':
            maxDepth = float(arg)
        else:
            print("""Usage: %s -i inputCsv -p paramToPredict -t temperature 
                -s step -d maxDepth""" % sys.argv[0])
            
    print ("""Input csv :  %s\nparam: %s\ntemp: %d\nstep: %f\nmaxDepth: %d""" 
           % (ifile, paramToPredict, temperature, step, maxDepth))
    
    # load csv_file
    csvData = csvloader.loadCars(ifile)

    result = simulatedAnnealing(csvData, paramToPredict, temperature=temperature, 
                                    maxDepth=maxDepth, step=step)
    
    print "Result for: ", paramToPredict, " and csv: ", ifile
    print "Solution (best MSE): ", result['bestMSE']
    print "found, when temperature was: ", result['bestTreeTemp']
         
    if len(ofile) == 0:
        # if the directory does not exist, create it
        directory = "img/" + "temp" + str(temperature) + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        path = (directory + paramToPredict + 
            "_max_depth_" + str(maxDepth) + ".png")
         
    else:
        path = ofile
    plotResult(result, "Temperature", paramToPredict + " Mean Squared Error",
                         pathToSave=path)
    
    print "Image written in: ", path
            

#     # load csv_file
#     cars = csvloader.loadCars("cars.csv")
#      
#     # get parameters of csv_file
#     parameters = cars[0].keys()
#     
# #     params = ["Horsepower", "Cylinders", "Displacement", "Weight", "Acceleration", "Model"]
#     params = ["Horsepower"]
#     
#     maxDepth = 5
#     step = 1
#     temperature = 100
#     for paramToPredict in params:
#         result = simulatedAnnealing(cars, paramToPredict, temperature=temperature, 
#                                     maxDepth=maxDepth, step=step)
#         print "Result for: ", paramToPredict    
#         print "Solution (best MSE): ", result['bestMSE']
#         print "found, when temperature was: ", result['bestTreeTemp']
#         
#     path = ("img/" + "temp" + str(temperature) + "/" + paramToPredict + 
#         "_max_depth_" + str(maxDepth) + ".png")
#     
#     plotResult(result, "Temperature", paramToPredict + " Mean Squared Error",
#                      pathToSave=path)



