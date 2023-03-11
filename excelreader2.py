# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 22:17:46 2022

@author: Ben Lanoue
The purpose of this file is to convert raw excel game data spreadsheets
and converts them into a single "master.xlsx". 

Before running this program, delete the current "master.xlsx"
and create a new excel file, and name it "master"
"""

import numpy as np
import pandas as pd
import random as r
import math
import matplotlib.pyplot as plt
import os
import subprocess
import xlsxwriter


def processFile(year, week,masterPath,filePath, tempFile):
    
    
    jrpd = pd.read_excel(filePath+ "//" +tempFile,dtype=str);
    #print(jrpd)
    #rowNum = len(jrpd.index)
    #print(jrpd);
    #pandasObject.iloc[row,column]
    #print(jrpd.iloc[0,1]);
    
    #These are the columns of the master speadsheet 
    columns = ["year","week","team","opponent","first downs", "rush", "rush yards", "rush td",
               "cmp", "att","pass yards", "pass td", "int", "sacks", "sack yards",
               "net yards", "total yards","fumbles", "fumble to", "to",
               "penalties", "penalty yards", "3 conversions","3 attempts",
               "4 conversions", "4 attempt", "min", "sec", "score"]
    #colNum=len(columns)
    #df.columns[2] is the home team
    #Creating 2 arrays for each team
    #temp will be used as an temp string
    #c will be used as a temp array
    a = []
    b = []
    
    print(year)
    print(week)
    print(jrpd.columns[1])
    print(jrpd.columns[2])
    

#Filling the first teams data into a
    a.append(year)
    a.append(week)
    a.append(jrpd.columns[1]) #team name
    a.append(jrpd.columns[2]) #opponent
    a.append(jrpd.iloc[0,1]) #First Down
    temp = jrpd.iloc[1,1] #Rush-yds-TD
    c = temp.split("-")
    for d in c:
        a.append(d)
    
    temp = jrpd.iloc[2,1] #Cmp-Att-Yd-TD-INT
    c = temp.split("-")
    for d in c:
        a.append(d)
    
    temp = jrpd.iloc[3,1] #Sacked-Yards
    c = temp.split("-")
    for d in c:
        a.append(d)
    
    a.append(jrpd.iloc[4,1]) #Net Pass Yard
    a.append(jrpd.iloc[5,1]) #Total Yards
    
    temp = jrpd.iloc[6,1] #Fumbles-Lost
    c = temp.split("-")
    for d in c:
        a.append(d)
        
    a.append(jrpd.iloc[7,1]) #Turnovers
    
    temp = jrpd.iloc[8,1] #Penalties-Yards
    c = temp.split("-")
    for d in c:
        a.append(d)
        
    temp = jrpd.iloc[9,1] #Third down conversions-Third down attempts
    c = temp.split("-")
    for d in c:
        a.append(d)
    
    temp = jrpd.iloc[10,1] #Fourth down conversions - Third down attempts
    c = temp.split("-")
    for d in c:
        a.append(d)
    
    temp = jrpd.iloc[11,1] #Time of Posession MIN - TOP SEC
    c = temp.split(":")
    a.append(c[0])
    a.append(c[1])
    
    a.append(jrpd.iloc[12,1]) #score

    
    
#Filling the escond teams data into b
    b.append(year)
    b.append(week)
    b.append(jrpd.columns[2])
    b.append(jrpd.columns[1])
    b.append(jrpd.iloc[0,2])
    temp = jrpd.iloc[1,2]
    c = temp.split("-")
    for d in c:
        b.append(d)
    
    temp = jrpd.iloc[2,2]
    c = temp.split("-")
    for d in c:
        b.append(d)
    
    temp = jrpd.iloc[3,2]
    c = temp.split("-")
    for d in c:
        b.append(d)
    
    b.append(jrpd.iloc[4,2])
    b.append(jrpd.iloc[5,2])   
    
    temp = jrpd.iloc[6,2]
    c = temp.split("-")
    for d in c:
        b.append(d)
        
    b.append(jrpd.iloc[7,2])  
    
    temp = jrpd.iloc[8,2]
    c = temp.split("-")
    for d in c:
        b.append(d)
        
    temp = jrpd.iloc[9,2]
    c = temp.split("-")
    for d in c:
        b.append(d)
    
    temp = jrpd.iloc[10,2]
    c = temp.split("-")
    for d in c:
        b.append(d)
    
    temp = jrpd.iloc[11,2]
    c = temp.split(":")
    b.append(c[0])
    b.append(c[1])
    
    b.append(jrpd.iloc[12,2])
    
#Adding the games into the master excel sheet
    master = pd.read_excel(io=masterPath)
    #master = master.iloc[0:0]
    
    a_series= pd.Series(data=a)
    master = master.append(a_series, ignore_index=True)
    b_series= pd.Series(data=b)
    master = master.append(b_series, ignore_index=True)
    
    
  

    #master.append(pd.Series(b),ignore_index=True)
    
    #print(master)
    master.to_excel("master2.xlsx",index=False)
    
    #print(b)
    #print(jrpd.columns[1])


#This will use
#processFile(year, week,masterPath,filePath, tempFile)
#And appropriately browse the data
cwd = os.getcwd() + "\data"
#print(cwd)

#os.remove("master.xlsx")
#open("master.xlsx","x")
#excel = xlsxwriter.Workbook("master.xlsx")
#excel.add_worksheet()

for yearFolder in os.listdir(cwd):
    year = yearFolder
    cwdYear = cwd + "\\" + yearFolder
    for weekFolder in os.listdir(cwdYear):
        week = weekFolder
        week = week.lower()
        week = week.strip("week")
        cwdWeek = cwdYear + "\\" + weekFolder
        for gameData in os.listdir(cwdWeek):
            #print(year)
            #print(week)
            processFile(year,week,"master2.xlsx",cwdWeek, gameData)
 




























     


