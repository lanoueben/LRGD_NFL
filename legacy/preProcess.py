# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 22:15:59 2022

@author: Ben Lanoue
The purpose of this is to edit the "master.xlsx"
and to "Preprocess" the data. It will then 
create a new excel file that will 


This includes, first converting all the appropriate strings
into numbers/integers.
Next is to normalize the values. 
Win, year week won't be normalized.
The team name will also not be normalized (This will stay a string)
Normalization Scale formula:
    
x= instance of a field
x’= normalized scaled value
xmin= the lowest value in the category (for all fields)
xmax=the high value in the category (for all fields)
xavg= mean value of the category
x' = (x-(xaverage)) / (xmax-xmin)

This will get an approximate range of -1<= x'<=1
which is desired

    columns = ["year","week","team","opponent","first downs", "rush", "rush yards", "rush td",
               "cmp", "att","pass yards", "pass td", "int", "sacks", "sack yards",
               "net yards", "total yards","fumbles", "fumble to", "to",
               "penalties", "penalty yards", "3 conversions","3 attempts",
               "4 conversions", "4 attempt", "min", "sec", "win"]
    
    
Before running this program, delete the current "masterPost.xlsx"
and create a new excel file, and name it "masterPost"
"""

import numpy as np
import pandas as pd
import random as r
import math
import matplotlib.pyplot as plt
import os
import subprocess



def getMin(series):
    minNum = series[0]
    
    for i in series:
        if minNum>i:
            minNum=i
    
    return float(minNum)
def getMax(series):
    maxNum = series[0]
    
    for i in series:
        if maxNum<i:
            maxNum = i
    
    return float(maxNum)
def getAvg(series):
    size = len(series)
    temp = 0
    
    for i in series:
        temp = temp+i
        
    return temp/size

def main():
    preM = pd.read_excel("master.xlsx")
    minL = []
    maxL = []
    avgL = []
    rowNum = preM.shape[0]
    columnNum = preM.shape[1]
    #Converting number strings into Integers
    
    #print(preM[0]) This prints a Series (a single column)
    
    #Converting number strings into Integers
    #Series preM[2] & preM[3] will remain strings
    for i in range(rowNum):
        preM[0][i] = int(preM[0][i])
        preM[1][i] = int(preM[1][i])
    
    #Don't convert preM[2] & preM[3] as theyre team names
    for i in range(4,columnNum):
        preM[i] = preM[i].astype(float)
        for j in preM[i]:
            preM[i][j] = float(j)
    #for i in range(columnNum):
        #print(type(preM[i][0]))


    #The preM is now converted to the appropriate data types,
    #Now it's time to normalized the values.
    #This won't effect the categories of "year","week","team","opponent"
    #& "win"
    #First for each series, I need to find the max and min of each category
    #The first 4 columns won't be normalized, and the last column (win)
    #won't be normalized, so the for loop will represent this
    for i in range(4,columnNum -1):
        minL.append(getMin(preM[i]))
        maxL.append(getMax(preM[i]))
        avgL.append(getAvg(preM[i]))
    
    
    print(avgL)
    dif =[]
    #calculate max-min
    for i in range(len(maxL)):
        dif.append(maxL[i]-minL[i])
    #print(dif)
    #normalize the values using values avgL[i-4] and dif[i-4]
    for i in range(4,columnNum -1):
        temp1 = avgL[i-4]
        temp2 = dif[i-4]
        for j in range(rowNum):
            preM[i][j] = (preM[i][j] - temp1)/temp2
            
    
    print(preM)
    preM.to_excel("masterPost.xlsx",index=False)
    

    return

main()





