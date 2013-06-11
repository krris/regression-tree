#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import csv

def printCsv(csv_file):
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            print row

def loadCars(csv_file):
    ''' Load cars dataset with following columns:
    Car(STRING) 
    MPG(DOUBLE)
    Cylinders(INT)
    Displacement(DOUBLE)
    Horsepower(DOUBLE)
    Weight(DOUBLE)
    Acceleration(DOUBLE)
    Model(INT)
    Origin(CAT)
    @return List of dictionaries with information about car parameters.'''
    
    cars = []
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        parameters = reader.next()
        for row in reader:
            car = {}
            for p in parameters:
                car[p] = row[parameters.index(p)]
            cars.append(car)
    return convertCarData(cars)

def loadCameras(csv_file):
    cameras = []
    with open(csv_file, 'rb') as f:
        reader = csv.reader(f, delimiter=';')
        parameters = reader.next()
        for row in reader:
            camera = {}
            for p in parameters:
                camera[p] = row[parameters.index(p)]
            cameras.append(camera)
    return convertCameraData(cameras)

def convertCameraData(cameras):
    ''' Converting cameras list of dictionaries. Will parse proper parameters from 
    strings to float or integer. '''

    for c in cameras:
        c["Release_date"] = int(c["Release_date"])
        c["Max_resolution"] = float(c["Max_resolution"])
        c["Low_resolution"] = float(c["Low_resolution"])
        c["Effective_pixels"] = float(c["Effective_pixels"])
        c["Zoom_wide"] = float(c["Zoom_wide"])
        
        c["Zoom_tele"] = float(c["Zoom_tele"])
        c["Normal_focus_range"] = float(c["Normal_focus_range"])
        c["Macro_focus_range"] = float(c["Macro_focus_range"])
        c["Storage_included"] = float(c["Storage_included"])
        c["Weight_inc_batteries"] = float(c["Weight_inc_batteries"])
        
        
        c["Dimensions"] = float(c["Dimensions"])
        c["Price"] = float(c["Price"])
    return cameras
    

def convertCarData(cars):
    ''' Converting cars list of dictionaries. Will parse proper parameters from 
    strings to float or integer. '''

    for car in cars:
        car["MPG"] = float(car["MPG"])
        car["Cylinders"] = int(car["Cylinders"])
        car["Displacement"] = float(car["Displacement"])
        car["Horsepower"] = float(car["Horsepower"])
        car["Weight"] = float(car["Weight"])
        car["Acceleration"] = float(car["Acceleration"])
        car["Model"] = int(car["Model"])
    return cars
        
        
# Tests
if __name__ == "__main__":
    cars = loadCars("small_cars.csv")
    for car in cars:
        print car 
        
    cars = loadCars("cars.csv")
    for car in cars:
        print car 
        