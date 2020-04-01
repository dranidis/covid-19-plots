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

