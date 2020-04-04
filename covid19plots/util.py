import numpy as np

def runningTotal(cases, days):
    total = []
    numbers = len(cases) - days + 1
    for d in range(numbers):
        t = 0
        for i in range(days):
            t += cases[d + i]
        total.append(t)

    return total

def newCases(cases):
    if len(cases) == 0:
        return []
    dcases = [cases[i+1] - cases[i] for i in range(len(cases)-1)]
    dcases.insert(0, cases[0])
    return dcases

def getFromTo(length, timePeriod, daysBefore, frameNr):
    if daysBefore == 0:
        fromValue = 0
        toValue = timePeriod + frameNr
    else:
        fromValue = length - daysBefore + 1 - timePeriod
        toValue = fromValue + timePeriod + frameNr

    return fromValue, toValue    

# running total that preserves the lenght of the argument list
def runningTotalN(cases, days):
    total = []
    numbers = len(cases) - days + 1
    for d in range(len(cases) -numbers):
        total.append(np.nan)
    for d in range(numbers):
        t = 0
        for i in range(days):
            t += cases[d + i]
        total.append(t)
    return total

def runningAvgN(cases, days):
    return [v/days for v in runningTotalN(cases, days)]

