# Import the usual numpy and matplotlib libraries for numerical operations and plotting
import numpy as np
import matplotlib.pyplot as plt
from numpy import random as rng



def moonwalkers():
    "Simulate an inning of Moonwalkers batting."
    outs = 0
    onBase = 0
    while(outs <3):
        hit = rng.random()
        if(hit < .4):
            onBase += 1
        else:
            outs += 1
    return np.max([0, onBase -3])

def doubloons():
    "Simulate an inning of Doubloons batting."
    outs = 0
    onBase = 0
    while(outs <3):
        hit = rng.random()
        if(hit < .2):
            onBase += 1
        else:
            outs += 1
    return np.max([0, onBase -1])

def taters():
    "Simulate an inning of Taters batting."
    outs = 0
    score = 0
    while(outs <3):
        hit = rng.random()
        if(hit < .1):
            score += 1
        else: 
            outs += 1
    return score


def teamInning(team):
    '''
    Simulate an inning of baseball by the given team.
    '''

    if(team == "walkers"):
        return moonwalkers()
    elif (team == "doubloons"):
        return doubloons()
    elif (team == "taters"):
        return taters()


def baseballGame(away, home):
    '''
    Simulate a baseball game with home and away teams given.
    '''

    homeScore = 0
    awayScore = 0

    #Simulate 9 innings of baseball
    for inning in range(9):
        awayScore += teamInning(away)
        homeScore += teamInning(home)
    
    #Do more innings if tied
    while(awayScore == homeScore):
        awayScore += teamInning(away)
        homeScore += teamInning(home)
    
    if(awayScore > homeScore):
        return away
    else:
        return home

def season(numGames):
    '''
    Simulate a season in which each team plays a number, numGames, of games against each other team.
    '''

    walkersBeatDoubloons = 0 
    walkersBeatTaters = 0
    tatersBeatDoubloons = 0
    tatersBeatWalkers = 0
    doubloonsBeatWalkers = 0
    doubloonsBeatTaters = 0

    for gameNum in range(numGames):
        #Simulate games
        winner = baseballGame("walkers", "doubloons")
        if winner == "walkers":
            walkersBeatDoubloons += 1
        else:
            doubloonsBeatWalkers += 1
    
        winner = baseballGame("walkers", "taters")
        if winner == "walkers":
            walkersBeatTaters += 1
        else:
            tatersBeatWalkers += 1
    
        winner = baseballGame("doubloons", "taters")
        if winner == "doubloons":
            doubloonsBeatTaters += 1
        else:
            tatersBeatDoubloons += 1

    return np.array([walkersBeatDoubloons, walkersBeatTaters, doubloonsBeatTaters, doubloonsBeatWalkers, tatersBeatDoubloons, tatersBeatWalkers])



numGames = 100000
winTotals = season(numGames)
winPct = winTotals/numGames

winPctLower = np.array([winPct[0], winPct[2], winPct[5]])
winPctUpper = np.array([winPct[3], winPct[4], winPct[1]])

index = np.arange(3)

plt.close()

fig, ax1 = plt.subplots(constrained_layout=True)

p1 = ax1.bar(index, winPctLower)
p2 = ax1.bar(index, winPctUpper, bottom = winPctLower)

plt.ylabel("Win Percentage")
plt.title("Head to head Win Percentage in RLB")
plt.xticks(index, ("Walkers", "Doubloons", "Taters"))

'''
def bottomMatchUps(x):
    if(x == "Walkers"):
        return "Doubloons"
    elif(x == "Doubloons"):
        return "Taters"
    elif(x == "Taters"):
        return "Walkers"

def topMatchUps(x):
    if(x == "Doubloons"):
        return "Walkers"
    elif(x == "Taters"):
        return "Doubloons"
    elif(x == "Walkers"):
        return "Taters"
'''

ax1.set_ylim([0, 1])
ax2 = ax1.twiny()
ax2.set_xticks([1/6,1/2,5/6,1])
ax2.set_xticklabels(("Doubloons", "Taters", "Walkers"))

plt.savefig("riddler9-29-19WinPct.png")
plt.show()
        
print(winPctLower)
