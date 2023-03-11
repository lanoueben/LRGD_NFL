# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 22:20:47 2022

@author: Ben Lanoue

3rd iteration of this algorithm based off of main2.py
This will account for the past 3 games, and then also account
for team "defense" stats (defense stats will just be a given team's opponent
for a given week.)

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
        #This gets the games related to teamA, I will need to add
        #another search for defensive stats.
        tempRow = getRow(master,teamA,tempW,tempY)
        if(tempRow!= -1):
            i=i+1
            selectedRow.append(tempRow)
            
            #add the offensive stats of teamA
            for k in range(xColNum):
                thetaX.append(master[k+4][tempRow])
            #end for k
            
            #Add the defensive stats of teamA
            tempDRow = getRow(master,master[3][tempRow],tempW,tempY)
            selectedRow.append(tempDRow)
            for k in range(xColNum):
                thetaX.append(master[k+4][tempDRow])
            #end for k
                
            
        #end if
        
        if tempW -1==0:
            tempW=decWeek(tempW)
            tempY=tempY-1
        else:
            tempW=decWeek(tempW)
    
    #end while i
    
    #This adds the teamB stats, aka the opponent to teamB
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
            
            #Add the defensive stats of teamB
            tempDRow = getRow(master,master[3][tempRow],tempW,tempY)
            selectedRow.append(tempDRow)
            for k in range(xColNum):
                thetaX.append(master[k+4][tempDRow])
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
    thetaX should be size xColNum*gameNum*2*2+1
    We multiply gameNum by 2 twice, once for the teamB, and another
    to account for defensive stats for each teamA and teamB
    
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
            
            #add the offensive stats of teamA
            for k in range(xColNum):
                thetaX.append(master[k+4][tempRow])
            #end for k
            
            #Add the defensive stats of teamA
            tempDRow = getRow(master,master[3][tempRow],tempW,tempY)
            for k in range(xColNum):
                thetaX.append(master[k+4][tempDRow])
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
            #add the offensive stats of TeamB
            for k in range(xColNum):
                thetaX.append(master[k+4][tempRow])
            #end for k
            
            #Add the defensive stats of teamB
            tempDRow = getRow(master,master[3][tempRow],tempW,tempY)
            for k in range(xColNum):
                thetaX.append(master[k+4][tempDRow])
            #end for k
            
            
        #end if
        if tempW -1==0:
            tempW=decWeek(tempW)
            tempY=tempY-1
        else:
            tempW=decWeek(tempW)
    #end while i
    thetaX.append(1)
    
    
    #calculate the hypothesis
    hx = 0
    for i in range(len(thetaX)):
        hx = hx+ (thetaX[i]*theta[i])
    hx = 1/(1+math.e**(-1*hx))
    
    
    return hx

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
    #First I will create thetas, I will make it so there are gameNum sets
    # of 2 teams game sets (Team A, and Team B)
    #First half of the thetas will be team stats for Team A in the past
    #3 games, and the second half the past 3 games for Team B
    
    xColNum = len(master.columns) - 5 #24 independed variables
    rowNum = len(master[28]) #master[28] is a series with win or loss indicated
   
    thetaLength = ((xColNum*gameNum*4))+1
    
    theta = []
    
    costValues = []
    xcostValues = []
    
    
    
    
    #This makes team A's thetas positive and team B's thetas negative,
    #as well as make the defensive stats of teamA be negative, and
    #make the defensive stats of teamB's  positive. This makes sense
    #bc if teamA's give huge amounts of defensive stats, then this should
    #decrease the chance to win.A defensive stat is just an opponents
    #offensive stats in a given game.
    
    #This will help avoid falling into a local min that would be wildy
    #inaccurate. Still possible that we'll fall into a local min, but
    #it will be deeper than having a complete random theta set
    
    '''
    for i in range(thetaLength):
        #teamA's stats
        if i<=thetaLength/2:
            
            polarity = 1
            if((i//xColNum) %2 == 1):
                polarity = -1
            theta.append(r.random() * polarity)
        #teamB's stats
        else:
            polarity = 1
            if((i//xColNum) %2 == 1):
                polarity = -1
            theta.append(r.random()*-1*polarity)
    #end for 
    
    
    
    
    Iterations:
        1000 @0.3
        2000 @0.07
        5000 @ 0.07
        
        accuracy = 0.7731343283582089
        Cost = 0.4554304391170479
    
    
    
    '''
    theta = [0.29797884392950885, -1.2537341067252503, 0.2420249513959888, -0.9790053318177347, 0.6413847390447146, -0.1447169482180503, 0.26000503105725165, 0.5974115775975233, 0.2904035805663098, 0.3060120915657821, 0.2558310038806525, -0.38385386094863, -0.24784162756594627, 0.5549761418219562, 0.1800572748960924, -0.3713309858884605, 0.6326928721700514, 0.29561311546854907, -1.100712782931844, -0.3164543932162742, -0.18399110044607686, 0.002356349028836564, -0.8163715076300262, 0.16369952602356255, 0.10867235813570376, -0.8883378058236162, -0.8433363950320266, -0.7189438015013802, -0.9582223653398902, 0.5646513032551301, 0.5796379849540592, -0.7669876846382175, 0.27364041417654184, 0.5922963771724874, 1.2927294400116116, 0.6242283599015661, 0.027228020958286827, -0.45465195064866537, 0.44886884598398086, 0.5987484430589948, 0.6697976155333016, -0.4971114490732351, 0.11169791738462667, -0.3877022925917254, -0.8953511165058049, 0.6381339167795432, 0.1490045923744462, 0.3995693528668835, 1.352086429927141, -0.28880137004641937, 0.8216596233527518, 0.4445486647939333, 0.017128214954648113, 0.24278505636164088, -0.22886460420945592, -0.0480233557283694, 0.18245714935934587, 1.0410669150102014, 0.3965589159292218, -0.40573497742840225, 0.6477071858354196, -0.7532986071982823, 0.08151940426043511, 0.3729543537607238, 0.12317122008797261, 0.5495587550888076, -0.004692039645436807, 0.21533676607572458, 0.22864721585664408, -1.053546718812441, -0.5583420282724386, -0.22901955819137398, 0.16431915900465466, -1.3574184147796973, -0.58419288209498, 0.5730717758898476, 0.36938175907169446, -0.5147874458756856, -0.013176031857754901, -0.07869314985739087, 0.5588646926705494, 0.07396220388240066, -0.4188847062341178, 0.2799094511997827, 0.08156090242959031, 0.05584560840843233, 0.5045686096724722, 1.2168904059163501, 0.03427639618974331, -0.5764228919943186, 0.2918040783265344, -0.28846022067912463, -0.11849402791065301, 0.003060610314841248, 0.6756794192099906, 0.2548880428215499, 0.15445558288719785, -0.25123677328641314, 0.5818965135966246, 0.12220316583510178, 0.5692246071380823, 1.0019300712938453, 0.9549476867779729, 0.4200433711339476, -0.2815885836773552, 0.6526864019868224, -0.8617518001591266, 0.02202852144114326, -0.10822197858727632, 1.4454712969843109, 0.300648230620062, -0.0403132069080888, -1.0032968971947, 0.2516942962174659, -0.90016889499868, 0.5935993011077109, -0.17468322096479869, -0.48630595821144645, 0.13013604315444, -1.4685372309011082, -1.4461076953423018, 0.07697952701590849, -0.5788847127625302, -0.47129318227623457, 0.7146560393321805, -0.5705183522896752, 0.2867158759113798, 0.022227658327350484, 0.2979995913299159, -0.1985458652951512, -0.4941871872013501, 0.24974899471073214, -0.1959041890235073, 0.8716935027209329, -0.12442711373606519, -0.07279754074479605, -0.9200117201680554, 0.43507860753462146, 0.6622370843553802, 0.11484839931561983, 1.0623144876514226, 0.13142400858869205, 0.691767272003929, -1.2377387627532188, 0.20920617520066648, 1.238844555081744, -0.379949113334688, 0.909619936446051, -0.7658178992397239, 0.0999978782755597, -0.15537545380230908, -0.6872732904240955, 0.046759094099335326, -0.40931476860373206, -0.4157895751703129, 0.34731704116051115, -0.11371219059377809, -0.5347596145603221, 0.023796870436063076, 0.13027903227448037, -0.5627257458090759, -0.47120783994591414, 0.7352852112756909, 0.5586789746309702, -0.1452743893129593, 0.02508867133484836, 1.0711906349742195, -0.07614869486086509, -0.059415333579198384, 0.6001599105720442, 0.8211016661535997, 0.680272067630153, 1.0826875072055273, -0.8621469656597841, -0.5004747853726209, 0.8055243516979145, -0.05238465840444202, -0.5832195140779745, -1.3779415282243683, -0.9054243320127713, 0.10730366451155465, 0.41197343528065566, -0.17294361165184072, -0.9139822111273592, -0.5025328624645636, 0.34063189395154053, 0.2691077638786456, 0.21135962363686298, 0.8192553598162274, -0.3707277500972061, 0.047289743550729714, -0.22076985756597617, -1.5644760782588254, 0.23257743589290278, -0.6823625415511924, -0.34607007483112545, 0.09979270198005073, -0.3988525796857164, 0.4039423816343923, 0.048621395274406315, -0.06773581679435683, -0.9401554218054415, -0.3149085275311538, 0.4103400038079462, -0.5099133198980046, 0.8848788058534758, -0.16953090619276664, -0.3792684797764921, -0.0018854498581489082, -0.8210833877486504, 0.20830713239042534, -0.3175311788075916, -0.3140572790238135, 1.154814426222327, 0.33216650376382645, 0.2900525474750825, -0.3504080807131477, 1.3135632862580897, 0.7142151132925739, -0.6598355212699025, -0.3692694661205761, 0.6289259097976195, 0.0901586406252688, 0.07397209146571908, -0.44945379223110776, -0.2621755544954522, 0.60973261718721, -0.397702835915586, -0.020605599523515688, -0.05675923845133358, -0.4467416717815201, -1.249754051101708, -0.12916487914907418, 0.8301653464934485, -0.49200881709922417, 0.30079249435255717, 0.17998994267349328, -0.10858679378173133, -0.6126683065158778, -0.0505970769263637, 0.4447827817100655, 0.08573673260453223, -0.4920158373881493, -0.31850770340508155, -0.4006181783585217, -1.5010158854210423, -1.0221091237520552, -0.46150506630290594, 0.05992400475311552, -0.9147192404269687, 1.2432423908259085, 0.05736045053335716, -0.23092644036657403, -1.23041225360839, -0.7883039564441862, 0.36117719957689004, 1.0192466399603777, -0.22772982048576523, 1.245609686034025, -0.7093186114472801, 0.39297840728542904, 0.4827427537289205, -0.2757399990195232, 1.3372640352158454, 1.281135974948457, 0.04620090330837132, 0.4493281088857302, 0.5147884378413898, -0.8395088661459368, 0.9590115206760669, -0.2439742418901994, -0.04614573458248332, -0.2588990727742726, 0.22259823059304942, 0.2985774768973278, -0.30944659167417976, 0.24471680871144735, -1.0730536943353755, 0.37338408595189854, 0.08618248763082313, 1.0544696181876054, -0.5754387915978553, -0.824761344323164, -0.14458710588118168, -1.252939514950869, -0.08236474625673101, -0.5346828449455849, 1.1431350397337592, -0.013278482052564083]
    
    

    

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
            
            if predW>gameNum:
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
            
        #predY = master[0][j]
        predW = master[1][j]
        #predT = master[2][j]
        
        if predW>=4:
            
            
            currentHrow.append(j)
            temp = calc_hx(master,theta,j)
            tempH = temp[0]
            
            
            if(tempH>=0.9):
                total75 = total75+1
                if (1 == master[28][j]):
                    correct75 = correct75 + 1
            
            if(tempH>=0.5):
                totalCount = totalCount+1
                if(1 == master[28][j]):
                    correctCount = correctCount+1
            
            
            
        
    #end for j
    
    
    print("accuracy")
    print(correctCount/totalCount)
    print()
    
    print("90%+ accuracy")
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
    
    
    
    '''
    thetas = gradientDescent(df,0.13,10)
    print("Thetas:")
    print(thetas)  
    
    '''
    thetas = [0.29797884392950885, -1.2537341067252503, 0.2420249513959888, -0.9790053318177347, 0.6413847390447146, -0.1447169482180503, 0.26000503105725165, 0.5974115775975233, 0.2904035805663098, 0.3060120915657821, 0.2558310038806525, -0.38385386094863, -0.24784162756594627, 0.5549761418219562, 0.1800572748960924, -0.3713309858884605, 0.6326928721700514, 0.29561311546854907, -1.100712782931844, -0.3164543932162742, -0.18399110044607686, 0.002356349028836564, -0.8163715076300262, 0.16369952602356255, 0.10867235813570376, -0.8883378058236162, -0.8433363950320266, -0.7189438015013802, -0.9582223653398902, 0.5646513032551301, 0.5796379849540592, -0.7669876846382175, 0.27364041417654184, 0.5922963771724874, 1.2927294400116116, 0.6242283599015661, 0.027228020958286827, -0.45465195064866537, 0.44886884598398086, 0.5987484430589948, 0.6697976155333016, -0.4971114490732351, 0.11169791738462667, -0.3877022925917254, -0.8953511165058049, 0.6381339167795432, 0.1490045923744462, 0.3995693528668835, 1.352086429927141, -0.28880137004641937, 0.8216596233527518, 0.4445486647939333, 0.017128214954648113, 0.24278505636164088, -0.22886460420945592, -0.0480233557283694, 0.18245714935934587, 1.0410669150102014, 0.3965589159292218, -0.40573497742840225, 0.6477071858354196, -0.7532986071982823, 0.08151940426043511, 0.3729543537607238, 0.12317122008797261, 0.5495587550888076, -0.004692039645436807, 0.21533676607572458, 0.22864721585664408, -1.053546718812441, -0.5583420282724386, -0.22901955819137398, 0.16431915900465466, -1.3574184147796973, -0.58419288209498, 0.5730717758898476, 0.36938175907169446, -0.5147874458756856, -0.013176031857754901, -0.07869314985739087, 0.5588646926705494, 0.07396220388240066, -0.4188847062341178, 0.2799094511997827, 0.08156090242959031, 0.05584560840843233, 0.5045686096724722, 1.2168904059163501, 0.03427639618974331, -0.5764228919943186, 0.2918040783265344, -0.28846022067912463, -0.11849402791065301, 0.003060610314841248, 0.6756794192099906, 0.2548880428215499, 0.15445558288719785, -0.25123677328641314, 0.5818965135966246, 0.12220316583510178, 0.5692246071380823, 1.0019300712938453, 0.9549476867779729, 0.4200433711339476, -0.2815885836773552, 0.6526864019868224, -0.8617518001591266, 0.02202852144114326, -0.10822197858727632, 1.4454712969843109, 0.300648230620062, -0.0403132069080888, -1.0032968971947, 0.2516942962174659, -0.90016889499868, 0.5935993011077109, -0.17468322096479869, -0.48630595821144645, 0.13013604315444, -1.4685372309011082, -1.4461076953423018, 0.07697952701590849, -0.5788847127625302, -0.47129318227623457, 0.7146560393321805, -0.5705183522896752, 0.2867158759113798, 0.022227658327350484, 0.2979995913299159, -0.1985458652951512, -0.4941871872013501, 0.24974899471073214, -0.1959041890235073, 0.8716935027209329, -0.12442711373606519, -0.07279754074479605, -0.9200117201680554, 0.43507860753462146, 0.6622370843553802, 0.11484839931561983, 1.0623144876514226, 0.13142400858869205, 0.691767272003929, -1.2377387627532188, 0.20920617520066648, 1.238844555081744, -0.379949113334688, 0.909619936446051, -0.7658178992397239, 0.0999978782755597, -0.15537545380230908, -0.6872732904240955, 0.046759094099335326, -0.40931476860373206, -0.4157895751703129, 0.34731704116051115, -0.11371219059377809, -0.5347596145603221, 0.023796870436063076, 0.13027903227448037, -0.5627257458090759, -0.47120783994591414, 0.7352852112756909, 0.5586789746309702, -0.1452743893129593, 0.02508867133484836, 1.0711906349742195, -0.07614869486086509, -0.059415333579198384, 0.6001599105720442, 0.8211016661535997, 0.680272067630153, 1.0826875072055273, -0.8621469656597841, -0.5004747853726209, 0.8055243516979145, -0.05238465840444202, -0.5832195140779745, -1.3779415282243683, -0.9054243320127713, 0.10730366451155465, 0.41197343528065566, -0.17294361165184072, -0.9139822111273592, -0.5025328624645636, 0.34063189395154053, 0.2691077638786456, 0.21135962363686298, 0.8192553598162274, -0.3707277500972061, 0.047289743550729714, -0.22076985756597617, -1.5644760782588254, 0.23257743589290278, -0.6823625415511924, -0.34607007483112545, 0.09979270198005073, -0.3988525796857164, 0.4039423816343923, 0.048621395274406315, -0.06773581679435683, -0.9401554218054415, -0.3149085275311538, 0.4103400038079462, -0.5099133198980046, 0.8848788058534758, -0.16953090619276664, -0.3792684797764921, -0.0018854498581489082, -0.8210833877486504, 0.20830713239042534, -0.3175311788075916, -0.3140572790238135, 1.154814426222327, 0.33216650376382645, 0.2900525474750825, -0.3504080807131477, 1.3135632862580897, 0.7142151132925739, -0.6598355212699025, -0.3692694661205761, 0.6289259097976195, 0.0901586406252688, 0.07397209146571908, -0.44945379223110776, -0.2621755544954522, 0.60973261718721, -0.397702835915586, -0.020605599523515688, -0.05675923845133358, -0.4467416717815201, -1.249754051101708, -0.12916487914907418, 0.8301653464934485, -0.49200881709922417, 0.30079249435255717, 0.17998994267349328, -0.10858679378173133, -0.6126683065158778, -0.0505970769263637, 0.4447827817100655, 0.08573673260453223, -0.4920158373881493, -0.31850770340508155, -0.4006181783585217, -1.5010158854210423, -1.0221091237520552, -0.46150506630290594, 0.05992400475311552, -0.9147192404269687, 1.2432423908259085, 0.05736045053335716, -0.23092644036657403, -1.23041225360839, -0.7883039564441862, 0.36117719957689004, 1.0192466399603777, -0.22772982048576523, 1.245609686034025, -0.7093186114472801, 0.39297840728542904, 0.4827427537289205, -0.2757399990195232, 1.3372640352158454, 1.281135974948457, 0.04620090330837132, 0.4493281088857302, 0.5147884378413898, -0.8395088661459368, 0.9590115206760669, -0.2439742418901994, -0.04614573458248332, -0.2588990727742726, 0.22259823059304942, 0.2985774768973278, -0.30944659167417976, 0.24471680871144735, -1.0730536943353755, 0.37338408595189854, 0.08618248763082313, 1.0544696181876054, -0.5754387915978553, -0.824761344323164, -0.14458710588118168, -1.252939514950869, -0.08236474625673101, -0.5346828449455849, 1.1431350397337592, -0.013278482052564083]
    
    
    teamA = "ARI"
    teamB = "SFO"
    week = 11
    year = 2022
    #print("team A odds vs team B")
    teamAodds = calc_hxNew(df, thetas, week, year, teamA, teamB)
    teamBodds = calc_hxNew(df, thetas, week, year, teamB, teamA)
    
    print("For week", week, "in season", year)
    print(teamA, "percent chance to win aginst", teamB )
    print(teamAodds/ (teamAodds+teamBodds))
    #print(teamAodds+teamBodds)
    
    
    
    return



cls = lambda: print("\033[2J\033[;H", end='')
cls()
main()

































