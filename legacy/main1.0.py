# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 19:25:28 2022

@author: Ben Lanoue
This programs serves 2 purposes, to create the algorithm and to test
how well the algorithm works.

This will all go under the function "main"
"""
import numpy as np
import pandas as pd
import random as r
import math
import matplotlib.pyplot as plt
import os
import subprocess


#Helper functions


#This function is create to decrement a week by 1, if the week
#reaches 0, then it will reset to week 22, which would be the
#week of the last game of the season (post extra game added).
def decWeek(week):
    week = week - 1
    if week == 0:
        week = 22
    return week

#given a team, a week, and a year, this will return the related row
#otherwise return -1 which indicates it doesn't exist 
def getRow(master,team,week,year):
    rowNum = -1
    rows = len(master[28])
    
    for i in range(rows):
        if(master[0][i]==year and master[1][i]==week and master[2][i].lower() == team.lower()):
            return i
        #end if
    #end for
    
    return rowNum
    #end getRow

#This function is made to calculate a hypothesis.
#The input will be master: the dataframe of data
#Theta: a list of current theta values
#row:The year,week,team,opp you're predicting
#This assumes the row that was inputed has a valid week and year in
#which a hypothesis could be made
def calc_hx(master,theta,row):
    tempYear = master[0][row]
    tempWeek = master[1][row]
    teamName = master[2][row]
    OppName = master[3][row]
    
    a = tempWeek
    
    xColNum = len(master.columns) - 5
    
    #This will hold the values which will correlate with the list theta
    #multiplying the correlating index and adding them all will generate a pre-hypothesis value
    thetaPair = []
    
    selectedRow = []
    
    if tempWeek-1==0:
        tempWeek = decWeek(tempWeek)
        tempYear = tempYear-1
    else:
        tempWeek = decWeek(tempWeek)
        
    tempWeekj = tempWeek
    tempYearj = tempYear
    
    #now using tempWeek, tempYear, teamName, and OppName, 
    #i will represent the amount of games which the teamName team has added to thetaPair (Offense and Defense included)
    #j will represent the OppName team by the same metric
    i=0
    j=0

    while(i<5):
        tempRow = getRow(master, teamName,tempWeek, tempYear)
        #print(tempRow)
        if(tempRow != -1):
            i=i+1
            selectedRow.append(tempRow)
            for k in range(xColNum):
                thetaPair.append(master[k+4][tempRow])
            
            #Now change the row to get the current oppenent of the team and add
            #their stats to the thetaPair list
            tempRow = getRow(master, master[3][tempRow],master[1][tempRow],master[0][tempRow])
            selectedRow.append(tempRow)
            for k in range(xColNum):
                thetaPair.append(master[k+4][tempRow])
            #end for


        #decrement the week/year
        if tempWeek-1==0:
            tempWeek=decWeek(tempWeek)
            tempYear = tempYear-1
        else:
            tempWeek=decWeek(tempWeek)
        
    #End while i
    
    #Do this all again for OppName
    while(j<5):
        tempRow = getRow(master,OppName , tempWeekj, tempYearj)
        #print(tempRow, " ", OppName, " ", tempWeekj)
        if(tempRow != -1):
            j=j+1
            selectedRow.append(tempRow)
            for k in range(xColNum):
                thetaPair.append(master[k+4][tempRow])
            
            tempRow = getRow(master,master[3][tempRow],master[1][tempRow],master[0][tempRow])
            selectedRow.append(tempRow)
            
            for k in range(xColNum):
                thetaPair.append(master[k+4][tempRow])
            #end for
        if tempWeekj-1==0:
            tempWeekj = decWeek(tempWeekj)
            tempYearj = tempYearj-1
        else:
            tempWeekj = decWeek(tempWeekj)
    #end while j
    
    
    #After the i and j while loops, the last thing needed is the coefficient
    #for the "b" value in y=mx + b
    #for this, the value will always just be 1 which will need to be added
    #to the end of thetaPair, as theta should already have this value
    thetaPair.append(1)
    
    
    #Now that there is all the necessary variables found and stored, a 
    #hypothesis will be generated. "prediction" will be the value before
    #converting to a value betweeen 0-1 using a sigmoid function
    
    
    '''
    sigmoid function
    z = the sum of theta[i]*thetaPair[i]
    
    sigmoid = 1/ (1+ e^(-z))
    
    sigmoid will then be a value between 0-1 which in this case will give
    the % chance that one team will win over another team
    '''
    
    prediction = 0
    for i in range(len(theta)):
        prediction = prediction + (theta[i]*thetaPair[i])
        
    #print(prediction)
    
    hypothesis = 1/(1+(math.e**(-1*prediction)))
    
    return [hypothesis,selectedRow]



#The y value will be master[28][hypothesisRow[i]]
#hypothesis will be a list of hypothesis for each row
#hypothesisRow will show which row will correlate with
#each hypothesis (hypothesis[i] will be the hypothesis for row
#hypthesisRow[i])
#master is the dataframe
def calc_cost(hypothesis,hypothesisRow,master):
    hNum = len(hypothesis)
    cost = 0
    for i in range(hNum):
        
        #need to fix domain error, (math.log(i)), i cannot be 0 or a negative number
        #I will need to check 2 different cases, if hypothesis[i] is 1 or 0,
        #if this can occurs
        #1 will change to 0.9999999999
        #and 0 will change to 0.0000000001
        currentH = hypothesis[i]
        '''
        if (currentH == 1):
            currentH = 0.9999999999
        if (currentH == 0):
            currentH = 0.0000000001
        '''
        
        
        cost = cost+ (-master[28][hypothesisRow[i]]*math.log(currentH) - ((1-master[28][hypothesisRow[i]]) * math.log(1-currentH)))/hNum
    
    return cost


#master[28][i] will be the dependent variable
#master[4-27][i] will be independent variables
#master[0-3][i] will be used for time/search/order purposes



def gradientDescent(master,alpha,T):
    
    #This be a list of cost values. For each iteration (T), the cost
    #of the current iteration will be recorded.
    #This will help assess if the cost of each new formula is decreasing, and
    #thus becoming more accurate.
    costValues = []
    #graphing puproses
    xcostValues = []
    
    #amount of independent variable columns
    xColNum = len(master.columns) - 5
    rowNum = len(master[28])
    
    #amount of thetas which will be used
    #2 teams, both offense and defense stats for each game
    #5 games
    #+1 is the "b" variable in y=mx+b, everything else will be "m"s
    thetaLength = ((xColNum * 4) * 5) + 1
    theta = []
    for i in range(thetaLength):
        if i <= (thetaLength/2):
            temp = i//(xColNum*2)
        else:
            temp = (i - (thetaLength/2))//(xColNum*2)
                
        
        
        
        theta.append(r.random()/(2**(temp)))
    #print(theta)
    for i in range(T):
        #This will be the size of the amount of predictions there are for
        #every game that a prediction can be made
        #Note that the first 5 games in the data set chronological wise
        #cannot have a hypothesis, as there aren't enough previous
        #game data to generate a hypothesis.
        tempHypothesis = []
        
        #This will be used to find which row on master[][row] will correlate
        #to in tempHypothesis. So tempHypothesis[i] will correlate to
        #master[][tempHypothesisRow[i]].
        #This will be needed for update thetas after calculating the hypothesis
        tempHypothesisRow = []
        
        #tempThetaRow will be a 2d array of values which will correlated
        #to the tempHypothesis. Each list in the array will represent
        #which rows were used to generate a given hypothesis.
        #Ex. for hypothesis tempHypothesis[i], the list
        #tempThetaRow[i] will return a 1d array of 20 values,
        #These 20 values will correlate to the 20 rows used to
        #generate tempHypothesis[i]
        tempThetaRow = []
        
        #Next iterate through every game to create a hypothesis for the
        #selected game. 
        #I will do this by iterating through every row and checking
        #if the year is 2021, then there can't be a hypothesis until
        #week>=6
        #Otherwise a hypothesis should be possible (2022 games will
        #will draw upon 2021 games in chronological order if needed)
        for j in range(rowNum):
            
            tempYear = master[0][j]
            tempWeek = master[1][j]
            
            if tempYear>2021 or tempWeek>=6:
                tempHypothesisRow.append(j)
                temp = calc_hx(master,theta,j)
                tempThetaRow.append(temp[1])
                tempHypothesis.append(temp[0])
            
        #end for j
        
        
        
        #Now will be the time to iterate through every hypothesis, and to
        #update thetas based on how close they are to the real value
        #iterate through every theta
        for j in range(len(theta)):
            tempTheta = 0
            
            #iterate through every hypothesis generated
            #note that theta 0-479 represent "m" in y=mx + b,
            #and b is represented by 480
            for k in range(len(tempHypothesis)):
                if(j!=480):

                    #master[((480-j)%24)+4][tempThetaRow[k][(j//24)-1]] is a complicated
                    #value call, but this is eventually becomes the value associated first with the correct
                    #theta coefficient (j), and also the correct game related to the hypothesis, lets simplify the call
                    #by changing it to master[category][row]
                    
                    #category =( (480-j) %24) + 4
                    #so the category that is associated with theta is going to be master[4-28][row]
                    #so using mod division will find which of the 4-28 is needed. Adding 4 will pass the 0-3 values
                    
                    #row = tempThetaRow[k][(j//24)]
                    #tempThetaRow is a 2d array which store the 20 different rows used for each
                    #hypothesis generated. k represents which hypothesis is specified, while
                    #the (j//24) finds which row is needed. 
                    
                    
                    tempTheta = tempTheta+(tempHypothesis[k] - master[28][tempHypothesisRow[k]])*master[((479-j)%24)+4][tempThetaRow[k][j//24]] /481
                else:
                    tempTheta = tempTheta + (tempHypothesis[k]-master[28][tempHypothesisRow[k]])/481
                #end if/else
            #end for k
            theta[j] = theta[j] - alpha*tempTheta
        #end for j
            
        
        #now with the new theta[], the cost of it will be calculated to see
        #how inaccurate the current theta[] is. first tempHypothesis and
        #tempHypothesis row will reset
        tempHypothesis = []
        tempHypothesisRow = []
        
        #Next recalculate the hypothesis, with the tempHypothesisRow
        for j in range(rowNum):
            
            tempYear = master[0][j]
            tempWeek = master[1][j]
            
            if tempYear>2021 or tempWeek>=6:
                tempHypothesisRow.append(j)
                temp = calc_hx(master,theta,j)
                #tempThetaRow.append(temp[1]) this isn't needed for calculating a new hypothesis, only adjusting thetas
                tempHypothesis.append(temp[0])
        #end for j
        
        #now with the new hypothesis, calculate cost
        tempCost = calc_cost(tempHypothesis,tempHypothesisRow,master)
        
        costValues.append(tempCost)
        xcostValues.append(i)
    #end for i
    
    plt.plot(xcostValues,costValues)
    #print("cost Values")
    #print(costValues)
    print()
    
    tempHypothesis = []
    correctCount = 0
    totalCount = 0
    #test the thetas
    for j in range(rowNum):
        tempYear = master[0][j]
        tempWeek = master [1][j]
        
        if tempYear>2021 or tempWeek>=6:
            totalCount = totalCount+1
            temp = calc_hx(master, theta, j)
            tempH = temp[0]
            if tempH >= 0.5:
                tempH = 1
            else:
                tempH = 0
            
            if (tempH == master[28][j]):
                correctCount = correctCount+1
    
    print("accuracy")
    print(correctCount/totalCount)
    print()    
    
    
    
    return theta


def main():
    df = pd.read_excel("masterPost.xlsx")
    #print(df)
    #df[category][row]
    
    formula = gradientDescent(df,0.01,400)
    print("thetas")
    print(formula)
    
    
    pass

main()





















