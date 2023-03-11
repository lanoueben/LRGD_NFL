# -*- coding: utf-8 -*-
"""
Created on Tue Dec  6 20:22:54 2022

@author: Ben Lanoue

This will be a modified versions of the gradient descent 
logistic regression  where instead of using a win or a loss  (0 or 1)
as the dependent variable, we change this to points scored instead.

This will redo the algorithm to make it a gradient descent linear regression
model.

But before doing this, an excelreader2.py and a preProcess2.py is also needed


Todo:
    I need to find what the optimal amount of iterations and learning should
    be in order to get the most accurate predictions.
    
    The method I will try to do this is by only creating a set of thetas using
    the 2021 data only, and optimizing that to predict the 2022 season so far.
    This was I can measure the parameters used to create the optimal 2022
    season predictor, then use the algorithm to create a model for the
    2022+2021 using the previous parameters.


"""


import numpy as np
import pandas as pd
import random as r
import math
import matplotlib.pyplot as plt
import os
import subprocess

gameNum = 4

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
    
    
    
    return hx

def cost(master,hypothesis, hypothesisRow):
    cost = 0
    
    
   #calculate cost using the formula  cost(h(x),y) =  summation[m,i=1][  (0.5 * (hx - y)^2) ] /m
   #m = amount of hypothesis
    for i in range(len(hypothesis)):
        cost = cost + ((hypothesis[i] - master[28][hypothesisRow[i]] )**2 * 0.5)
        #cost = cost + (master[28][hypothesisRow[i]]*math.log(hypothesis[i])) + ((1-master[28][hypothesisRow[i]])*math.log(1-hypothesis[i]))
    #end for i
    cost = cost/(len(hypothesis))
    
    return cost


def thetaAccuracy(df,thetas):
    rowNum = len(df[28])
    
    totalCount = 0
    correctCount = 0
    
    
    
    for j in range(rowNum):
        
        predY = df[0][j]
        predW = df[1][j]
        predT = df[2][j]
        predO = df[3][j]
        
        if (predW>gameNum and predY==2022):
            teamApro = calc_hxNew(df, thetas, predW, predY, predT, predO)
            teamBpro = calc_hxNew(df, thetas, predW, predY, predO, predT)
            
            teamBrow = getRow(df,predO,predW,predY)
            
            #if the algorithm predicts the correct winner, iterate correctCount
            if ( df[28][j]>df[28][teamBrow]):
                totalCount = totalCount+1
                
                #print(predW, predT, predO)
                #print("A cor:", df[28][j] )
                #print("A pre", teamApro)
                #print("B cor:",df[28][teamBrow] )
                #print("B pre", teamBpro)
                #print()
                
                if((teamApro>teamBpro)):
                    correctCount = correctCount+1
                    
            #end if
            
            
        #end if
    #end for j
    
    
    
    #print("The algorithm predicts 2022 with an accuracy of",correctCount/totalCount)           
    
            
    print(correctCount)
    print(totalCount)
    
    
    return correctCount/totalCount









def gradientDescent(master,alpha,T, thetas):
    
    print("iterations: ", T)
    print("Learning Rate: ", alpha)
    #First I will create thetas, I will make it so there are gameNum sets
    # of 2 teams game sets (Team A, and Team B)
    #First half of the thetas will be team stats for Team A in the past
    #3 games, and the second half the past 3 games for Team B
    
    xColNum = len(master.columns) - 5 #24 independed variables
    rowNum = len(master[28]) #master[28] is a series the points scored by team A
   
    thetaLength = ((xColNum*gameNum*4))+1
        
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
    if (thetas[0] == 0):
        theta = []
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
    #end if
    else:
        theta = thetas
    
    

    
    

    #amount of iterations
    for i in range(T):
        
        #Shrink alpha if needed
        
        if(i==(T//10)):
            alpha = alpha*0.1
        
        
        
        
        currentH = []
        currentHrow = []
        
        #2d array
        #this will hold a list of list
        #tempThetaRow[i] will be a list of rows used to calculate
        #a hypothesis such that tempThetaRow[z] was used to calculate
        #currentH[z]
        tempThetaRow = []
        
        #create an array corresponding to the amount of rows.
        #randomize the list so the algorithm grabs games at
        #random instead of the same games in the same order.
        tempRand = []
        for j in range(rowNum):
            tempRand.append(j)
        r.shuffle(tempRand)
        
        
        #Rock this bitch
        #calculate hypothesis for each game capable of getting a hypothesis
        #record needed information from each hypothesis as well
        for j in range(rowNum):
            
            row = tempRand[j]
            predY = master[0][row]
            predW = master[1][row]
            
            if predW>gameNum and predY==2021:
                currentHrow.append(row)
                temp = calc_hx(master,theta,row)
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
        
        #This will update thetas 
        #for all thetas
        #0j = oj - alpha * (summation[m,i=1] [(hx - y)x])/m
        
        for j in range(thetaLength):
            tempHold = 0
            categoryNum = j%xColNum
            tempRow = j//xColNum
            
            #iterate k for every hypothesis
            for k in range(len(currentH)):
                

                if(j!=thetaLength-1):
                    
                    tempHold = tempHold + ( (currentH[k] - master[28][currentHrow[k]])*master[categoryNum+4][tempThetaRow[k][tempRow]])
                else:
                    tempHold = tempHold + (currentH[k] - master[28][currentHrow[k]])
            #end for k
            
            
            #update theta[j]
            theta[j] = theta[j]-alpha*tempHold/len(currentH)
            
        #print(theta)
        #end for j
    #end for i
    
    plt.plot(xcostValues,costValues)
        
    #end for j
    
    #grab the final cost Value from list costValue in the array
    print("Cost of Thetas", costValues[len(costValues)-1])
    print()

    
    
    return theta

def predTeams(teamA, teamB, week, year, thetas, df):

    #print("team A odds vs team B")
    teamApro = calc_hxNew(df, thetas, week, year, teamA, teamB)
    teamBpro = calc_hxNew(df, thetas, week, year, teamB, teamA)
    
    print("For week", week, "in season", year)
    print(teamA, "has a projected to score", teamApro )
    print(teamB, "has a projected to score", teamBpro )
    
    
    return






def main():
    
    df = pd.read_excel("masterPost2.xlsx")
    
    
    #@0.3a, 30i, CoT 49.87, Acc 48%
    #0.1a, 20i, CoT 48.7,Acc 48%
    thetas = [1.0027764933200416, 0.6690440694967983, 0.42496794630171014, -0.3046834857508937, 0.2663789750474402, 0.26129920394487016, 0.886808222329378, 1.4638766179972404, 0.2384518133152281, -0.6177741412327431, 0.012085838726734686, 1.0431684705679027, -0.18952840572991048, 0.6362418960602602, -0.004204646359575855, 0.0383545941881812, 0.7727819637901829, 0.6501829007999945, 1.2050852732334216, 0.1498608408168022, 0.1951429097528093, -0.12238342961591778, 1.141967721532242, 0.5840620333017662, -1.1333447239450927, -0.5891429246669952, -0.3350355794094965, -0.5509799460236945, -0.7371305547746755, -0.3214939693885501, -0.39978147523874624, -1.1443653225710126, 0.6183791825546767, -0.6939533550849598, 0.19090910291471339, 0.4026681471310298, -0.3206443074594129, -0.04800823158951643, -0.5292417030690315, -0.19951177488705915, -1.0235761778885155, -0.8038748648850466, -0.6619265581979925, -0.5338297029414234, -0.020482312586499164, 0.3539924955378244, -0.7921170051072244, -0.4560017623690417, 1.1679200758352117, 0.8743099391487082, 1.975380757689774, 0.7366382915504271, 0.514391665438241, 0.3398127701914208, 0.6867900148072871, 1.5077579839618223, 0.10441341407958771, 0.5045842275456177, 0.052975849102966474, 0.67422842075334, 0.09903022300836714, 0.24899613607671647, -0.11652410752061611, -0.1823494695419667, 0.5719805797515174, 0.35385472775056265, 1.1602460135989134, 0.13483260429597654, 0.251592638359884, -0.11986185390420118, 0.24659482541649116, 0.23250081527740643, 0.1292511938951683, -1.4715586052420033, -0.0014543596154722917, -0.8420329481274613, -0.27955749372387095, -0.48425382284538787, -0.003510999428038861, -0.12377725590980994, 0.3036237469583986, 0.508934182385604, -0.3546992696164405, 0.49719591188705975, -1.1199550168985006, -0.7351824671493967, -0.5210842511707005, 0.7009269183611317, -0.280194401561957, -0.9622186447206647, -0.33977810754901105, -1.094638235634147, -0.4688956609278115, 0.012195602954059784, -0.5220160407623383, -0.8934387284628739, 0.7417101682955379, 0.08522392558380167, 1.6800915390826907, 0.9797744800806446, 0.7916748657683855, 0.8755859459445468, 1.0386000357381033, 0.9858812806798154, 0.35977774846235994, -0.5542742633969588, 0.4724109070112092, 0.9838742225009796, -0.48405543157337544, 0.3132961359714987, 0.5145615201942404, 0.6291461421354027, 1.3662885267802367, 0.8026253846801605, 0.7424498156579569, 0.13400164137814402, 0.1368863559909302, 0.5508372805910546, 1.067474540506732, -1.1150965704430178, -0.3053980636357867, -0.24937589969672783, 0.44127973812905147, -0.6244511251962185, -0.41842329928605226, 0.1885326990313192, -0.5199021160519591, -0.9680659404415405, -0.3711281319563935, 0.09343428730093158, -0.14414907036188704, -0.5618129536770067, -1.1752411508904563, -0.37387490785485805, -0.6120301504839922, 0.3112866867183226, 0.21432253035521037, 0.23727438368770304, -0.38675609820622564, -0.4541671642698811, -0.43511132824551496, 0.09647384880689774, -0.6138836744406558, 0.6060447058580569, -0.055579389816646466, -0.1950199061244782, 0.6943077600020932, 1.0049805700758956, 0.0005037333766420985, 0.4398620893235947, 0.5615487221072744, 0.8784367812208534, 0.705954681682991, 0.4660140345002387, -0.2756227433520076, 0.40509183866423487, 0.731769329275943, -0.020470600707376482, 0.4589664187468611, 0.03346195833679475, 1.197616743302023, 1.2290205764363153, 1.369712427719452, 0.4378422334971882, 0.6862964519824701, 0.09365924162406149, -0.06461755998174604, 0.23056475068739274, -0.2955511812643221, -1.0557385481249293, 0.2553082243320641, -0.3352410667979982, -0.1932218126082777, -0.2759325469890511, -0.3663329254979719, -0.39625137862042037, 0.3619254206959814, -0.14898271915579606, -1.1903456344194583, -0.7210315871209003, -0.7364816267072953, 0.2397625409470097, 0.10557643860460715, 1.055965752066333, -0.06653310463374422, -0.6106417227208666, -0.7181815440497001, 0.19835438835533306, -0.18384526420458652, -0.035975702461960475, -0.6711753103181479, -1.2026768985767635, 0.6999733970319406, -0.3274626369819485, 0.05770111767396581, 0.18161676353154715, 0.19631596589251968, -0.30473184512904045, -0.23422288739357766, -0.5619284415882817, -0.5142201783905909, -0.7078275030937766, -0.7268545700506206, 0.4091899851108322, -0.43979264530471646, -1.4316565451814487, -1.5264661191934068, -1.0953175729142643, -0.2617480213290712, -0.7021623199168463, -0.15237587108489872, -0.5034552352981506, 0.29303935995186564, 0.5918190770846722, -0.2458742889448378, 0.007706577758851222, 0.13305041018781372, 0.8938191323663373, 0.802843201869363, 0.7602317219565506, 0.4645484081370562, 0.8614428151076112, 0.28507820145602425, 0.7057598434897021, 0.11149660361166373, 0.06307464005062657, 0.19708112875544956, 0.7589151237615968, 0.7496077387300586, 0.7050533185760888, 0.4246249383962259, 0.4155846229869283, 0.14825118579981933, 0.09811875674047775, 1.2551661562831053, 0.14000458278717812, 0.8779852088399455, 0.7340236868203827, 0.15699044240342055, -0.01042961795670071, -0.5060848664888575, -0.41731762990228277, 0.2889081520171929, -0.23645548939115932, -0.5722242208766388, -0.24583818364756077, -0.08344323933197977, -0.7434389466005868, -0.9359837547319726, -0.8989653786237792, -0.9402709834098523, 0.2193765824812301, -0.4726978182453498, 0.3113194795741079, 0.4013697129934349, -0.49256125677830814, -0.3072925245706992, -0.26279256419497277, -0.5639448047343272, 0.03771961120081064, -0.09045469258010948, -0.058098435182446215, -0.7493802739096679, -1.1273145931948851, 0.4142700507863539, 0.4744493545565195, 1.706279617063044, 0.24560342659867276, -0.5772995527510915, -0.5203646476853288, 0.9052951852925988, 0.8842674735126005, -0.07000654141837459, 0.46414631019359676, 0.7042738503252108, 0.6113082263042039, 0.022957156838102302, -0.39442274184301956, -0.5278765102106757, -0.3394202042335944, 0.9099924753417993, 0.23888002263300714, -0.008334874288727423, 0.7428942436717172, 0.6359995177035592, 0.7811946919167122, -0.18916130630018838, -0.31102958587869817, 0.21522162250381494, 0.24848540727743285, 0.3119136954818272, -0.6862552015868414, -0.1189105908907369, -1.2261684523405376, -0.490845213755199, -0.45322803503379566, -0.01776596740774811, -1.1039478131845624, -0.013271798575315737, -0.9052595071759401, -1.292426035868824, -0.3703962105674916, -0.6566799621039542, -0.4245815040570343, 0.17216588102445493, 0.17000822077114283, 0.20901224038071725, -0.7009031568905997, -0.23673151656303773, 0.10590167853130013, -0.15735420327540328, -0.6199630742560029, 0.8276010041156268, -0.2525449416848112, 1.1679661756865378, 0.2726433961055902, 1.0828027733984564, 0.5526437131737972, -0.13676035775913675, -0.30785292882858906, -0.21703619412646744, 0.08400421463988367, 0.463772558408477, 0.5843827770276722, -0.3714722069213995, -0.23356422036705152, 0.03315000394213433, -0.6458199514106452, 0.8261207374660856, 0.578131482462223, 0.31325934279531675, 0.28836272456167167, 0.003930478995421938, -0.2576264491166125, 0.1529060147683427, 0.7519472742349301, 0.12490416494517365, -0.6534620744715344, -0.5662529567900226, -1.2966368202484835, -0.5108134643436171, -0.1226562241537383, -0.39578488463125455, -0.2927033702994774, -0.2454070932684076, -0.5607169989400108, -0.10589461081606422, -0.24114368750061996, -1.200470636827471, 0.30728586304318195, -0.06685122595889847, 0.3003634438742819, 0.35372995232246157, 0.5017572970353451, -0.06737439477637037, -0.6601228203606542, 0.008094565073014339, 0.3340782494726774, -1.1199821500024576, -1.252263782258109, 1.0001035786204282, 0.3641699599362061, 0.9145273916822357, 1.6104494528320863, 0.6520570539233249, -0.1782708776110477, 0.3584370618469987, 0.4572768965614706, 0.413218914957767, 0.5176256832992915, 0.36323277262641557, -0.2966363707951379, 0.12626545383639867, 0.903646960836254, 0.14465773636925253, 0.5412161397389703, 0.654880825065611, 0.9142076570243624, 0.518458483604969, 0.5519468706941288, 1.0321264475155865, 0.8889294789650137, -0.4851694415949534, 0.34684240274077954, 23.063620463284206]
    
    thetas = gradientDescent(df,0.01,100,thetas)
    
    print(thetas)
    
    print("2022 Accuracy:",thetaAccuracy(df, thetas))
    
    #print("Thetas:")
    #print(thetas)
    
    
    
    '''
    Run 1000 iterations, and at every 1000%200=0, test and record the
    accuracy of the thetas. Im making the gradient descent only
    learn off of 2021 data, and testing it with 2022 data
    
    thetas = [0]
    thetaSet = []
    it = 0
    iterations = []
    
    highestAcc = 0
    AccIt = 0
    AccTheta = []
    
    
    alpha = 0.7
    for i in range(4):
        it = it+2
        itTemp = it
        temp = gradientDescent(df,alpha,2, thetas)
        thetas = temp
        thetaSet.append(temp)
        iterations.append(itTemp)
        
        accuracy22 = thetaAccuracy(df, thetas)
        
        print(accuracy22)
        
        if(accuracy22>highestAcc):
            highestAcc = accuracy22
            AccIt = it
            AccTheta = thetas
        #end if
        
        
    #end for i
    
    print("Accuracy for 2022:", highestAcc)
    print("Iterations:", AccIt)
    print("Thetas:")
    print(AccTheta)
    
    '''
    
    
    #Test Theta accuracy
    #thetaAccuracy(df,thetas)
    
    
    
    '''
    #Predict new games 1 at a time
    teamA = "NWE"
    teamB = "ARI"
    week = 14
    year = 2022
    
    predTeams(teamA, teamB, week, year, thetas, df)
   
    '''
    
    return



cls = lambda: print("\033[2J\033[;H", end='')
#cls()
main()

































