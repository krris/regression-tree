#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import os

temperatures = ['50', '100', '500']
maxDepths = ['10', '20', '30']

# test cars
print "Start testing cars..."
params = ["Horsepower", "Cylinders", "Displacement", "Weight", 
          "Acceleration", "Model"]
 
for depth in maxDepths:
    for temp in temperatures:
        for param in params:
            os.system("./annealing.py -i cars.csv -p " + param + 
                      " -t " + temp +" -s 1 -d " + depth)
 
print "End testing cars."
 
# test cameras
print "Start testing cameras..."

params = ["Release_date", "Max_resolution", "Low_resolution","Effective_pixels",
          "Zoom_wide","Zoom_tele","Normal_focus_range",
          "Macro_focus_range","Storage_included","Weight_inc_batteries",
          "Dimensions","Price"]

for depth in maxDepths:
    for temp in temperatures:
        for param in params:
            os.system("./annealing.py -i camera.csv -p " + param + 
                      " -t " + temp +" -s 1 -d " + depth)

print "End testing cameras."
