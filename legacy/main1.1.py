# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 18:50:24 2022

@author: Ben Lanoue
This will be another version of main.py
THere maaaay be way to many theta values and not enough data, so instead
I will only use the previous 3 games of each team, and will also exclude
offesnive stats of the opponents 
"""

import numpy as np
import pandas as pd
import random as r
import math
import matplotlib.pyplot as plt
import os
import subprocess

gameNum = 3

def decWeek(week):
    week = week - 1
    if week == 0:
        week = 22
    return week

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
    
#will return -1 or 1 randomly, probs don't need it
def randSign():    
    if r.random() >= 0.5:
        return -1
    return 1


def calc_hx(master,theta,row):
    predY = master[0][row]
    predW = master[1][row]
    teamA = master[2][row]
    teamB = master[3][row]
    
    
    tempW = predW
    tempY = predY
    
    xColNum = len(master.columns) - 5
    
    thetaX = []
    
    selectedRow = []
    
    
    if tempW -1==0:
        tempW=decWeek(tempW)
        tempY=tempY-1
    else:
        tempW=decWeek(tempW)
        
    i=0
    
    while (i<gameNum):
        tempRow = getRow(master,teamA,tempW,tempY)
        if(tempRow!= -1):
            i=i+1
            selectedRow.append(tempRow)
            
            #add the offensive stats of teamA
            for k in range(xColNum):
                thetaX.append(master[k+4][tempRow])
            #end for k
        #end if
        
        if tempW -1==0:
            tempW=decWeek(tempW)
            tempY=tempY-1
        else:
            tempW=decWeek(tempW)
    
    #end while i
    
    i=0
    tempW = predW
    tempY = predY
    
    if tempW -1==0:
        tempW=decWeek(tempW)
        tempY=tempY-1
    else:
        tempW=decWeek(tempW)
    
    while(i<gameNum):
        tempRow = getRow(master,teamB,tempW,tempY)
        if(tempRow!=-1):
            i=i+1
            selectedRow.append(tempRow)
            
            #add the offensive stats of TeamB
            for k in range(xColNum):
                thetaX.append(master[k+4][tempRow])
            #end for k
            #end if
        if tempW -1==0:
            tempW=decWeek(tempW)
            tempY=tempY-1
        else:
            tempW=decWeek(tempW)
    #end while i
    thetaX.append(1)
    
    '''
    After the 2 while i loops the lists thetaX and selectedRow
    should be populated
    thetaX should be size xColNum*6 +1 and
    selectedRow should have 6 ints in it, indicated
    
    selectedRow[0] ->thetaX[0-23]
    selectedRow[1] ->thetaX[24-47]
    etc...
    selectedRow[5] ->thetaX[112-137]
    thetaX[138] will not correlate to anything, as it is just 1
    "the b value in y=mx+b"
    
    '''
    
    
    #calculate the hypothesis
    hx = 0
    for i in range(len(thetaX)):
        hx = hx+ (thetaX[i]*theta[i])
    hx = 1/(1+math.e**(-1*hx))
    
    
    
    return [hx, selectedRow]

def calc_hxNew(master,theta,week,year,teamA,teamB):
    
    predY = year
    predW = week

    tempW = predW
    tempY = predY
    
    xColNum = len(master.columns) - 5
    
    thetaX = []
    
    selectedRow = []
    
    
    if tempW -1==0:
        tempW=decWeek(tempW)
        tempY=tempY-1
    else:
        tempW=decWeek(tempW)
        
    i=0
    
    while (i<gameNum):
        tempRow = getRow(master,teamA,tempW,tempY)
        if(tempRow!= -1):
            i=i+1
            selectedRow.append(tempRow)
            
            #add the offensive stats of teamA
            for k in range(xColNum):
                thetaX.append(master[k+4][tempRow])
            #end for k
        #end if
        
        if tempW -1==0:
            tempW=decWeek(tempW)
            tempY=tempY-1
        else:
            tempW=decWeek(tempW)
    
    #end while i
    
    i=0
    tempW = predW
    tempY = predY
    
    if tempW -1==0:
        tempW=decWeek(tempW)
        tempY=tempY-1
    else:
        tempW=decWeek(tempW)
    
    while(i<gameNum):
        tempRow = getRow(master,teamB,tempW,tempY)
        if(tempRow!=-1):
            i=i+1
            selectedRow.append(tempRow)
            
            #add the offensive stats of TeamB
            for k in range(xColNum):
                thetaX.append(master[k+4][tempRow])
            #end for k
            #end if
        if tempW -1==0:
            tempW=decWeek(tempW)
            tempY=tempY-1
        else:
            tempW=decWeek(tempW)
    #end while i
    thetaX.append(1)
    
    '''
    After the 2 while i loops the lists thetaX and selectedRow
    should be populated
    thetaX should be size xColNum*6 +1 and
    selectedRow should have 6 ints in it, indicated
    
    selectedRow[0] ->thetaX[0-23]
    selectedRow[1] ->thetaX[24-47]
    etc...
    selectedRow[5] ->thetaX[112-137]
    thetaX[138] will not correlate to anything, as it is just 1
    "the b value in y=mx+b"
    
    '''
    
    
    #calculate the hypothesis
    hx = 0
    for i in range(len(thetaX)):
        hx = hx+ (thetaX[i]*theta[i])
    hx = 1/(1+math.e**(-1*hx))
    
    
    return hx





#master[28][i] are the depended variables tested
#for a given hypothesis[z], then hypothesisRow[z] will correlate to a
#dependent variable of master[28][i] such that
#hypothesis[z] -> master[28][hypothesisRow[z]]
def cost(master,hypothesis, hypothesisRow):
    cost = 0

    for i in range(len(hypothesis)):
        cost = cost + (master[28][hypothesisRow[i]]*math.log(hypothesis[i])) + ((1-master[28][hypothesisRow[i]])*math.log(1-hypothesis[i]))
    #end for i
    cost = cost/(-len(hypothesis))
    
    return cost
    
def gradientDescent(master,alpha,T):
    
    print("iterations: ", T)
    print("Learning Rate: ", alpha)
    #First I will create thetas, I will make it so there are 3 sets
    # of 2 teams game sets (Team A, and Team B)
    #First half of the thetas will be team stats for Team A in the past
    #3 games, and the second half the past 3 games for Team B
    
    xColNum = len(master.columns) - 5 #24 independed variables
    rowNum = len(master[28]) #master[28] is a series with win or loss indicated
   
    thetaLength = ((xColNum*6))+1
    
    theta = []
    
    costValues = []
    xcostValues = []
    
    
    
    '''
    #This makes team A's thetas positive and team B's thetas negative,
    #This will help avoid falling into a local min that would be wildy
    #inaccurate. Still possible that we'll fall into a local min, but
    #it will be deeper than having a complete random theta set
    for i in range(thetaLength):
        if i<=thetaLength/2:
            theta.append(r.random())
        else:
            theta.append(r.random()*-1)
    #end for i
    
    
    
    iterations:
        450 @0.7
        3000 @0.1
        200 @0.07
    
    accuracy:0.6686746987951807
    cost:0.5899622234718129
    
    
    '''
    
    theta = [0.071813619966139, -0.6054200612039949, 0.3322087370872743, -0.6530071830139814, 0.4790636296871511, -0.10384201338641476, -0.31345473740379687, 0.6775247082293672, 0.0685747966564183, 0.4784348652846645, 0.49841413019067493, 0.14417139003590027, 0.1569988153331051, 0.3689864146392164, 0.0316423440934469, -0.24569058071294259, 0.0853364917000188, 0.9042901204062767, -0.25807881851946085, -0.5920032668759647, -0.2652583538824257, -0.7968832548169861, -0.03903884010423535, -0.05263464431008967, 0.793312015857549, -0.1483158725566748, 0.17059126514751224, 0.8975157050144343, -0.2799742549636224, 0.03640582978663326, -0.3843059223884006, 0.5249603986490514, 0.3665760655626935, 0.8384282999669963, 0.0866865538910454, -0.18426688895390567, 0.4169435688386637, -0.659236239512881, 0.1868270312803136, -0.06440810664327376, 0.6502294025564436, 0.48646907199844575, 0.32268316517713586, -0.036241587446195746, 0.3554801651997395, -1.2493683479735853, -0.12247214350767745, -0.3708872366641213, -0.9065441245294086, 0.503200024202676, 0.4326620006324375, 0.40279884712289865, 0.44583064815628276, 1.0227176097574546, 1.016304517222456, 0.561666405140533, 0.19923286725268247, 0.7392473141646221, -0.9123719580907219, 0.18102746026368152, 0.14135440805371097, 0.9695280724644546, 0.3475554227638514, -0.2755537000251421, -1.2023644630337909, 0.17906546375283675, -0.6729577393716396, 0.7034077688589689, -0.18723661593105073, -0.3173981952936948, -0.25883727335195006, -0.30325387243229185, 0.15326356907538716, 0.49380996805714533, -0.33742637625460625, 0.6558913016168371, -0.5470097319965893, 0.03066412895634197, 0.21139946315170333, -0.6656882828957674, 0.1150489329732663, -0.5008976983824996, -0.6193544412749361, -0.11929727910813148, -0.16408784838686072, -0.3101137769733495, -0.027852971002018907, 0.14344195744430102, -0.16132244308216764, -0.7611792861695432, 0.18363906975084934, 0.7221171158117506, 0.23210192158891224, 0.6707236989609454, -0.04713475534343726, 0.060947528593379256, -0.7227904714345912, 0.178794017871624, -0.202868210278433, -0.8685395138283166, 0.12736006454210708, 0.16409158070246793, 0.2574034633273252, -0.510465237999557, -0.028761601354763005, -0.9135121569341806, 0.07631104927275678, 0.3401515774824411, -0.48609188223089494, 0.7409228116388126, 0.18743118657530955, -0.3826527536572938, -0.6195615934909523, -0.5459379075030102, -0.29920395734640093, 0.06198101589985927, -0.16252878395462625, 0.9927919509693973, -0.029763272544991667, 0.3071606298885703, 0.4359486158348137, -0.26225293581300496, -0.2796772633170501, -0.24320126486107363, -0.23448958934026803, -0.96810696720506, -1.0338129745449467, -0.37819649515502185, 0.009128874174902844, -0.6447686971795179, 0.9486314811545643, -0.019901621884085827, -0.3025882246055504, -0.9030421842349324, -0.16145460117885246, 0.04060093339422671, 1.0490971144694665, -0.05722054587581723, 0.6886580999126184, -0.8013990560481896, 0.0010843221161208254, 0.4417590879556229, 0.26851020893602007, 0.3345950027763404, -0.0014577532490873339]


    #amount of iterations
    for i in range(T):
        #if (i!=0 and i%100==0):
            #alpha = alpha*0.1
        
        currentH = []
        currentHrow = []
        
        #2d array
        #this will hold a list of list
        #tempThetaRow[i] will be a list of rows used to calculate
        #a hypothesis such that tempThetaRow[z] was used to calculate
        #currentH[z]
        
        tempThetaRow = []
        
        
        
        #Rock this bitch
        #calculate hypothesis for each game capable of getting a hypothesis
        #record needed information from each hypothesis as well
        for j in range(rowNum):
            
            predY = master[0][j]
            predW = master[1][j]
            
            if predW>=4:
                currentHrow.append(j)
                temp = calc_hx(master,theta,j)
                currentH.append(temp[0])
                tempThetaRow.append(temp[1])
            
        #end for j
        
        
        #calculate cost
        costValues.append(cost(master,currentH,currentHrow))
        xcostValues.append(i)
        
        
        #the j here indicates which theta were on. The column/catetgory 
        #j will correlate to will be. We know which category it will be
        #by doing j%24, whatever the remainder is is the category number
        #this work for everything except the last theta, which is "b"
        
        for j in range(thetaLength):
            tempHold = 0
            categoryNum = j%xColNum
            tempRow = j//xColNum
            
            #iterate k for every hypothesis
            for k in range(len(currentH)):
                
                #the number of thetas is 145, 144 'm' values and 1 'b' value
                #but the way this iterates is 0-143 are the 144 'm' values and
                #the b value is 144
                #the way loops work in python is thetaLength is value 145, but
                #will loop through ranges 0-144, which is technically 145 values
                #so subtracting 1 from thetaLength will account for the 'b' value
                if(j!=thetaLength-1):
                    tempHold = tempHold + (currentH[k] - master[28][currentHrow[k]])*master[categoryNum+4][tempThetaRow[k][tempRow]] /len(currentH)
                else:
                    tempHold = tempHold + (currentH[k] - master[28][currentHrow[k]])/len(currentH)
            #end for k
            
            
            #update theta[j]
            theta[j] = theta[j]-alpha*tempHold
            
        #print(theta)
        #end for j
    #end for i
    
    plt.plot(xcostValues,costValues)
    
    
    currentHrow = []
    currentH = []
    correctCount=0
    totalCount = 0
    correct75 = 0
    total75=0
    

    
    #calculate accuracy of thetas
    for j in range(rowNum):
            
        predY = master[0][j]
        predW = master[1][j]
        predT = master[2][j]
        
        if predW>=4:
            
            
            currentHrow.append(j)
            temp = calc_hx(master,theta,j)
            tempH = temp[0]
            
            
            if(tempH>=0.75):
                total75 = total75+1
                if (1 == master[28][j]):
                    correct75 = correct75 + 1
            
            if(tempH>=0.51):
                totalCount = totalCount+1
                if(1 == master[28][j]):
                    correctCount = correctCount+1
            
            
            
        
    #end for j
    
    
    print("accuracy")
    print(correctCount/totalCount)
    print()
    
    print("75%+ accuracy")
    print(correct75/total75)
    print(correct75)
    print(total75)
    print()
    
    print("Cost of Thetas")
    print(costValues[len(costValues)-1])
    print()

    
    
    return theta
    
    
def main():
    df = pd.read_excel("masterPost.xlsx")

    #thetas = gradientDescent(df,0.07,1)
    #print("Thetas: ")
    #print(thetas)  
    
    thetas = [0.071813619966139, -0.6054200612039949, 0.3322087370872743, -0.6530071830139814, 0.4790636296871511, -0.10384201338641476, -0.31345473740379687, 0.6775247082293672, 0.0685747966564183, 0.4784348652846645, 0.49841413019067493, 0.14417139003590027, 0.1569988153331051, 0.3689864146392164, 0.0316423440934469, -0.24569058071294259, 0.0853364917000188, 0.9042901204062767, -0.25807881851946085, -0.5920032668759647, -0.2652583538824257, -0.7968832548169861, -0.03903884010423535, -0.05263464431008967, 0.793312015857549, -0.1483158725566748, 0.17059126514751224, 0.8975157050144343, -0.2799742549636224, 0.03640582978663326, -0.3843059223884006, 0.5249603986490514, 0.3665760655626935, 0.8384282999669963, 0.0866865538910454, -0.18426688895390567, 0.4169435688386637, -0.659236239512881, 0.1868270312803136, -0.06440810664327376, 0.6502294025564436, 0.48646907199844575, 0.32268316517713586, -0.036241587446195746, 0.3554801651997395, -1.2493683479735853, -0.12247214350767745, -0.3708872366641213, -0.9065441245294086, 0.503200024202676, 0.4326620006324375, 0.40279884712289865, 0.44583064815628276, 1.0227176097574546, 1.016304517222456, 0.561666405140533, 0.19923286725268247, 0.7392473141646221, -0.9123719580907219, 0.18102746026368152, 0.14135440805371097, 0.9695280724644546, 0.3475554227638514, -0.2755537000251421, -1.2023644630337909, 0.17906546375283675, -0.6729577393716396, 0.7034077688589689, -0.18723661593105073, -0.3173981952936948, -0.25883727335195006, -0.30325387243229185, 0.15326356907538716, 0.49380996805714533, -0.33742637625460625, 0.6558913016168371, -0.5470097319965893, 0.03066412895634197, 0.21139946315170333, -0.6656882828957674, 0.1150489329732663, -0.5008976983824996, -0.6193544412749361, -0.11929727910813148, -0.16408784838686072, -0.3101137769733495, -0.027852971002018907, 0.14344195744430102, -0.16132244308216764, -0.7611792861695432, 0.18363906975084934, 0.7221171158117506, 0.23210192158891224, 0.6707236989609454, -0.04713475534343726, 0.060947528593379256, -0.7227904714345912, 0.178794017871624, -0.202868210278433, -0.8685395138283166, 0.12736006454210708, 0.16409158070246793, 0.2574034633273252, -0.510465237999557, -0.028761601354763005, -0.9135121569341806, 0.07631104927275678, 0.3401515774824411, -0.48609188223089494, 0.7409228116388126, 0.18743118657530955, -0.3826527536572938, -0.6195615934909523, -0.5459379075030102, -0.29920395734640093, 0.06198101589985927, -0.16252878395462625, 0.9927919509693973, -0.029763272544991667, 0.3071606298885703, 0.4359486158348137, -0.26225293581300496, -0.2796772633170501, -0.24320126486107363, -0.23448958934026803, -0.96810696720506, -1.0338129745449467, -0.37819649515502185, 0.009128874174902844, -0.6447686971795179, 0.9486314811545643, -0.019901621884085827, -0.3025882246055504, -0.9030421842349324, -0.16145460117885246, 0.04060093339422671, 1.0490971144694665, -0.05722054587581723, 0.6886580999126184, -0.8013990560481896, 0.0010843221161208254, 0.4417590879556229, 0.26851020893602007, 0.3345950027763404, -0.0014577532490873339]

    teamA = "TEN"
    teamB = "GNB"
    print("team A odds vs team B")
    teamAodds = calc_hxNew(df, thetas, 11, 2022, teamA, teamB)
    teamBodds = calc_hxNew(df, thetas, 11, 2022, teamB, teamA)
    
    print("TeamA percent chance to win is:" )
    print(teamAodds/ (teamAodds+teamBodds))
    print(teamAodds+teamBodds)
    
    
    return
    

main()














